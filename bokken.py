#!/usr/bin/python2.7

import pygame
import sys

pygame.init()

size = width, height = 640, 640
n = 8
sq_width = width / n
sq_height = height / n
colors = [(255, 0, 0), (0, 0, 0)]
objects = [['' for x in range(n)] for x in range(n)]

print sq_width, sq_height

surface = pygame.display.set_mode(size)

# load image
launcher = pygame.image.load("img/launcher-up.png")
farmer = pygame.image.load("img/farmer-icon.png")

clock = pygame.time.Clock()

# set up launcher positions
for col in range(n):
    objects[col][0] = 'launcher-up'

def get_row(col):
    for row in range(1, n):
        if objects[col][row] != '':
            return (row - 1)
    return (n - 1)

while True:
    click_pos = None
    # event
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            click_pos = ev.dict['pos']
            print click_pos
            icon_col = int(click_pos[0]) / int(width / n)
            icon_row = int(click_pos[1]) / int(height / n)
            # for debug
            print icon_col, icon_row
            print get_row(icon_col), '\n'
            objects[icon_col][get_row(icon_col)] = 'farmer'

    # main drawing
    for row in range(n):           # Draw each row of the board.
        c_indx = row % 2           # Change starting color on each row
        for col in range(n):       # Run through cols drawing squares
            the_square = (col*sq_width, row*sq_height, sq_width, sq_height)
            surface.fill(colors[c_indx], the_square)
            # now flip the color index for the next square
            c_indx = (c_indx + 1) % 2

    # load icons
    for col in range(n):
        for row in range(n):
            if objects[col][row] == 'farmer':
                surface.blit(farmer, (sq_width * col, sq_height * row))
            elif objects[col][row] == 'launcher-up':
                surface.blit(launcher, (sq_width * col, sq_height * row))

    pygame.display.flip()
    clock.tick(40)
