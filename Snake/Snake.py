
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 20
    w = 500
    def __init__(self,start, dirnx=1, dirny=0,color=(0,255,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):

        self.dirnx = dirnx
        self.dirny = dirny
        self.pos(self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


    def draw(self, surface, eyes=False):

        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface,(0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface,(0,0,0), circleMiddle2, radius)



class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0  # x direction
        self.dirny = 1  # y direction


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
                    c.move(c.dirnx, c.dirny)  # if you haven't hit anything, just keep going


    def reset(self, pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):

        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



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


def randomSnack(rows, items):
    pass

def messageBox(subject, content):
    pass

def drawSurface(window: object, size, rows, snake):
    pygame.display.set_caption('Snake by Alec')

    window.fill((0,0,0))

    snake.draw(window)

    drawGrid(size, rows, window)

    pygame.display.flip()

def main():
    size = 500
    rows = 20
    win = pygame.display.set_mode((size,size))
    snake = Snake((0,255,0), (10,10))
    clock = pygame.time.Clock()
    # game loop
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        drawSurface(win, size, rows, snake)

        # for loop through the event queue
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == pygame.QUIT:
                flag = False



if __name__ == "__main__":
    main()