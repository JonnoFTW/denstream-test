#!/usr/bin/env python
from __future__ import print_function
from ljtserver.analysis import DenStream, DenPoint
import pygame
import sys
import random
import numpy as np
import random_color
import math
pygame.init()

size = width, height = 960, 960
FPS = 100
fpsClock = pygame.time.Clock()
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
paused = False
jiggle = 0.001


class Ball(object):
    COLORS = []

    def __init__(self, center):
        self.points = np.random.normal(center, 30, (50, 2))
        c = random_color.generate_new_color(self.COLORS)
        self.color = map(lambda val: int(255.0*val), c)
        self.velocity = [2, random.random() * 2 * math.pi]  # magnitude, radians


def show_point(x, y, color):
    pygame.draw.circle(screen, color, map(int, (x, y)), 3)

balls = [Ball(100), Ball(700), Ball(500), Ball(200)]

from collections import namedtuple

trips = []
for i, arr in enumerate(np.concatenate([b.points for b in balls])):
    trips.append(DenPoint(i, 0, arr))
d = DenStream(40, 10, trips)
try:
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONUP:
                paused = not paused
        if not paused:
            screen.fill(black)
            for ball in balls:
                ball.points += (ball.velocity[0] * math.cos(ball.velocity[1]),
                                ball.velocity[0] * math.sin(ball.velocity[1]))
                # give them a bit of ijggle
                ball.points *= np.random.uniform(1 - jiggle, 1 + jiggle, ball.points.shape)
                for x, y in ball.points:
                    show_point(x, y, ball.color)
                means = np.mean(ball.points, 0)
                if not (0 < means[1] < height) or not (0 < means[0] < width):
                    ball.velocity[1] -= random.uniform(3*math.pi / 4, 5 * math.pi/4)
            for cluster in d.p_micro_clusters:
                pygame.draw.circle(screen, (255,255,255), cluster.center(), cluster.radius(), 2)
        pygame.display.flip()
        fpsClock.tick(FPS)
except (KeyboardInterrupt, e):
    print("Bye")
    sys.exit()
