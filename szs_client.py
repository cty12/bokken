#!/usr/bin/python2.7

from Mastermind import *
from szs_server import SzsServer
import pygame

def main():
    global client, server
    client = MastermindClientTCP(5.0, 10.0)
    ip = "localhost"
    port = 6317

    try:
        client.connect(ip, port)
    except MastermindError:
        print "server connection error! "
        return

    data = dict()
    data['col'] = 24
    data['row'] = 42
    client.send(data)
    client.disconnect()

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc() 
     
