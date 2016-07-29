#!/usr/bin/python2.7

from Mastermind import *

import argparse
import threading

class Connections:
    def __init__(self):
        # key: the connection object associated with a client
        # value: a serial number
        self._all_conn = dict()
        self._conn_serial = 0

    def insert(self, conn):
        self._all_conn[conn] = self._conn_serial
        self._conn_serial += 1

    def remove(self, conn):
        self._all_conn.pop(conn)

    # return a list of valid serial numbers
    def get_index(self):
        return self._all_conn.values()

    def get_conn_objs(self):
        return self._all_conn.keys()

    # return the number of valid client connections
    def get_conn_cnt(self):
        return len(self._all_conn.keys())

    def get_conn_serial(self):
        return self._conn_serial

    def conn_to_serial(self, conn):
        return self._all_conn[conn]

    def reset(self):
        self._all_conn = {}
        self._conn_serial = 0

class SzsServer(MastermindServerTCP):

    def __init__(self):
        # server refresh; conn refresh; timeout
        MastermindServerTCP.__init__(self, 0.5,0.5,10.0)
        # define the collection of all client connections
        self._connections = Connections()
        self._update_idx = 0
        # TODO add map consensus

    # reset server settings
    def reset(self):
        # for debug
        print 'server settings reset'
        self._connections.reset()
        self._update_idx = 0

    # update player index
    def _update_player_index(self):
        # check whether there is no active client connection
        # avoid infinite loop
        if self._connections.get_conn_cnt() == 0:
            return
        while True:
            self._update_idx = (self._update_idx + 1) % self._connections.get_conn_serial()
            if self._update_idx in self._connections.get_index():
                break
        # for debug
        print 'next player updated to', self._update_idx

    def callback_connect(self):
        return super(SzsServer, self).callback_connect()

    def callback_disconnect(self):
        return super(SzsServer, self).callback_disconnect()

    def callback_connect_client(self, connection_object):
        # TODO when a new client connects,
        # there should be a force chessboard sync
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
        # update the player index
        self._update_player_index()
        # if all clients are disconnected
        if self._connections.get_conn_cnt() == 0:
            # reset server settings
            self.reset()
        return super(SzsServer, self).callback_disconnect_client(connection_object)

    def callback_client_receive(self, connection_object):
        return super(SzsServer, self).callback_client_receive(connection_object)

    def callback_client_handle(self, connection_object, data):
        if data[0] == 'heartbeat':
            # handle heartbeat message
            pass
        elif data[0] == 'update':
            # update chessboard
            # decide whether is the player's round
            client_serial = self._connections.conn_to_serial(connection_object)
            if client_serial == self._update_idx:
                print 'col: ', data[1]['col'], 'row: ', data[1]['row'], 'icon: ', data[1]['icon']
                # do broadcast
                for conn in self._connections.get_conn_objs():
                    self.callback_client_send(conn, data[1])
                # update the player index
                self._update_player_index()
            else:
                print 'It\'s', self._update_idx, 'turn, not', client_serial

    def callback_client_send(self, connection_object, data, compression=None):
        return super(SzsServer, self).callback_client_send(connection_object, data, compression)

def parse_args():
    parser = argparse.ArgumentParser(description='SZS server. ')
    parser.add_argument('--ip', type=str, default='127.0.0.1', dest='ipaddr', help='configuring the IP address of the network interface to use')
    parser.add_argument('--port', type=int, default=6317, dest='port', help='configuring the port')
    args = parser.parse_args()
    return (args.ipaddr, args.port)

if __name__ == '__main__':
    server = SzsServer()
    # parse args
    ip, port = parse_args()
    print 'server config: ip=', ip, 'port=', port
    # tcp connect
    server.connect(ip, port)
    try:
        server.accepting_allow_wait_forever()
    except:
        pass
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()
