from graph import Graph
from vertex import Vertex
from edge import Edge
from step import Step

class JKUMap(Graph):

    def __init__(self):
        super().__init__()
        v_spar = self.insert_vertex("Spar")
        v_lit = self.insert_vertex("LIT")
        v_openlab = self.insert_vertex("Open Lab")
        v_khg = self.insert_vertex("KHG")
        v_parking = self.insert_vertex("Parking")
        v_bellacasa = self.insert_vertex("Bella Casa")
        v_sp1 = self.insert_vertex("SP1")
        v_sp3 = self.insert_vertex("SP3")
        v_lui = self.insert_vertex("LUI")
        v_teichwerk = self.insert_vertex("Teichwerk")
        v_library = self.insert_vertex("Library")
        v_chat = self.insert_vertex("Chat")
        v_bank = self.insert_vertex("Bank")
        v_porter = self.insert_vertex("Porter")
        v_castle = self.insert_vertex("Castle")
        v_papaya = self.insert_vertex("Papaya")
        v_JKH = self.insert_vertex("JKH")

        self.insert_edge(v_spar, v_lit, 50)
        self.insert_edge(v_spar, v_porter, 103)
        self.insert_edge(v_spar, v_khg, 165)
        self.insert_edge(v_khg, v_bank, 150)
        self.insert_edge(v_khg, v_parking, 190)
        self.insert_edge(v_parking, v_bellacasa, 145)
        self.insert_edge(v_parking, v_sp1, 240)
        self.insert_edge(v_sp1, v_sp3, 130)
        self.insert_edge(v_sp1, v_lui, 175)
        self.insert_edge(v_lui, v_teichwerk, 135)
        self.insert_edge(v_lui, v_library, 90)
        self.insert_edge(v_lui, v_chat, 240)
        self.insert_edge(v_library, v_chat, 160)
        self.insert_edge(v_chat, v_bank, 115)
        self.insert_edge(v_bank, v_porter, 100)
        self.insert_edge(v_porter, v_openlab, 70)
        self.insert_edge(v_porter, v_lit, 80)
        self.insert_edge(v_castle, v_papaya, 85)
        self.insert_edge(v_papaya, v_JKH, 80)


    def get_shortest_path_from_to(self, from_vertex: Vertex, to_vertex: Vertex):
        """
        This method determines the shortest path between two POIs "from_vertex" and "to_vertex".
        It returns the list of intermediate steps of the route that have been found
        using the dijkstra algorithm.

        :param from_vertex: Start vertex
        :param to_vertex:   Destination vertex
        :return:
           The path, with all intermediate steps, returned as an list. This list
           sequentially contains each vertex along the shortest path, together with
           the already covered distance (see example on the assignment sheet).
           Returns None if there is no path between the two given vertices.
        :raises ValueError: If from_vertex or to_vertex is None, or if from_vertex equals to_vertex
        """

        if from_vertex is None or to_vertex is None or from_vertex == to_vertex:
            raise ValueError

        self.init_dijkstra(from_vertex)
        self._dijkstra(from_vertex)
        self.unload_dijkstras()

        list = self.create_path(from_vertex, to_vertex, [])[::-1]
        if len(list) != 0:
            return list
        else:
            return None



    def get_steps_for_shortest_paths_from(self, from_vertex: Vertex):
        """
        This method determines the amount of "steps" needed on the shortest paths
        from a given "from" vertex to all other vertices.
        The number of steps (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and number of steps as value.
        E.g., the "from" vertex has a step count of 0 to itself and 1 to all adjacent vertices.

        :param from_vertex: start vertex
        :return:
          A map containing the number of steps (or -1 if no path exists) on the
          shortest path to each vertex, using the vertex name as key and the number of steps as value.
        :raises ValueError: If from_vertex is None.
        """
        if from_vertex is None:
            raise ValueError
        self.init_dijkstra(from_vertex)
        self._dijkstra(from_vertex)
        self.unload_dijkstras()

        self.print_table()

        maps = {}
        for line in self.table:
            if line[1] == -1:
                maps[line[0].name] = -1
            else:
                maps[line[0].name] = line[2]
        return maps

    def get_shortest_distances_from(self, from_vertex: Vertex):
        """
        This method determines the shortest paths from a given "from" vertex to all other vertices.
        The shortest distance (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and the distance as value.

        :param from_vertex: Start vertex
        :return
           A dictionary containing the shortest distance (or -1 if no path exists) to each vertex,
           using the vertex name as key and the distance as value.
        :raises ValueError: If from_vertex is None.
        """
        if from_vertex is None:
            raise ValueError

        self.init_dijkstra(from_vertex)
        self._dijkstra(from_vertex)
        self.unload_dijkstras()

        maps = {}
        for line in self.table:
            if line[2] == -1:
                maps[line[0].name] = -1
            else:
                maps[line[0].name] = line[1]
        return maps


    def init_dijkstra(self, start: Vertex):
        self.unvisited = self.get_vertices().copy()
        self.visited = []
        self.table = []
        for i in self.unvisited:
            if i == start:
                self.table.append([i, 0, 0, None])
            else:
                self.table.append([i,999999,0, None])
        return self.table

    def get_min_distance(self):
        min = [None, 99999]
        for line in self.table:
            if line[1] < min[1] and line[0] in self.unvisited:
                min = [line[0], line[1]]
        return min

    def print_table(self):
        for i in self.table:
            if i[3] is not None:
                print(i[0].name, i[1], i[2], i[3].name)
            else:
                print(i[0].name, i[1], i[2], i[3])

    def _dijkstra(self, cur: Vertex):
        """
        This method is expected to be called with correctly initialized data structures and recursively calls itself.

        :param cur: Current vertex being processed
        :param visited_list: List which stores already visited vertices.
        :param distances: Dict (nVertices entries) which stores the min. distance to each vertex.
        :param paths: Dict (nVertices entries) which stores the shortest path to each vertex.
        """
        if cur in self.unvisited:
            self.unvisited.remove(cur) #removing vertex from unvisited

        if cur is not None:
            adjacent = self.get_adjacent_vertices(cur) #getting adjacent vertices
        if cur is None:
            adjacent = []

        curr_weight = 0 #preparing current weight of the edge
        step = 0

        for line in self.table:
            if line[0] == cur:
                curr_weight += line[1]
                step += line[2]

        if len(adjacent) != 0:
            for vertex in adjacent:
                curr_edge = self.find_edge(cur, vertex)
                for line in self.table:
                    if line[0] == vertex:
                        if curr_weight + curr_edge.weight < line[1]:
                            line[1] = curr_weight + curr_edge.weight
                            line[2] = step + 1
                            line[3] = cur



        l = self.get_min_distance()
        if l[0] is not None:
            self._dijkstra(l[0])


    def unload_dijkstras(self):
        for i in self.table:
            if i[1] == 999999:
                i[1] = -1

    def create_path(self, start: Vertex, end: Vertex, road):
        a = None

        for line in self.table:
            if line[0] == end:
                if line[1] == -1:
                    return []
                step = Step(end,line[1])
                road.append(step)
                a = line[3]
        if start != end:
            self.create_path(start, a, road)
        return road