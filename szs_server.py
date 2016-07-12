#!/usr/bin/python2.7

from Mastermind import *

import threading

class SzsServer(MastermindServerTCP):
    def __init__(self):
        # server refresh; conn refresh; timeout
        MastermindServerTCP.__init__(self, 0.5,0.5,10.0)

    def callback_connect(self):
        return super(SzsServer, self).callback_connect()

    def callback_disconnect(self):
        return super(SzsServer, self).callback_disconnect()

    def callback_connect_client(self, connection_object):
        return super(SzsServer, self).callback_connect_client(connection_object)

    def callback_disconnect_client(self, connection_object):
        return super(SzsServer, self).callback_disconnect_client(connection_object)

    def callback_client_receive(self, connection_object):
        return super(SzsServer, self).callback_client_receive(connection_object)

    def callback_client_handle(self, connection_object, data):
        print 'col: ', data['col'], 'row: ', data['row']
        self.callback_client_send(connection_object, "received")

    def callback_client_send(self, connection_object, data, compression=None):
        return super(SzsServer, self).callback_client_send(connection_object, data, compression)

if __name__ == '__main__':
    server = SzsServer()
    ip = "localhost"
    port = 6317
    # tcp connect
    server.connect(ip, port)
    try:
        server.accepting_allow_wait_forever()
    except:
        pass
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()
