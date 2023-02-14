import numpy as np
import pygame as pg
import copy
from const import *

class Grid_Map:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Project1")
        self.WIN = None
        self.map = None
        self.row_count = 0
        self.col_count = 0

    def read_map(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            self.col_count, self.row_count = [int(i) for i in f.readline().strip().split()]
            display_size = [EPSILON * self.col_count, EPSILON * self.row_count]
            self.WIN = pg.display.set_mode(display_size)
            map = []
            for idx, line in enumerate(f):
                line = [int(value) for value in line.strip().split()]
                map.append(line)
            if len(map) == 0:
                map = np.zeros((self.row_count, self.col_count), dtype=int)
            self.map = map
        return copy.deepcopy(map)

    def draw(self):
        self.draw_map()
        pg.display.flip()

    def draw_map(self):
        '''
        map (ui):
            0: allowed cell
            1: obstacle cell
        '''
        self.WIN.fill(BLACK)
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                color = WHITE
                if self.map[row][col] == 1:  # dùng chung cho map.txt
                    color = BLACK
                if self.map[row][col] == 2:
                    color = RED
                pg.draw.rect(self.WIN,color,[EPSILON * col + BORDER,EPSILON * row + BORDER,EPSILON - BORDER,EPSILON - BORDER])



    def critical_point(self):
        count=0
        for col in range(len(self.map)):
            for row in range(len(self.map[0])):
                if self.map[row][col]==1:
                    count+=1
                    if count == 1:
                        x=row
                elif count!=0:
                    tmp=x+int((count-1)/2)
                    self.map[tmp][col]=2
                    count=0
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col]==2:
                    for i in range(col+1,len(self.map[0])-1,1):
                        if self.map[row][i] == 2 and self.map[row][i+1] == 2:
                            self.map[row][i] = 1
                        else: break



def main():
    ui = Grid_Map()
    ui.read_map('map/map_7.txt')
    ui.critical_point()
    print(ui.read_map('map/map_7.txt'))

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        ui.draw()
    pg.quit()

if __name__ == "__main__":
    main()
