#!/usr/bin/python2.7

from Mastermind import *
from szs_server import SzsServer
import pygame
from chessboard import ChessBoard, Manipulate
from icons import icons

def set_up():
    global cb, sq
    # set up chess board
    cb = ChessBoard(8, 8)
    # the size of a square in px
    sq = 80

    # define colors
    red = (255, 0, 0)
    black = (0, 0, 0)
    global cb_color, surface, launcher_up, farmer, clock
    cb_color = [red, black]
    surface = pygame.display.set_mode([sq * x for x in cb.size()])
    launcher_up = pygame.image.load(icons['launcher-up'])
    farmer = pygame.image.load(icons['farmer'])
    clock = pygame.time.Clock()

# def draw_board():

def main():
    # init
    pygame.init()
    set_up()

    # establishing connections
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
    main()
