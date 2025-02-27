import math
import random
from turtle import width
import pygame
import tkinter as tk
from tkinter import messagebox

from sqlalchemy import false
from sympy import S, root

class cube(object):
    rows = 10
    w = 500
    def __init__(self,start,dirnx = 1, dirny =0, color = (0,0,255)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    def draw(self,surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class blue(object):
    body = []
    turns = {}
    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        
    def move(self, move):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
            
            
            if move == 'left':
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
            elif move == 'right':
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
            elif move == 'down':
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
            elif move == 'up':
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p) 
        
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    def path(self, emeraldcoords):
        while self.head.pos != emeraldcoords:
            if self.head.pos > emeraldcoords:
                pass
            elif self.head.pos < emeraldcoords:
                pass
        
    def draw(self,surface):
        #makes the agent appear
        for i, c in enumerate(self.body):
            c.draw(surface, True)
    
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    
    x = 0
    y = 0
    
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x,0),(x,w))
        pygame.draw.line(surface, (255, 255, 255), (0, y),(w, y))

def redrawWindow(surface):
    global rows, width, b, emerald, pits
    surface.fill((0,0,0))
    b.draw(surface)
    emerald.draw(surface)
    for w in pits:
        drawwall = cube(w, color = (255,0,0))
        drawwall.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomEmerald(rows, item, wall):
    
    positions = item.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0 or (x,y) in wall:
            continue
        else:
            break
    return(x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global rows, width, b, emerald, pits
    print('please type corn or cent to choose where to start')
    start = str(input())
    if start == 'cent':
        scoord = (4,4)
    elif start == 'corn':
        scoord = (0,0)
    width = 500
    rows = 10
    win = pygame.display.set_mode((width, width))
    pits = [(1,1),(1,3),(1,6),(1,8),(3,1),(3,3),(3,6),(3,8),(6,1),(6,3),(6,6),(6,8),(8,1),(8,3),(8,6),(8,8)] 
    b = blue((0,0,255), scoord)
    emerald = cube(randomEmerald(rows, b, pits), color = (0,255,0))
    flag = True
    clock = pygame.time.Clock()
    score = 0
    while flag:
        pygame.time.delay(1)
        clock.tick(30)
        print('blue position: ' + str(b.body[0].pos))
        print('emerald position: ' + str(emerald.pos))
        if b.body[0].pos[0] > emerald.pos[0]:
            if (b.body[0].pos[0] - 1, b.body[0].pos[1]) in pits or ((b.body[0].pos[0] - 1, b.body[0].pos[1]) != emerald.pos  and b.body[0].pos[0] - 1 == emerald.pos[0] and ((b.body[0].pos[0] - 1, b.body[0].pos[1]) in pits or (b.body[0].pos[0] - 1, b.body[0].pos[1] - 1) in pits or (b.body[0].pos[0] - 1, b.body[0].pos[1] + 1) in pits)):
                if b.body[0].pos[1] > emerald.pos[1]:
                    b.move('down')
                    print('down')
                elif b.body[0].pos[1] < emerald.pos[1]:
                    b.move('up')
                    print('up')
                elif b.body[0].pos[1] == emerald.pos[1]:
                    if b.body[0].pos[1] <= 4:
                        b.move('up')
                        print('up')
                    else:
                        b.move('down')
                        print('down')
            else:
                b.move('left')
                print('left')
        elif b.body[0].pos[0] < emerald.pos[0]:
            if (b.body[0].pos[0] + 1, b.body[0].pos[1]) in pits or ((b.body[0].pos[0] + 1, b.body[0].pos[1]) != emerald.pos  and b.body[0].pos[0] + 1 == emerald.pos[0] and ((b.body[0].pos[0] + 1, b.body[0].pos[1]) in pits or (b.body[0].pos[0] + 1, b.body[0].pos[1] - 1) in pits or (b.body[0].pos[0] + 1, b.body[0].pos[1] + 1) in pits)):
                if b.body[0].pos[1] > emerald.pos[1]:
                    b.move('down')
                    print('down')
                elif b.body[0].pos[1] < emerald.pos[1]:
                    b.move('up')
                    print('up')
                elif b.body[0].pos[1] == emerald.pos[1]:
                    if b.body[0].pos[1] <= 4:
                        b.move('up')
                        print('up')
                    else:
                        b.move('down')
                        print('down')
            else:
                b.move('right')
                print('right')
        elif b.body[0].pos[1] > emerald.pos[1]:
            if (b.body[0].pos[0], b.body[0].pos[1] - 1) in pits:
                if b.body[0].pos[0] <= 4:
                    b.move('left')
                    print('left')
                else:
                    b.move('right')
                    print('right')
            else:
                b.move('down')
                print('down')
        elif b.body[0].pos[1] < emerald.pos[1]:
            if (b.body[0].pos[0], b.body[0].pos[1] - 1) in pits:
                if b.body[0].pos[0] <= 4:
                    b.move('left')
                    print('left')
                else:
                    b.move('right')
                    print('right')
            else:
                b.move('up')
                print('up')
                
        if b.body[0].pos == emerald.pos:
                emerald = cube(randomEmerald(rows, b, pits), color = (0,255,0))
                score = score + 1
                
        if b.body[0].pos in pits:
            print('Score', score)
            message_box('You Lost', 'Play Again')
            b.reset(scoord)
        if score == 10:
            redrawWindow(win)
            print('Score', score)
            message_box('Win', 'Play Again')
            score = 0
            b.reset(scoord)
        redrawWindow(win)
    pass
main()

