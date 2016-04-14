#!/usr/bin/python2.7

import pygame
import sys

pygame.init()

size = width, height = 640, 640
n = 8
sq_width = width / n
sq_height = height / n
colors = [(255, 0, 0), (0, 0, 0)]

print sq_width, sq_height

surface = pygame.display.set_mode(size)

# load image
launcher = pygame.image.load("img/launcher-left.png")

clock = pygame.time.Clock()

while True:
    # event
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            click_pos = ev.dict['pos']
            print click_pos

    # main drawing
    for row in range(n):           # Draw each row of the board.
        c_indx = row % 2           # Change starting color on each row
        for col in range(n):       # Run through cols drawing squares
            the_square = (col*sq_width, row*sq_height, sq_width, sq_height)
            surface.fill(colors[c_indx], the_square)
            # now flip the color index for the next square
            c_indx = (c_indx + 1) % 2
    # load images
    for i in range(8):
        surface.blit(launcher, (0, 80 * i))
    pygame.display.flip()
    clock.tick(40)
