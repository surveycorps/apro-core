#!/usr/bin/env python

import pygame
import sys
import socket
import select
import time
 
#host = '192.168.7.2'
host = '10.0.0.1'
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

# connect to remote host
try :
    s.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()

x = y = 0
running = 1
screen = pygame.display.set_mode((640, 400))
msg = ['0', '0', '0', '0', '0', '0', '0']

while 1:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    #elif event.type == pygame.MOUSEMOTION:
    #    print "mouse at (%d, %d)" % event.pos
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            msg[0] = '1'
        if event.key == pygame.K_DOWN:
            msg[1] = '1'
        if event.key == pygame.K_LEFT:
            msg[2] = '1'
        if event.key == pygame.K_RIGHT:
            msg[3] = '1'
    elif event.type == pygame.KEYUP:            # check for key releases
        if event.key == pygame.K_UP:        # left arrow turns left
            msg[0] = '0'
        if event.key == pygame.K_DOWN:     # right arrow turns right
            msg[1] = '0'
        if event.key == pygame.K_LEFT:        # up arrow goes up
            msg[2] = '0'
        if event.key == pygame.K_RIGHT:     # down arrow goes down
            msg[3] = '0'

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2: # Middle Click
            msg[4] = '1'
        if event.button == 4: # Scroll Down
            msg[5] = '1'
        if event.button == 5: # Scroll Up
            msg[6] = '1'
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 2:
            msg[4] = '0'
        if event.button == 4:
            msg[5] = '0'
        if event.button == 5:
            msg[6] = '0'


    screen.fill((0, 0, 0))
    pygame.display.flip()
    message = ' '.join(msg)
    print message
    time.sleep(.1)
    s.send(message)
