#!/usr/bin/python2.7

from Mastermind import *
from szs_server import SzsServer
import pygame
from chessboard import ChessBoard, Manipulate
from icons import icons

def set_up():
    global cb, sq
    # set up chess board
    cb = ChessBoard(8, 10)
    # the size of a square in px
    sq = 80

    # define colors
    red = (255, 0, 0)
    black = (0, 0, 0)
    global cb_color, surface, launcher_up, farmer, clock
    cb_color = [red, black]
    surface = pygame.display.set_mode([sq * x for x in cb.size()])
    # load icons here
    launcher_up = pygame.image.load(icons['launcher-up'])
    launcher_down = pygame.image.load(icons['launcher-down'])
    launcher_left = pygame.image.load(icons['launcher-left'])
    launcher_right = pygame.image.load(icons['launcher-right'])
    farmer = pygame.image.load(icons['farmer'])
    keymaker = pygame.image.load(icons['keymaker'])
    clock = pygame.time.Clock()

def construct_msg(head='heartbeat', body=None):
    # may add a timestamp here
    return (head, body)

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

    # main ui loop
    while True:
        # handle event
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                client.disconnect()
                print 'client disconnected! '
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.dict['pos']
                pos_col = int(pos[0]) / int(sq)
                pos_row = int(pos[1]) / int(sq)
                print 'col: ', pos_col, 'row: ', pos_row
                # send chessboard update message to server
                client.send(construct_msg('update', {'col': pos_col, 'row': pos_row}))

        # receive from the server
        reply = client.receive(False)
        if reply is not None:
            print 'reply col: ', reply['col'], 'row: ', reply['row']
        # send keep alive message to the server
        client.send(construct_msg('heartbeat'))

        # draw chessboard
        for col in range(cb.size()[0]):
            flip_indx = col % 2
            for row in range(cb.size()[1]):
                # fill the square
                the_square = (col * sq, row * sq, sq, sq)
                surface.fill(cb_color[flip_indx], the_square)
                flip_indx = (flip_indx + 1) % 2
                # load icons
                icon = cb.get(col=col, row=row)
                if icon == 'farmer':
                    surface.blit(farmer, (sq * col, sq * row))
                elif icon == 'keymaker':
                    surface.blit(keymaker, (sq * col, sq * row))
                elif icon == 'launcher-up':
                    surface.blit(launcher_up, (sq * col, sq * row))
                elif icon == 'launcher-down':
                    surface.blit(launcher_down, (sq * col, sq * row))
                elif icon == 'launcher-left':
                    surface.blit(launcher_left, (sq * col, sq * row))
                elif icon == 'launcher-right':
                    surface.blit(launcher_right, (sq * col, sq * row))
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
