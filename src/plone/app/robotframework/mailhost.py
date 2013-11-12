# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary


class MockMailHost(RemoteLibrary):

    def get_the_last_sent_email(self):
        """Return the last sent email from MockMailHost sent messages storage
        """
        return self.MailHost.messages[-1] if self.MailHost.messages else u""
