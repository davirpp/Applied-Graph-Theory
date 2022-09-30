class Graph:

    def __init__(self, instance=None):
        self.matrix, self.adj_lists, self.edges, self.n_vertices = self.__read_instance(instance)

    @staticmethod
    def __read_instance(instance):
        """
        It reads a file and returns a matrix, a list of adjacency lists, a list of edges, and the number of
        vertices
        
        :param instance: the path to the instance file
        :return: The matrix, adjacency lists, edges, and number of vertices.
        """
        file = open(instance, 'r')
        n_vertices = int(file.readline())
        matrix = []
        for _ in range(n_vertices):
            line = file.readline().split()
            casting = list(map(int, line[0]))
            matrix.append(casting)
        file.close()

        adj_lists = []
        for i in range(n_vertices):
            n_adj = [i + 1 for i, a in enumerate(matrix[i]) if a == 1]
            adj_lists.append(n_adj)

        edges = []
        for i in range(n_vertices):
            j = i + 1
            while j < n_vertices:
                if matrix[i][j]:
                    edges.append((i + 1, j + 1))
                j += 1

        return matrix, adj_lists, edges, n_vertices

    def max_min_degree(self):
        """
        It returns the maximum and minimum degree of the graph
        :return: The maximum and minimum degree of the graph.
        """
        max_d = min_d = len(self.adj_lists[0])

        for i in range(self.n_vertices):
            if len(self.adj_lists[i]) > max_d:
                max_d = len(self.adj_lists[i])
            elif len(self.adj_lists[i]) < min_d:
                min_d = len(self.adj_lists[i])
        return max_d, min_d

    def degree_sequence(self):  # sourcery skip: list-comprehension
        """
        It returns a sorted list of the degrees of the vertices in the graph.
        :return: The degree sequence of the graph.
        """
        degree_list = []
        for i in range(self.n_vertices):
            degree_list.append(len(self.adj_lists[i]))
        return sorted(degree_list)

    def degree_and_neighbors(self, vertice):
        """
        The function returns the degree of a vertice, the open neighbors of a vertice, and the close
        neighbors of a vertice
        
        :param vertice: the vertice you want to find the degree and neighbors of
        :return: The degree of the vertice, the open neighbors of the vertice, and the close neighbors
        of the vertice.
        """
        if vertice not in list(range(1, self.n_vertices + 1)):
            print(f"Vertice {vertice} not in list of vertices")
            return None

        degree = len(self.adj_lists[vertice - 1])
        open_neighbor = self.adj_lists[vertice - 1][:]
        close_neighbor = self.adj_lists[vertice - 1][:]
        close_neighbor.append(vertice)
        close_neighbor.sort()
        return degree, open_neighbor, close_neighbor

    def is_adjacent(self, vertice_1, vertice_2):
        """
        It checks if two vertices are adjacent.
        
        :param vertice_1: The first vertice to check if it's adjacent to the second vertice
        :param vertice_2: The vertice you want to check if it's adjacent to vertice_1
        :return: A boolean value.
        """
        return bool(self.matrix[vertice_1 - 1][vertice_2 - 1])

    def is_regular(self):
        """
        If all the vertices have the same degree, then the graph is regular
        :return: A boolean value and the degree of the graph.
        """
        degree = len(self.adj_lists[0])

        for i in range(self.n_vertices):
            if degree == len(self.adj_lists[i]):
                continue
            else:
                return False
        return True, degree

    def is_complete(self):  # sourcery skip: sum-comprehension
        """
        It checks if the graph is complete.
        :return: The number of edges in the graph.
        """
        n_edges = 0

        for i in range(self.n_vertices):
            n_edges += len(self.adj_lists[i])
        n_edges /= 2
        n_max_edge = (self.n_vertices * (self.n_vertices - 1)) / 2
        return n_max_edge == n_edges

    def universal_vertices(self):
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        """
        For each vertex, check if it is adjacent to all other vertices. If so, add it to the list of
        universal vertices
        :return: A list of vertices that are adjacent to all other vertices.
        """
        universals_list = []

        for i in range(self.n_vertices):
            if len(self.adj_lists[i]) == self.n_vertices - 1:
                universals_list.append(i + 1)
        return universals_list

    def isolated_vertices(self):
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        """
        The function `isolated_vertices` returns a list of isolated vertices in the graph
        :return: A list of isolated vertices.
        """
        isolated_lists = []

        for i in range(self.n_vertices):
            if len(self.adj_lists[i]) == 0:
                isolated_lists.append(i + 1)
        return isolated_lists

    def is_subgraph(self, vertices_list, edges_list):
        # sourcery skip: invert-any-all, use-any
        """
        If the vertices and edges of the subgraph are all in the graph, then if you can walk in the edges, is a subgraph 
        
        :param vertices_list: a list of vertices in the subgraph
        :param edges_list: a list of tuples, each tuple is an edge
        :return: returns True if the graph is a subgraph of the graph, and False
        otherwise.
        """
        if not set(vertices_list).issubset(set(list(range(1, self.n_vertices + 1)))):
            return False

        for i in range(len(edges_list)):
            u, v = edges_list[i]
            if not self.is_adjacent(u, v):
                return False

        for e in edges_list:
            if not set(e).issubset(set(vertices_list)):
                return False
        return True

    def is_walk(self, walk_list):
        # sourcery skip: invert-any-all, remove-redundant-continue, use-any
        """
        If the walk is valid, return True, else return False
        
        :param walk_list: a list of vertices that are visited in order
        :return: The function is_walk() returns a boolean value.
        """
        for i in range(len(walk_list) - 1):
            if self.matrix[walk_list[i] - 1][walk_list[i + 1] - 1]:
                continue
            else:
                return False
        return True

    def is_path(self, path_list):
        """
        If the path is a walk and the path is a set, then is a path
        
        :param path_list: a list of nodes
        :return: True or False
        """
        if not self.is_walk(path_list):
            return False
            
        if path_list == list(set(path_list)):
            pass
        else:
            return False
        return True

    def is_cycle(self, cycle_list):
        """
        If the list is a walk and the first and last elements are the same and the list has no repeated
        elements except for the first and last elements, then the list is a cycle
        
        :param cycle_list: a list of vertices
        :return: A boolean value.
        """
        if not self.is_walk(cycle_list) or cycle_list[0] != cycle_list[-1]:
            return False

        sliced = cycle_list[1:-1]
        return sliced == list(set(sliced))

    def is_trail(self, trail_list):
        """
        If the trail is a walk, then check if is a trail by checking if the edges are unique
        
        :param trail_list: a list of vertices
        :return: A boolean value.
        """
        if not self.is_walk(trail_list):
            return False

        edges = []

        for i in range(len(trail_list) - 1):
            edge = (trail_list[i], trail_list[i + 1])
            if edge in edges or edge[::-1] in edges:
                return False
            else:
                edges.append(edge)
        return True

    def is_clique(self, clique_list, matrix=None):
        """
        If the list is not a set, return false. If the list is a set, then for each element in the list,
        check if the element is connected to all other elements in the list. If it is not, return false. If
        it is, return true
        
        :param clique_list: a list of vertices that are in the clique
        :param matrix: the adjacency matrix of the graph
        :return: A boolean value.
        """
        if not matrix:
            matrix = self.matrix

        if clique_list != list(set(clique_list)):
            return False

        for i, v in enumerate(clique_list):
            n_list = matrix[v - 1]
            for j in clique_list:
                if clique_list[i] == j:
                    continue
                if not n_list[j - 1]:
                    return False
        return True

    def is_max_clique(self, clique_list):  # sourcery skip: list-comprehension
        """
        It checks if the given list of vertices is a clique and if it is, it checks if it is a maximal
        clique.
        
        :param clique_list: a list of vertices that are in the clique
        :return: A list of all the maximal cliques in the graph.
        """
        if not self.is_clique(clique_list):
            return False

        adjs_list = []

        for i in range(len(clique_list)):
            adjs_list.append(self.adj_lists[clique_list[i] - 1])
        intersection = set.intersection(*map(set, adjs_list))
        return not intersection

    def complement_graph(self):
        """
        It takes the matrix of the graph and returns the edges of the complement graph and the matrix of
        the complement graph
        :return: A list of edges and a matrix
        """
        edges = []
        complement_matrix = [row[:] for row in self.matrix]
        for i in range(self.n_vertices):
            j = i + 1
            while j < self.n_vertices:
                if not self.matrix[i][j]:
                    edges.append((i + 1, j + 1))
                j += 1
            for j in range(self.n_vertices):
                complement_matrix[i][j] = 0 if self.matrix[i][j] else 1
        return edges, complement_matrix

    def is_independent_set(self, set_list):
        """
        If the complement of the graph is a clique, then the graph is an independent set
        
        :param set_list: a list of vertices
        :return: The complement graph of the graph.
        """
        _, comp_matrix = self.complement_graph()
        return self.is_clique(set_list, comp_matrix)


