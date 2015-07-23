# -*- coding: utf-8 -*-

import os
import signal
import time

from Signals.SignalHandler import SignalHandler
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


registerHandler = SignalHandler.registerHandler


TIME = lambda: time.strftime('%H:%M:%S')
WAIT = lambda msg:  '{0} [\033[33m wait \033[0m] {1}'.format(TIME(), msg)
ERROR = lambda msg: '{0} [\033[31m ERROR \033[0m] {1}'.format(TIME(), msg)


class Watcher(FileSystemEventHandler):

    allowed_extensions = set(('po', 'pt', 'py', 'xml', 'csv', 'zcml'))

    def __init__(self, paths, forkloop, minimum_wait=2.0):
        FileSystemEventHandler.__init__(self)
        self.forkloop = forkloop
        self.observers = []
        self.paths = paths
        self.minimum_wait = minimum_wait
        self.last_event = time.time()

    def start(self):
        """Start file monitoring thread
        """

        registerHandler(signal.SIGINT, self._exitHandler)
        registerHandler(signal.SIGTERM, self._exitHandler)

        for path in self.paths:
            print WAIT("Watchdog is watching for changes in %s" % path)
            observer = Observer()
            self.observers.append(observer)
            observer.schedule(self, path=path, recursive=True)
            observer.start()

    def _exitHandler(self):
        for observer in self.observers:
            observer.stop()

    def on_any_event(self, event):
        extension = event.src_path.split('.')[-1].lower()

        if extension in self.allowed_extensions:
            event_type = event.event_type
            event_path = event.src_path

            event_relpath = event_path
            for path in self.paths:
                abspath = os.path.abspath(path)
                if event_relpath.startswith(abspath):
                    event_relpath = os.path.relpath(event_relpath, abspath)
                    break

            if self.last_event + self.minimum_wait < time.time():
                print WAIT("Watchdog got %s event on %s"
                           % (event_type, event_relpath))
                try:
                    self.forkloop.forkNewChild()
                    self.last_event = time.time()
                except Exception as e:
                    print ERROR(str(e))
            else:
                print WAIT("Watchdog skipped %s event on %s"
                           % (event_type, event_relpath))


class ForkLoop(object):

    def __init__(self):

        self.fork = True  # Must be 'True' to create new child on start
        self.active = False
        self.pause = False
        self.killed_child = True
        self.forking = False
        self.exit = False

        self.parent_pid = os.getpid()
        self.child_pid = None

    def isChild(self):
        return self.child_pid == 0

    def isChildAlive(self):
        if self.isChild():
            return True
        elif self.child_pid is not None and os.path.exists('/proc'):
            return os.path.exists('/proc/%i' % self.child_pid)
        elif self.child_pid is not None:
            try:
                os.kill(self.child_pid, 0)
                return True
            except OSError:  # [Errno 3] No such process
                return False
        else:
            return False

    def _scheduleFork(self, signum=None, frame=None):
        self.fork = True

    def _childIsGoingToDie(self, signum=None, frame=None):
        self.killed_child = True

    def start(self):
        """Start fork loop
        """
        # SIGCHLD tells us that child process has really died and we can spawn
        # new child
        registerHandler(signal.SIGCHLD, self._waitChildToDieAndScheduleNew)

        # With SIGUSR1 child can tell that it dies by request, not by exception
        # etc.
        registerHandler(signal.SIGUSR1, self._childIsGoingToDie)

        self.loop()

    def loop(self):
        """Magic happens
        """
        registerHandler(signal.SIGINT, self._parentExitHandler)
        registerHandler(signal.SIGTERM, self._parentExitHandler)

        self.active = True

        print WAIT("Fork loop now starting on parent process %i" % os.getpid())
        while True:
            self.forking = False

            if self.exit:
                return

            if self.fork:
                self.fork = False

                if self.pause:
                    # Pause mode. No forks now.
                    continue

                if not self.killed_child:
                    print ERROR(
                        "Forked child process died on bootup. "
                        "Fix possible errors and save edits. "
                        "We are now paused until we detect the next file "
                        "change..."
                    )

                    # Child died because of unknown reason. Mark it as killed
                    # and go into pause mode.
                    self.killed_child = True
                    self.pause = True
                    continue

                if self.isChildAlive():
                    # Child is still alive for some reason. Lets wait few
                    # rounds for it to die.
                    continue

                self.forking = True
                self.child_pid = os.fork()
                if self.child_pid == 0:
                    break
                self.killed_child = False

            time.sleep(1)

        self.forking = False

        print WAIT("Fork loop forked a new child process %i" % (os.getpid()))

    def forkNewChild(self):
        """STEP 1 (parent): New child process forking starts by killing the
        current child process.

        """
        if not self.active:
            raise Exception("Cannot fork the process, because the fork loop "
                            "has not been started yet")

        if self.forking:
            raise Exception("Cannot fork the process, because there should be "
                            "serious forking action already going on")

        if self.child_pid is None:
            raise Exception("Cannot kill a process fork, because there should "
                            "not be one yet")

        self.pause = False

        if self.isChildAlive() or self.isChild():
            self._killChild()
        else:
            # Ok, we already have sent the SIGINT the child, but asking for new
            # child
            print WAIT("Fork loop scheduling a new fork")
            self._scheduleFork()

        self.killed_child = True

    def _killChild(self):
        if self.isChild():
            # Signal parent that this is requested kill, not an error situation
            os.kill(self.parent_pid, signal.SIGUSR1)
            # Kill itself
            os.kill(os.getpid(), signal.SIGINT)
        else:
            os.kill(self.child_pid, signal.SIGINT)

    def _parentExitHandler(self, signum=None, frame=None):
        if self.exit:
            return

        self.exit = True

        if self.isChild():
            return

        while self.isChildAlive():
            # XXX: Somehow this may get stuck if we don't print before kill
            print WAIT("Fork loop is terminating its child process %s" %
                       self.child_pid)
            self._killChild()
            time.sleep(2)

    def _waitChildToDieAndScheduleNew(self, signal=None, frame=None):
        """STEP 2 (parent): Child told us via SIGCHLD that we can spawn new
        child

        """
        if self.isChild():
            # Ignore grandchildren
            return

        try:
            # Acknowledge dead child
            pid, exit_status = os.wait()

            if pid != self.child_pid:
                # Ignore unknown children
                return

            exit_flags = []
            if os.WCOREDUMP(exit_status):
                exit_flags.append("core dumped")
            if os.WIFSIGNALED(exit_status):
                code = os.WTERMSIG(exit_status)
                exit_flags.append("terminated by signal %d" % code)
            if os.WIFEXITED(exit_status):
                code = os.WEXITSTATUS(exit_status)
                exit_flags.append("exited with code %d" % code)

            if exit_status == 0:
                print WAIT("Fork loop terminated child process %d" % pid)

            elif exit_flags:
                print ERROR("Forked child process %d %s"
                            % (pid, ", ".join(exit_flags)))
            else:
                print ERROR("Forked child process %d exited with code %s"
                            % (pid, exit_status))

        except OSError:
            # OSError: [Errno 10] No child processes
            pass

        # Schedule new
        self._scheduleFork()
