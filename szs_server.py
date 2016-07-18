#!/usr/bin/python2.7

from Mastermind import *

import threading

class Connections:
    def __init__(self):
        self._all_conn = dict()
        self._conn_serial = 0

    def insert(self, conn):
        self._all_conn[self._conn_serial] = conn
        self._conn_serial += 1

    def remove(self, conn):
        for key, value in self._all_conn.iteritems():
            if value == conn:
                self._all_conn.pop(key)
                break

    def get_conn_objs(self):
        return self._all_conn.values()

    def get_conn_cnt(self):
        return len(self._all_conn.keys())

class SzsServer(MastermindServerTCP):

    def __init__(self):
        # server refresh; conn refresh; timeout
        MastermindServerTCP.__init__(self, 0.5,0.5,10.0)
        # define the collection of all client connections
        self._connections = Connections()

    def callback_connect(self):
        return super(SzsServer, self).callback_connect()

    def callback_disconnect(self):
        return super(SzsServer, self).callback_disconnect()

    def callback_connect_client(self, connection_object):
        # for debug
        print 'incoming client connection'
        self._connections.insert(connection_object)
        print 'number of connections: ', self._connections.get_conn_cnt()
        return super(SzsServer, self).callback_connect_client(connection_object)

    def callback_disconnect_client(self, connection_object):
        # for debug
        print 'client disconnected'
        self._connections.remove(connection_object)
        print 'number of connections: ', self._connections.get_conn_cnt()
        return super(SzsServer, self).callback_disconnect_client(connection_object)

    def callback_client_receive(self, connection_object):
        return super(SzsServer, self).callback_client_receive(connection_object)

    def callback_client_handle(self, connection_object, data):
        if data[0] == 'heartbeat':
            # handle heartbeat message
            pass
        elif data[0] == 'update':
            # update chessboard
            print 'col: ', data[1]['col'], 'row: ', data[1]['row'], 'icon: ', data[1]['icon']
            for conn in self._connections.get_conn_objs():
                self.callback_client_send(conn, data[1])

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
