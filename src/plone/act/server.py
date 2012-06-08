import select
import socket


def start(zope_layer_dotted_name):

    COUNT = 50

    from plone.act import Zope2ServerLibrary

    print '=' * COUNT
    print "Starting Zope 2 server"

    print "layer : {0}".format(zope_layer_dotted_name)
    print '=' * COUNT

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(5)

    # Sockets from which we expect to read
    inputs = [server]

    # Sockets to which we expect to write
    outputs = []

    zsl = Zope2ServerLibrary()
    zsl.start_zope_server(zope_layer_dotted_name)
    print '=' * COUNT
    print "Zope 2 server started"
    print "layer : {0}".format(zope_layer_dotted_name)
    print '=' * COUNT

    try:

        while inputs:

            # Wait for at least one of the sockets to be ready for processing
            readable, writable, exceptional = select.select(
                    inputs, outputs, inputs)
    finally:
        print
        print "Stopping Zope 2 server"
        print '=' * COUNT
        zsl.stop_zope_server()
        print '=' * COUNT
        print "Zope 2 server stopped"
        print '=' * COUNT


def server():
    import sys
    try:
        start(sys.argv[1])
    except KeyboardInterrupt:
        pass
