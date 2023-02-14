import numpy as np
import pygame as pg
import copy


# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# epsilon value (size of 𝜀-cell)
EPSILON = 5
BORDER = 1

class Grid_Map:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Coverage")
        self.WIN = None

        self.map = None
        self.row_count = 0
        self.col_count = 0

        self.vehicle_img = pg.Rect(BORDER, BORDER, EPSILON - BORDER, EPSILON - BORDER)
        self.start_pos = (0, 0)
        self.vehicle_path = [(0, 0)]

    def read_map(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            self.col_count, self.row_count = [int(i) for i in f.readline().strip().split()]
            # print(self.col_count,self.row_count)
            display_size = [EPSILON * self.col_count, EPSILON * self.row_count]
            # print(type(display_size))
            self.WIN = pg.display.set_mode(display_size)

            map = []

            for idx, line in enumerate(f):
                line =[int(value) for value in line.strip().split()]
                # print(line)
                map.append(line)

            if len(map) == 0:
                map = np.zeros((self.row_count, self.col_count), dtype=int)

            self.map = map

        return copy.deepcopy(map)

    def edit_map(self):
        done = False
        draw_obstacle = False
        prev_cell = None


        while done == False:
            pos = pg.mouse.get_pos()
            col = pos[0] // EPSILON
            row = pos[1] // EPSILON

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pressed = pg.mouse.get_pressed()
                    if mouse_pressed[0]: # left mouse click: obstacle
                        draw_obstacle = True
                    if mouse_pressed[2]: # right mouse click: starting position
                        self.start_pos = (row, col)
                        self.vehicle_path = [(row, col)]
                        # self.update_vehicle_pos(self.start_pos)
                        self.map[row][col] = 0

                elif event.type == pg.MOUSEBUTTONUP:
                    draw_obstacle = False
                    prev_cell = None

            # check boolean flag to allow holding left click to draw
            if draw_obstacle:
                if (prev_cell != (row, col)):
                    prev_cell = (row, col)
                    if self.map[row][col] == 0 and self.start_pos != (row, col):
                        self.map[row][col] = 1
                    else:
                        self.map[row][col] = 0

            # pygame draw
            self.draw_map()
            pg.draw.rect(self.WIN, RED, self.vehicle_img)
            pg.display.flip()

        return copy.deepcopy(self.map), self.start_pos

    def save_map(self, output_file):
        map = self.map
        with open(output_file, "w", encoding="utf-8") as f:
            col_count, row_count = len(map[0]), len(map)
            f.write(str(col_count) + ' ' + str(row_count) + '\n')
            for row in map:
                line = [str(value) for value in row]
                line = " ".join(line)
                f.write(line +'\n')
            print("Save map done!")

    def draw(self):
        self.draw_map()
        self.draw_path()
        pg.draw.rect(self.WIN, RED, self.vehicle_img)
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
                if self.map[row][col] == 1: # dùng chung cho map.txt
                    color = BLACK

                elif self.map[row][col] == 'f':
                    color = YELLOW

                elif self.map[row][col] == 'e':
                    color = GREEN

                pg.draw.rect(self.WIN,color,
                            [EPSILON * col + BORDER,EPSILON * row + BORDER,
                            EPSILON - BORDER,EPSILON - BORDER])

    def draw_path(self):
        current_pos = self.vehicle_path[-1]
        self.update_vehicle_pos(current_pos)

        point_list = [(EPSILON * pos[1] + EPSILON // 2, EPSILON * pos[0] + EPSILON // 2) for pos in self.vehicle_path]
        if len(point_list) > 1:
            pg.draw.lines(self.WIN, RED, False, point_list, width=2)

    def update_vehicle_pos(self, pos):
        self.vehicle_img.x = EPSILON * pos[1] + BORDER
        self.vehicle_img.y = EPSILON * pos[0] + BORDER

    def move_to(self, pos):
        self.vehicle_path.append(pos)

    def task(self, pos):
        self.map[pos[0]][pos[1]] = 'e'

def main():
    ui = Grid_Map()
    ui.read_map('map/map_3.txt')
    ui.edit_map()



    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        ui.draw()

    pg.quit()

if __name__ == "__main__":
    main()
