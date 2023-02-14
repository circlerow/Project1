# Reference : https://github.com/WJTung/GA-TSPCPP/blob/master/Decomposition.py
import numpy as np
import copy
from const import *
import pygame as pg

fps=100
class Region:
    def __init__(self, id):
        self.region_id = id
        self.min_y, self.max_y = None, None
        self.cell_list = list()
        self.center = (None, None)


class Graph:
    def __init__(self):
        self.edges = dict()
        self.WIN = None
        self.map = None
        self.row_count = 0
        self.col_count = 0

    def neighbors(self, node):
        return self.edges[node]

    def read_map(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            self.col_count, self.row_count = [int(i) for i in f.readline().strip().split()]
            display_size = [EPSILON * self.col_count, EPSILON * self.row_count+30]
            self.WIN = pg.display.set_mode(display_size)
            pg.display.set_caption("PJ1")
            map = []
            for idx, line in enumerate(f):
                line = [int(value) for value in line.strip().split()]
                map.append(line)
            if len(map) == 0:
                map = np.zeros((self.row_count, self.col_count), dtype=int)
                self.map = np.array(map, dtype=object)
        return copy.deepcopy(map)

    def draw(self, decomposed):
        self.draw_map(decomposed)
        pg.display.flip()

    def draw_map(self, decomposed):
        '''
        map (ui):
            0: allowed cell
            1: obstacle cell
        '''
        self.WIN.fill(BLACK)
        for row in range(len(decomposed)):
            for col in range(len(decomposed[0])):
                color = BLACK
                if decomposed[row][col] == 1:  # dùng chung cho map.txt
                    color = WHITE
                if decomposed[row][col] == 2:
                    color = RED
                if decomposed[row][col] == 3:
                    color = YELLOW
                if decomposed[row][col] == 4:
                    color = GREEN
                if decomposed[row][col] == 5:
                    color = BLUE
                if decomposed[row][col] == 6:
                    color = PURPLE
                if decomposed[row][col] == 7:
                    color = ORANGE
                if decomposed[row][col] == 8:
                    color = SILVER
                if decomposed[row][col] == 9:
                    color = CYAN
                if decomposed[row][col] == 10:
                    color = OLIVE
                if decomposed[row][col] == 11:
                    color = DARKPURPLE
                if decomposed[row][col] == 12:
                    color = DARKGREEN
                if decomposed[row][col] == 13:
                    color = TEAL
                if decomposed[row][col] == 14:
                    color = NAVY
                if decomposed[row][col] == 15:
                    color = MAROON
                if decomposed[row][col] == 16:
                    color = GRAY
                if decomposed[row][col] == 17:
                    color = FIREBRICK
                if decomposed[row][col] == 18:
                    color = GOLD
                if decomposed[row][col] == 19:
                    color = LAWNGREEN
                if decomposed[row][col] == 20:
                    color = TURQUOISE
                if decomposed[row][col] == 21:
                    color = BLUEVIOLET
                if decomposed[row][col] == 22:
                    color = DEEPPINK
                if decomposed[row][col] == 23:
                    color = CHOCOLATE
                if decomposed[row][col] == 24:
                    color = LIGHTSTEELBLUE
                if decomposed[row][col] == 25:
                    color = LIGHTGRAY
                if decomposed[row][col] == 26:
                    color = AQUAMARINE
                if decomposed[row][col] == 27:
                    color = MIDNIGHTBLUE
                if decomposed[row][col] == 28:
                    color = ORANGERED
                if decomposed[row][col] == MAX:
                    color = SPRINGGREEN
                pg.draw.rect(self.WIN, color,
                             [EPSILON * col + BORDER, EPSILON * row + BORDER, EPSILON - BORDER, EPSILON - BORDER])
        pg.draw.rect(self.WIN,(255,255,255), (0, EPSILON*len(decomposed), EPSILON*len(decomposed), EPSILON))


    def add_node(self, node):
        if self.edges.get(node) == None:
            self.edges[node] = list()

    def add_edge(self, node1, node2):
        if node2 not in self.neighbors(node1):
            self.edges[node1].append(node2)
            self.edges[node2].append(node1)


# 1 : obstacle (black), cell id = 1 -> total_cells_number
def Boustrophedon_Cellular_Decomposition(environment):
    environment = np.array(environment)

    def calculate_connectivity(slice):
        connectivity = 0
        connective_parts = []
        start_point = -1
        for i in range(len(slice)):
            if slice[i] == 1 and start_point != -1:
                connectivity += 1
                connective_parts.append((start_point, i))
                start_point = -1
            elif slice[i] == 0 and start_point == -1:
                start_point = i
            # print(connectivity)
            # print(connective_parts)
        if start_point != -1:
            connectivity += 1
            # print(connectivity)
            connective_parts.append((start_point, len(slice)))
        # print(connectivity)
        # print(connective_parts)
        return connectivity, connective_parts

    def get_adjacency_matrix(left_parts, right_parts) -> np.ndarray:
        adjacency_matrix = np.zeros([len(left_parts), len(right_parts)], dtype=bool)
        # print(adjacency_matrix)
        for i, left_part in enumerate(left_parts):
            for j, right_part in enumerate(right_parts):
                if min(left_part[1], right_part[1]) - max(left_part[0], right_part[0]) > 0:
                    adjacency_matrix[i, j] = True
        # print(adjacency_matrix)
        return adjacency_matrix

    last_connectivity = 0
    last_connectivity_parts = []
    last_cells = []
    total_cells_number = 0
    decomposed = np.zeros(environment.shape, dtype=int)  # obstacle
    adjacency_graph = Graph()

    for x in range(environment.shape[1]):
        current_slice = environment[:, x]
        connectivity, connective_parts = calculate_connectivity(current_slice)
        # print(connectivity)

        if last_connectivity == 0:
            current_cells = []
            for _ in range(connectivity):
                total_cells_number += 1
                current_cells.append(total_cells_number)
                # print(total_cells_number)

        elif connectivity == 0:
            current_cells = []

        else:
            # print(x,': last_connect:',last_connectivity_parts)
            # print(connective_parts)
            adjacency_matrix = get_adjacency_matrix(last_connectivity_parts, connective_parts)
            # print('adj_matrix:',adjacency_matrix)
            # print('connectivity:',connectivity)
            current_cells = [0] * len(connective_parts)
            # print(current_cells)

            for i in range(last_connectivity):
                if np.sum(adjacency_matrix[i, :]) == 1:
                    for j in range(connectivity):
                        if adjacency_matrix[i, j]:
                            # print('fi:',current_cells[j])
                            current_cells[j] = last_cells[i]
                            # print('se:',current_cells[j])
                # IN
                elif np.sum(adjacency_matrix[i, :]) > 1:
                    for j in range(connectivity):
                        if adjacency_matrix[i, j]:
                            # print('total',total_cells_number)
                            total_cells_number = total_cells_number + 1
                            # print('efi:', current_cells[j])
                            current_cells[j] = total_cells_number
                            # print('ese:', current_cells[j])
            # print('Curent:',current_cells)
            for j in range(connectivity):
                # OUT
                if np.sum(adjacency_matrix[:, j]) > 1:
                    total_cells_number = total_cells_number + 1
                    current_cells[j] = total_cells_number
                # IN
                # elif np.sum(adjacency_matrix[:, j]) == 0 :
                #     total_cells_number = total_cells_number + 1
                #     current_cells[j] = total_cells_number

        for cell, slice in zip(current_cells, connective_parts):
            # print('cell:',cell,'slide:',slice)
            # print('slide0',slice[0],'slide1',slice[1])
            decomposed[slice[0]: slice[1], x] = cell

        last_connectivity = connectivity
        last_connectivity_parts = connective_parts
        last_cells = current_cells
        # print('current1 :',current_cells)

    return decomposed, total_cells_number, adjacency_graph


def CheckCell(decompose, x, y, i):
    if 0 <= x <= len(decompose[0]) - 1 and 0 <= y <= len(decompose) - 1:
        if decompose[y][x] == i:
            return True
    return False


def startpoint1(decompose, i):
    for y in range(len(decompose)):
        for x in range(len(decompose[0])):
            if decompose[y][x] == i:
                return x, y
    return 0, 0

def startpoint2(decompose, i):
    for y in range(len(decompose)-1,0,-1):
        for x in range(len(decompose[0])):
            if decompose[y][x] == i:
                return x, y
    return 0, 0
def startpoint3(decompose, i):
    for y in range(len(decompose)):
        for x in range(len(decompose[0])-1,0,-1):
            if decompose[y][x] == i:
                return x, y
    return 0, 0
def startpoint4(decompose, i):
    for y in range(len(decompose)-1,0,-1):
        for x in range(len(decompose[0])-1,0,-1):
            if decompose[y][x] == i:
                return x, y
    return 0, 0


def BoustrophedonMove1(decompose, i, x, y):
    global count
    ui.draw(decomposed)
    clock.tick(fps)
    South = [y + SOUTH[0], x + SOUTH[1]]
    North = [y + NORTH[0], x + NORTH[1]]
    East = [y + EAST[0], x + EAST[1]]
    West = [y + WEST[0], x + WEST[1]]

    if CheckCell(decompose, South[0], South[1], i):
        move = SOUTH
    elif CheckCell(decompose, North[0], North[1], i):
        move = NORTH
    elif CheckCell(decompose, East[0], East[1], i):
        move = EAST
    # elif CheckCell(decompose, West[0], West[1],i):
    #     move = WEST
    else:
        move = [0, 0]

    y += move[0]
    x += move[1]
    # print(path)
    if move[0] == 0 and move[1] == 0:
        # print(y,x)
        return (y,x)
    else:
        decompose[x][y] = MAX
        count += 1
        return(BoustrophedonMove1(decompose, i, x, y))


def BoustrophedonMove2(decompose, i, x, y):
    global count
    ui.draw(decomposed)
    clock.tick(fps)
    South = [y + SOUTH[0], x + SOUTH[1]]
    North = [y + NORTH[0], x + NORTH[1]]
    East = [y + EAST[0], x + EAST[1]]
    West = [y + WEST[0], x + WEST[1]]

    if CheckCell(decompose, North[0], North[1], i):
        move = NORTH
    elif CheckCell(decompose, South[0], South[1], i):
        move = SOUTH
    elif CheckCell(decompose, East[0], East[1], i):
        move = EAST
    # elif CheckCell(decompose, West[0], West[1],i):
    #     move = WEST
    else:
        move = [0, 0]

    y += move[0]
    x += move[1]
    # print(path)
    if move[0] == 0 and move[1] == 0:
        return (y,x)
    else:
        decompose[x][y] = MAX
        count += 1
        return(BoustrophedonMove2(decompose, i, x, y))


def  BoustrophedonMove3(decompose, i, x, y):
    global count
    ui.draw(decomposed)
    clock.tick(fps)
    South = [y + SOUTH[0], x + SOUTH[1]]
    North = [y + NORTH[0], x + NORTH[1]]
    East = [y + EAST[0], x + EAST[1]]
    West = [y + WEST[0], x + WEST[1]]

    if CheckCell(decompose, South[0], South[1], i):
        move = SOUTH
    elif CheckCell(decompose, North[0], North[1], i):
        move = NORTH
    elif CheckCell(decompose, West[0], West[1],i):
        move = WEST
    # elif CheckCell(decompose, East[0], East[1], i):
    #     move = EAST

    else:
        move = [0, 0]

    y += move[0]
    x += move[1]
    # print(path)
    if move[0] == 0 and move[1] == 0:
        return (y, x)
    else:
        decompose[x][y] = MAX
        count += 1
        return (BoustrophedonMove3(decompose, i, x, y))

def BoustrophedonMove4(decompose, i, x, y):
    global count
    ui.draw(decomposed)
    clock.tick(fps)
    South = [y + SOUTH[0], x + SOUTH[1]]
    North = [y + NORTH[0], x + NORTH[1]]
    East = [y + EAST[0], x + EAST[1]]
    West = [y + WEST[0], x + WEST[1]]

    if CheckCell(decompose, North[0], North[1], i):
        move = NORTH
    elif CheckCell(decompose, South[0], South[1], i):
        move = SOUTH
    elif CheckCell(decompose, West[0], West[1],i):
        move = WEST
    # elif CheckCell(decompose, East[0], East[1], i):
    #     move = EAST

    else:
        move = [0, 0]

    y += move[0]
    x += move[1]
    # print(path)
    if move[0] == 0 and move[1] == 0:
        return (y, x)
    else:
        decompose[x][y] = MAX
        count += 1
        return (BoustrophedonMove4(decompose, i, x, y,))

def distance(a,b):
    c=abs(a[0]-b[0])+abs(a[1]-b[1])
    return c

def main():
    pg.init()
    screen = pg.display.set_mode((400, 400))
    ingame = True
    clock = pg.time.Clock()

    bs = decomposed


if __name__ == "__main__":



    ui = Graph()
    clock = pg.time.Clock()
    ui.read_map('map/map_7.txt')
    environment = ui.read_map('map/map_7.txt')


    decomposed, region_count, adj_graph = Boustrophedon_Cellular_Decomposition(environment)
    decomposed2 = decomposed
    # print(startpoit(decomposed,3))
    print(decomposed)
    # print(decomposed[0][0])
    # print(region_count)

    # x, y = startpoint(decomposed2, 1)
    # print('Điểm bắt đầu là : (', x, ',', y, ')')
    # path = []
    # BoustrophedonMove(decomposed2, 1, y, x, path)
    # print('Đường đi của ô số', 1, 'là :')
    # print(path)
    #
    # for i in range(1,region_count+1,1):
    #     x, y = startpoint(decomposed2,i)
    #     print('Điểm bắt đầu là : (',x,',',y,')')
    #     path = []
    #     BoustrophedonMove(decomposed2,i,y,x,path)
    #     print('Đường đi của ô số',i,'là :')
    #     print(path)
    # print(adj_graph)
    list_graph = [1,2,6,18,20,21,22,27,24,23,23,25,26,26,19,17,15,14,20,16,17,9,5,4,10,11,13,13,12,6,7,10,5,3,1]
    ui.draw(decomposed)

    run = True
    run1 = False
    global count
    count = 0

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_SPACE :
                    run1 = True

        if run1:
            choose = []
            ui.draw(decomposed)
            for i in range(1, region_count + 1, 1):
                print("vùng số ",i)
            # for i in list_graph:


                if i==1:
                    x, y = startpoint1(decomposed2, i)
                # print('Điểm bắt đầu là : (', x, ',', y, ')')

                    result=(BoustrophedonMove1(decomposed2, i, y, x))
                    choose.insert(i,result)
                    print(choose[i-1])

                # print(BoustrophedonMove1(decomposed2, i, y, x, path))
                    print("Chi phí đến đây:",count)
                # print('Đường đi của ô số', i, 'là :')
                # print(path)

                elif i>=2:
                    print("Vị trí ô số 1", startpoint1(decomposed2, i))
                    print("Vị trí ô số 2", startpoint2(decomposed2, i))
                    print("Vị trí ô số 3", startpoint3(decomposed2, i))
                    print("Vị trí ô số 4", startpoint4(decomposed2, i))

                    startpoint = []
                    if choose[i-2]==[0,0]:
                        startpoint.insert(1, (distance(choose[i - 3], startpoint1(decomposed2, i))))
                        startpoint.insert(2, (distance(choose[i - 3], startpoint2(decomposed2, i))))
                        startpoint.insert(3, (distance(choose[i - 3], startpoint3(decomposed2, i))))
                        startpoint.insert(4, (distance(choose[i - 3], startpoint4(decomposed2, i))))
                    else:
                        startpoint.insert(1,(distance(choose[i - 2], startpoint1(decomposed2, i))))
                        startpoint.insert(2,(distance(choose[i - 2], startpoint2(decomposed2, i))))
                        startpoint.insert(3,(distance(choose[i - 2], startpoint3(decomposed2, i))))
                        startpoint.insert(4,(distance(choose[i - 2], startpoint4(decomposed2, i))))
                    min_value=min(startpoint)
                    print("Chi Phí đến vùng tiếp theo là :",min_value)
                    count+=min_value
                    min_index=startpoint.index(min_value)
                    print(startpoint)
                    print("Ô đầu vào là ô số",min_index+1)
                    if (min_index == 0):
                        x, y = startpoint1(decomposed2, i)
                        print("Điểm bắt đầu",startpoint1(decomposed2, i))
                        # BoustrophedonMove1(decomposed2,i,x,y)
                        result = (BoustrophedonMove1(decomposed2, i, y, x))
                        choose.insert(i, result)
                    elif (min_index == 1):
                        x, y = startpoint2(decomposed2, i)
                        print("Điểm bắt đầu",startpoint2(decomposed2, i))
                        # BoustrophedonMove2(decomposed2, i, x, y)
                        result = (BoustrophedonMove2(decomposed2, i, y, x))
                        choose.insert(i, result)
                    elif (min_index == 2):
                        x, y = startpoint3(decomposed2, i)
                        print("Điểm bắt đầu",startpoint3(decomposed2, i))
                        # BoustrophedonMove3(decomposed2, i, x, y)
                        result = (BoustrophedonMove3(decomposed2, i, y, x))
                        choose.insert(i, result)
                    elif (min_index == 3):
                        x, y = startpoint4(decomposed2, i)
                        print("Điểm bắt đầu",startpoint4(decomposed2, i))
                        # BoustrophedonMove4(decomposed2, i, x, y)
                        result = (BoustrophedonMove4(decomposed2, i, y, x))
                        choose.insert(i, result)
                    print("Chi phí đến đây:",count)
            print(choose[26])
            count+=(choose[region_count-1][0]+choose[region_count-1][1])
            print("final:",count)
            run1 =False




        # pg.display.flip()
    pg.quit()
