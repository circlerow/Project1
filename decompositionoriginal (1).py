# Reference : https://github.com/WJTung/GA-TSPCPP/blob/master/Decomposition.py
import numpy as np

class Region :
    def __init__(self, id) :
        self.region_id = id
        self.min_y, self.max_y = None, None
        self.cell_list = list()
        self.center = (None, None)

class Graph :
    def __init__(self):
        self.edges = dict()
    
    def neighbors(self, node):
        return self.edges[node]
    
    def add_node(self, node):
        if self.edges.get(node) == None:
            self.edges[node] = list()
    
    def add_edge(self, node1, node2):
        if node2 not in self.neighbors(node1):
            self.edges[node1].append(node2)
            self.edges[node2].append(node1)

# 1 : obstacle (black), cell id = 1 -> total_cells_number
def Boustrophedon_Cellular_Decomposition(environment) :
    def calculate_connectivity(slice) :
        connectivity = 0
        connective_parts = []
        start_point = -1
        for i in range(len(slice)) :
            if slice[i] == 1 and start_point != -1 :
                connectivity += 1
                connective_parts.append((start_point, i))
                start_point = -1
            elif slice[i] == 0 and start_point == -1 :
                start_point = i
        if start_point != -1 :
            connectivity += 1
            connective_parts.append((start_point, len(slice)))
        return connectivity, connective_parts

    def get_adjacency_matrix(left_parts, right_parts) -> np.ndarray :
        adjacency_matrix = np.zeros([len(left_parts), len(right_parts)], dtype = bool)
        for i, left_part in enumerate(left_parts) :
            for j, right_part in enumerate(right_parts) :
                if min(left_part[1], right_part[1]) - max(left_part[0], right_part[0]) > 0:
                    adjacency_matrix[i, j] = True

        return adjacency_matrix

    last_connectivity = 0
    last_connectivity_parts = []
    last_cells = []
    total_cells_number = 0
    decomposed = np.zeros(environment.shape, dtype = int) # obstacle
    adjacency_graph = Graph()

    for x in range(environment.shape[1]) :
        current_slice = environment[:, x]
        connectivity, connective_parts = calculate_connectivity(current_slice)

        if last_connectivity == 0 :
            current_cells = []
            for _ in range(connectivity) :
                total_cells_number += 1
                current_cells.append(total_cells_number)

        elif connectivity == 0 :
            current_cells = []
        
        else :
            adjacency_matrix = get_adjacency_matrix(last_connectivity_parts, connective_parts)
            current_cells = [0] * len(connective_parts)

            for i in range(last_connectivity) :
                if np.sum(adjacency_matrix[i, :]) == 1 :
                    for j in range(connectivity) :
                        if adjacency_matrix[i, j] :
                            current_cells[j] = last_cells[i]
                # IN
                elif np.sum(adjacency_matrix[i, :]) > 1 :
                    for j in range(connectivity) :
                        if adjacency_matrix[i, j] :
                            total_cells_number = total_cells_number + 1
                            current_cells[j] = total_cells_number

            for j in range(connectivity) :
                # OUT
                if np.sum(adjacency_matrix[:, j]) > 1 :
                    total_cells_number = total_cells_number + 1
                    current_cells[j] = total_cells_number
                # IN
                elif np.sum(adjacency_matrix[:, j]) == 0 :
                    total_cells_number = total_cells_number + 1
                    current_cells[j] = total_cells_number

        # TODO (maybe):
        # build the connectivity graph using: adjacency_matrix, last_cells, current_cells
        for cell in current_cells:
            adjacency_graph.add_node(cell)
        for i, l_cell in enumerate(last_cells):
            for j, c_cell in enumerate(current_cells):
                if adjacency_matrix[i][j] == True and l_cell != c_cell:
                    adjacency_graph.add_edge(l_cell, c_cell)
        
        for cell, slice in zip(current_cells, connective_parts) :
            decomposed[slice[0] : slice[1], x] = cell

        last_connectivity = connectivity
        last_connectivity_parts = connective_parts
        last_cells = current_cells

    return decomposed, total_cells_number, adjacency_graph

def create_regions(decomposed, region_count):
    regions = [None] * (region_count + 1) # using index >= 1 (no region with id 0)

    for x in range(len(decomposed)):
        for y in range(len(decomposed[0])):
            id = decomposed[x, y]

            if id == 0: continue # obstacle
            if regions[id] == None:
                regions[id] = Region(id)

            regions[id].cell_list.append((x, y))
            if regions[id].min_y == None or y < regions[id].min_y:
                regions[id].min_y = y
            if regions[id].max_y == None or y > regions[id].max_y:
                regions[id].max_y = y
    
    # calculate center
    for region in regions:
        if region == None: continue    

        region.center = np.mean(region.cell_list, axis=0)
    
    return regions


if __name__ == "__main__" :
    environment = np.zeros([8, 8], dtype=int)
    environment[4][4] = environment[4][5] = environment[5][4] = environment[5][5] = 1
    decomposed, region_count, adj_graph = Boustrophedon_Cellular_Decomposition(environment)
    print(environment.shape)

    regions = create_regions(decomposed, region_count)
    pass
