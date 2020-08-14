"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex Does not exist!")

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        queue = Queue()
        queue.enqueue(starting_vertex)
        visited = set()

        while queue.size() > 0:
            visiting = queue.dequeue()
            if visiting not in visited:
                visited.add(visiting)
                print(visiting)
                for next_vertex in self.get_neighbors(visiting):
                    queue.enqueue(next_vertex)

    def dft(self, starting_vertex):
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()

        while stack.size() > 0:
            visiting = stack.pop()
            if visiting not in visited:
                visited.add(visiting)
                print(visiting)
                for next_vertex in self.get_neighbors(visiting):
                    stack.push(next_vertex)

    def dft_recursive(self, starting_vertex, visited=None):
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        print(starting_vertex)

        for next_vertex in self.get_neighbors(starting_vertex):
            if next_vertex not in visited:
                self.dft_recursive(next_vertex, visited)

    def bfs(self, starting_vertex, destination_vertex):
        queue = Queue()
        queue.enqueue([starting_vertex])

        visited = set()

        while queue.size() > 0:
            path = queue.dequeue()
            visiting = path[-1]

            if visiting not in visited:
                if visiting == destination_vertex:
                    return path
                visited.add(visiting)

                for next_visiting in self.get_neighbors(visiting):
                    path_copy = list(path)
                    path_copy.append(next_visiting)
                    queue.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        stack = Stack()
        stack.push([starting_vertex])

        visited = set()

        while stack.size() > 0:
            path = stack.pop()
            visiting = path[-1]

            if visiting not in visited:
                if visiting == destination_vertex:
                    return path
                visited.add(visiting)

                for next_visiting in self.get_neighbors(visiting):
                    path_copy = list(path)
                    path_copy.append(next_visiting)
                    stack.push(path_copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None):
        if starting_vertex == destination_vertex:
            return [starting_vertex]

        if visited is None:
            visited = set()

        visited.add(starting_vertex)

        for next_vertex in self.get_neighbors(starting_vertex):
            if next_vertex not in visited:
                path = self.dfs_recursive(
                    next_vertex, destination_vertex, visited)
                if path is not None:
                    path.insert(0, starting_vertex)
                    return path

    # def bft_ancestors(self, starting_vertex):
    #     queue = Queue()
    #     queue.enqueue(starting_vertex)
    #     visited = set()
    #     ancestors_dict = {}

    #     while queue.size() > 0:
    #         visiting = queue.dequeue()
    #         # if next_vertex not in ancestors_dict:
    #         #     ancestors_dict[next_vertex] = set()
    #         # ancestors_dict[next_vertex].add(visiting)
    #         if visiting not in visited:
    #             ancestors_dict[visiting] = self.get_neighbors(visiting)
    #             visited.add(visiting)
    #             for next_vertex in self.get_neighbors(visiting):
    #                 queue.enqueue(next_vertex)

    #     return ancestors_dict

    def dft_recursive_ancestors(self, starting_vertex, visited=None, count=0):
        if len(self.get_neighbors(starting_vertex)) == 0:
            return [set([starting_vertex]), count]
        ancestors = [set([-1]), 0]
        count += 1
        if visited is None:
            visited = set()
        visited.add(starting_vertex)

        for next_vertex in self.get_neighbors(starting_vertex):
            if next_vertex not in visited:
                found_ancestor = (self.dft_recursive_ancestors(
                    next_vertex, visited, count))
                if found_ancestor[1] > ancestors[1]:
                    ancestors = found_ancestor
                if found_ancestor[1] == ancestors[1]:
                    ancestors[0] = ancestors[0].union(found_ancestor[0])
        return ancestors


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
