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

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # main drawing
    for row in range(n):           # Draw each row of the board.
        c_indx = row % 2           # Change starting color on each row
        for col in range(n):       # Run through cols drawing squares
            the_square = (col*sq_width, row*sq_height, sq_width, sq_height)
            surface.fill(colors[c_indx], the_square)
            # now flip the color index for the next square
            c_indx = (c_indx + 1) % 2
    pygame.display.flip()
    clock.tick(40)
