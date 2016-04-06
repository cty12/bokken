#!/usr/bin/python2.7

import pygame
import sys

pygame.init()

size = width, height = 640, 640
black = 0, 0, 0

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(black)
    clock.tick(40)
