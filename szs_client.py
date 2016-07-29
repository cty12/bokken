#!/usr/bin/env python

import argparse
from Mastermind import *
from szs_server import SzsServer
import pygame
from chessboard import ChessBoard, Manipulate
from icons import icons, launchers

def set_up():
    global cb, sq
    # load the map and set up the chessboard
    cb = ChessBoard("maps/sample.map")
    # the size of a square in px
    # TODO add config
    sq = 80

    # define colors
    red = (255, 0, 0)
    black = (0, 0, 0)
    global cb_color, surface
    global launcher_up, launcher_down, launcher_left, launcher_right, \
        block, farmer, keymaker
    global clock
    cb_color = [red, black]
    surface = pygame.display.set_mode([sq * x for x in cb.size()])
    # load icons here
    launcher_up = pygame.image.load(icons['launcher-up'])
    launcher_down = pygame.image.load(icons['launcher-down'])
    launcher_left = pygame.image.load(icons['launcher-left'])
    launcher_right = pygame.image.load(icons['launcher-right'])
    block = pygame.image.load(icons['block'])
    farmer = pygame.image.load(icons['farmer'])
    keymaker = pygame.image.load(icons['keymaker'])
    clock = pygame.time.Clock()

def construct_msg(head='heartbeat', body=None):
    # may add a timestamp here
    return (head, body)

# the all-in-one coordinate mapper for launchers
def cb_update_handler(pos_col, pos_row):
    pos_icon = cb.get(pos_col, pos_row)
    if pos_icon not in launchers:
        raise ValueError
    ret_col, ret_row = pos_col, pos_row
    if pos_icon == 'launcher-up':
        while (ret_row + 1) < cb.size()[1] and \
                cb.get(ret_col, ret_row + 1) == '':
            ret_row += 1
    elif pos_icon == 'launcher-down':
        while (ret_row - 1) >= 0 and \
                cb.get(ret_col, ret_row - 1) == '':
            ret_row -= 1
    elif pos_icon == 'launcher-left':
        while (ret_col + 1) < cb.size()[0] and \
                cb.get(ret_col + 1, ret_row) == '':
            ret_col += 1
    elif pos_icon == 'launcher-right':
        while (ret_col - 1) >= 0 and \
                cb.get(ret_col - 1, ret_row) == '':
            ret_col -= 1

    if (ret_col, ret_row) == (pos_col, pos_row):
        raise ValueError
    return ret_col, ret_row


def parse_args():
    parser = argparse.ArgumentParser(description='SZS client. ')
    parser.add_argument('--ip', type=str, default='127.0.0.1', dest='ipaddr', help='the IP address of the server')
    parser.add_argument('--port', type=int, default=6317, dest='port', help='the port configuration of the server')
    parser.add_argument('--icon', type=str, default='farmer', dest='icon', help='the icon to use')
    args = parser.parse_args()
    return (args.ipaddr, args.port, args.icon)

def main(ipaddr, port, player_icon):
    # init
    pygame.init()
    set_up()

    # establishing connections
    global client, server
    client = MastermindClientTCP(5.0, 10.0)

    try:
        client.connect(ipaddr, port)
    except MastermindError:
        print "server connection error! "
        return

    # TODO initial map consensus

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
                try:
                    mapped_col, mapped_row = cb_update_handler(pos_col, pos_row)
                except ValueError:
                    print 'invalid pos'
                    continue
                # for debug
                print 'col: ', pos_col, 'row: ', pos_row
                print 'mapped col: ', mapped_col, 'row: ', mapped_row
                # send chessboard update message to server
                client.send(construct_msg('update', {'col': mapped_col, 'row': mapped_row, 'icon': player_icon}))

        # receive from the server
        reply = client.receive(False)
        if reply is not None:
            print 'reply col: ', reply['col'], 'row: ', reply['row']
            cb.update(Manipulate(reply['col'], reply['row'], reply['icon'], None))
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
                elif icon == 'block':
                    surface.blit(block, (sq * col, sq * row))
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    ipaddr, port, icon = parse_args()
    # for debug
    print '**CONFIG**: ', ipaddr, port, icon
    main(ipaddr, port, icon)
