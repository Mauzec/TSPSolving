import networkx as nx
import matplotlib.pyplot as plt
import random

class NN:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_edges_nodes(self, n: int, edges: list):
        self.graph.add_nodes_from([(x+1) for x in range(n)])
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])
    
    def heuristic_selection(self, i, candidates):
        # Добавим эвристику для выбора следующей вершины
        weights = [self.graph.edges[i, j]['weight'] for j in candidates]
        degrees = [self.graph.degree(j) for j in candidates]
        reverse_w = [1 / self.graph.edges[i, j]['weight'] if self.graph.edges[i, j]['weight'] != 0 else 0 for j in candidates]
        diversity = 0.1
        scores = [0.4 * w + 0.3 * d + 0.3 * c + diversity * random.random() for w, d, c in zip(weights, degrees, reverse_w)]

        # Выбираем вершину с наилучшим комбинированным показателем
        min_score = min(scores)
        best_candidates = [candidates[i] for i in range(len(candidates)) if scores[i] == min_score]
        return random.choice(best_candidates)
    
    def search(self, n: int, heuristic=False, tour_return=False):
        tour = [1]
        edges = []

        while len(tour) < n:
            i = tour[-1]
            neighbors = list(self.graph.neighbors(i))
            candidates = [j for j in neighbors if j not in tour]

            if len(candidates) == 0:
                break

            # # Выбираем следующую вершину на основе эвристики
            s = None
            if heuristic:
                s = self.heuristic_selection(i, candidates)
            else:
                s = min([self.graph.edges[i, j]['weight'] for j in candidates])
                s = [j for j in candidates if s == self.graph.edges[i, j]['weight']][0]
            tour.append(s)
            edges.append((i, s, self.graph.edges[i, s]['weight']))


        # print(edges)
        # print("networkx:", nx.algorithms.approximation.traveling_salesman_problem(self.graph))
        if (tour[-1] != 1) and (tour[-1], 1) in self.graph.edges:
            edges.append((tour[-1], 1, self.graph[tour[-1]][1]['weight']))
            tour.append(1)
        if tour_return: return tour
        return edges

if __name__ == '__main__':
    nn = NN()
    nn.graph = nx.gnm_random_graph(20, 200, directed=True)
    import random
    my_pos = {i: (random.random(), random.random()) for i in nn.graph.nodes}
    nx.draw(nn.graph, pos=my_pos)
    
    for (i, j, w) in nn.graph.edges(data=True):
        w['weight'] = random.randint(1, 50)

    plt.show()

    nn.search(20)
    nx.draw(nn.graph, pos=my_pos)
    plt.show()