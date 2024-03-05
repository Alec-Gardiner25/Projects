
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 0
    w = 0
    def __int__(self,start, dirnx=1, dirny=0,color=(255,0,0)):
        pass
    def move(self, dirnx, dirny):
        pass
    def draw(self, surface, eyes=False):
        pass
class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0  # x direction
        self.dirny = 1  # y direction

        pass
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                # border checking, if the snake hits any of the walls, it appears on the other side of the screen
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)

                else:
                    c.move(c.dirnx, c.dirny)


    def reset(self, pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):
        pass

def drawGrid(w, rows, surface):
    sizeBtwn = w//rows

    x = 0
    y = 0

    for i in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        # Draw two lines for every loop
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))  # Draws vertical line, moves horizontally
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))  # Draws horizontal line, moves vertically

    pass

def redrawWindow(surface):
    global rows, width
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, items):
    pass

def messageBox(subject, content):
    pass

def main():
    global width, rows
    width = 500
    rows = 20
    win = pygame.display.set_mode((width,width))
    snake = Snake((0,255,0),(10,10))
    clock = pygame.time.Clock()

    while True:

        pygame.time.delay(50)
        clock.tick(10)  # game runs at max 10 frames per second
        redrawWindow(win)
    pass
