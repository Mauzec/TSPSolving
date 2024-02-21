import networkx as nx
import matplotlib.pyplot as plt
from queue import LifoQueue

class NN:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_edges_nodes(self, n: int, edges: list):
        self.graph.add_nodes_from([(x+1) for x in range(n)])
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])

    def two_optimization(self, tour, edges):
        improvement = True
        while improvement:
            improvement = False
            for i in range(1, len(tour) - 2):
                for j in range(i + 2, len(tour)):
                    if j - i == 1:
                        continue 
                    new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                    new_edges = self.construct_edges(new_tour)
                    if new_edges == [] :
                        continue
                    if self.total_length(new_edges) < self.total_length(edges):
                        tour = new_tour
                        edges = new_edges
                        improvement = True

        return tour, edges

    def search(self, n: int):
        tour = [1]
        edges = []
        while len(tour) < n:
            i = tour[-1]
            neigh = [self.graph.edges[i, j]['weight'] for j in self.graph.neighbors(i) if j not in tour]
            if len(neigh) == 0:
                break
            min_length = min(neigh)
            nns = [j for j in self.graph.neighbors(i) if j not in tour and self.graph.edges[i, j]['weight'] == min_length]
            tour.append(nns[0])
            edges.append((i, nns[0], self.graph.edges[i, nns[0]]['weight']))
        # Apply 2-optimization
        tour, edges = self.two_optimization(tour, edges)

        # print(tour)
        # print(edges)

        last_edge = edges[-1]
        if (last_edge[1], 1) in self.graph.edges:
            edges.append((last_edge[1], 1, self.graph.edges[last_edge[1], 1]['weight']))
        # print(edges)
        return edges

    
    def total_length(self, edges):
        return sum(edge[2] for edge in edges)

    
    def construct_edges(self, tour):
        edges = []
        for i in range(len(tour) - 1):
            try:
                edges.append((tour[i], tour[i + 1], self.graph.edges[tour[i], tour[i + 1]]['weight']))
            except:
                return []
        return edges


