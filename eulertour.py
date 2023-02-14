def next_node(edge, current):
    return edge[0] if current == edge[1] else edge[1]

def remove_edge(raw_list, discard):
    return [item for item in raw_list if item != discard]

def find_eulerian_tour(graph):
    search = [[[], graph[0][0], graph]]
    while search:

        path, node, unexplore = search.pop()
        path += [node]
        # print('path:',path)
        # print('node:',node)
        # print('unexplore:',unexplore)

        if not unexplore:
            return path

        for edge in unexplore:
            if node in edge:
                search += [[path, next_node(edge, node), remove_edge(unexplore, edge)]]

if __name__ == '__main__':
    graph = [(1, 2), (2, 1), (2, 3), (2, 6), (3, 4), (4, 3), (4, 5), (5, 4), (5, 6), (5, 8), (6, 7), (7, 6), (7, 8),
             (7, 9), (8, 10), (10, 8), (9, 10), (9, 11), (11, 9), (11, 14), (11, 18), (3, 12), (12, 13), (13, 14),
             (14, 13), (13, 15), (10, 14), (15, 16), (15, 17), (17, 15), (16, 18), (18, 16), (16, 17), (17, 19), (18, 19) ]
    print('Euler_tour:',find_eulerian_tour(graph))