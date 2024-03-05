
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
    def __init__(self, color, pos):
        pass
    def move(self):
        pass
    def reset(self, pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):
        pass

def drawGrid(w, rows, surface):
    pass

def redrawWindow(surface):
    surface.fill((0,0,0))
    drawGrid(surface)
    pygame.display.update()
    pass

def randomSnack(rows, items):
    pass

def messageBox(subject, content):
    pass

def main():
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width,height))
    s = Snake((0,255,0),(10,10))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)  # game runs at max 10 frames per second
        redrawWindow(win)
    pass
