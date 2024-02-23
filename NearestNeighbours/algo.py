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
    
    def two(self, tour, edges):
        improved = True
        n = len(tour)
        while improved:
            improved = False
            for i in range(n):
                for j in range(i + 1, n):
                    new1 = (tour[i],tour[j])
                    new2 = (tour[i+1],tour[(j+1)%n])
                    cur1 = (tour[i], tour[i + 1])
                    cur2 = (tour[j], tour[(j+1)%n])
                    if not (self.graph.has_edge(*new1) and self.graph.has_edge(*new2)):
                        continue
                    if not (self.graph.has_edge(*cur2)):
                        continue
    
                    cur_w = self.graph.edges[*cur1]['weight'] + self.graph.edges[*cur2]['weight']
                    new_w = self.graph.edges[*new1]['weight'] + self.graph.edges[*new2]['weight']

                    if new_w < cur_w:
                        print("swapping edges", cur1, cur2, "with", new1, new2)
                        tour[i + 1: j+1] = tour[i + 1: j+1][::-1]
                        improved = True

                        edges = [ (tour[i - 1], tour[i]) for i in range(n) ]
        return tour, edges

    def two_optimization(self,nedges):
        edges = nedges[:]
        improvement = True
        i = 0
        while improvement:
            improvement = False
            for i in range(len(edges) - 2):
                for j in range(i + 2, len(edges)):
                    if not(self.graph.has_edge(edges[i][1], edges[j][0])
                        and self.graph.has_edge(edges[j][1], edges[i][0])):
                        continue
                    alter = (
                        edges[i][2] + self.graph.edges[edges[i][1], edges[j][0]]['weight']
                      + edges[j][2] + self.graph.edges[edges[j][1], edges[i][0]]['weight']
                    )
                    current = edges[i][2] + edges[j][2]
                    if alter < current:
                        edges[i + 1: j] = reversed[edges[i + 1 : j]]
                        improvement = True
                        print('improve!', alter)
            i += 1
        print('two:', i)
        return edges
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
        return best_candidates[0]
    def search(self, n: int, heuristic=True):
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

        last_edge = edges[-1]
        if (last_edge[1], 1) in self.graph.edges:
            edges.append((last_edge[1], 1, self.graph.edges[last_edge[1], 1]['weight']))
            tour.append(tour[0])

        # print(edges)
        # print("networkx:", nx.algorithms.approximation.traveling_salesman_problem(self.graph))
        return edges

    
    def total_weight(self, edges):
        return sum(edge[2] for edge in edges)

    
    def construct_edges(self, tour):
        edges = []
        for i in range(len(tour) - 1):
            try:
                edges.append((tour[i], tour[i + 1], self.graph.edges[tour[i], tour[i + 1]]['weight']))
            except:
                return []
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