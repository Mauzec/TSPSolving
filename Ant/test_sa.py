import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from copy import deepcopy


class SA:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_edges_nodes(self, n: int, edges: list):
        self.graph.add_nodes_from([(x+1) for x in range(n)])
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])
    
            
    def initial_solution(self, n: int):
        # free_nodes = [(x + 1) for x in range(1, n)]
        # tour = [1]
        # curr_node = 1
        # while free_nodes:
        #     neigbours = [j for j in self.graph.neighbors(curr_node) if j in free_nodes]
        #     if len(neigbours) == 0: break
        #     next_node = min(neigbours, key=lambda x: self.graph[curr_node][x]['weight'])
        #     tour.append(next_node)
        #     free_nodes.remove(next_node)
        #     curr_node = next_node
        # return tour
        
        tour = []; tour.append(1)
        while len(tour) < n:
            i = tour[-1]
            neighbors = list(self.graph.neighbors(i))
            candidates = [j for j in neighbors if j not in tour]

            if len(candidates) == 0:
                break

            s = min([self.graph.edges[i, j]['weight'] for j in candidates])
            s = [j for j in candidates if s == self.graph.edges[i, j]['weight']][0]
            tour.append(s)

        v = random.choice(range(2, n+1))

        atour = []; atour.append(v)
        while len(atour) < n:
            i = atour[-1]
            neighbors = list(self.graph.neighbors(i))
            candidates = [j for j in neighbors if j not in atour]

            if len(candidates) == 0:
                break

            s = min([self.graph.edges[i, j]['weight'] for j in candidates])
            s = [j for j in candidates if s == self.graph.edges[i, j]['weight']][0]
            atour.append(s)
        if self.calculate_cost(tour) > self.calculate_cost(atour):
            return atour
        return tour
        tour = list(range(1, n+1))
        random.shuffle(tour)
        return tour
    def calculate_cost(self, tour):
        # Рассчитываем общую стоимость маршрута
        cost = 0
        for i in range(0, len(tour) - 1):
            if self.graph.has_edge(tour[i], tour[i+1]):
                cost += self.graph[tour[i]][tour[i+1]]['weight']
            else:
                # print('No edge weight:', tour[i], tour[i+1]) 
                return -1
        if tour[-1] != tour[0]:
            if self.graph.has_edge(tour[-1], tour[0]):
                cost += self.graph[tour[-1]][tour[0]]['weight']
            else: return -1
        return cost
    def anneal(self, n, init_temp=1, stop_temp=0.00001,cooling_rate=0.9999, iterations=5000):
        curr_tour = []
        curr_cost = -1
        while len(curr_tour) != n or curr_cost == -1:
            curr_tour = self.initial_solution(n)
            curr_cost = self.calculate_cost(curr_tour)
        assert curr_cost != -1
        assert len(curr_tour) == n
        best_tour = curr_tour
        best_edges = [(curr_tour[i], curr_tour[i+1], self.graph[curr_tour[i]][curr_tour[i+1]]['weight']) for i in range(len(curr_tour) - 1)]
        best_temp = 0
        best_cost = curr_cost
        iter_to_opt = 0
        temp = init_temp

        # print('Initial tour:', curr_tour)
        explored_tour = {tuple(curr_tour)}

        for i in range(iterations):

            new_tour = list(curr_tour)
            # l = random.randint(3, len(curr_tour) - 1)
            # k = random.randint(1, len(curr_tour) - 1)
            # while k <= l:
            #     l = random.randint(3, len(curr_tour) - 1)
            #     k = random.randint(1, len(curr_tour) - 1)   
            # new_tour[k: (k + l)] = reversed(new_tour[k: (k + l)])
            
            random_idxs = random.sample(range(0, n), 2)
            k, l = sorted(random_idxs)
            new_tour[k], new_tour[l] = new_tour[l], new_tour[k]

            # new_tour = list(curr_tour)
            # random_idxs = random.sample(range(0, n), 3)

            # for idx in random_idxs:
            #     new_tour[idx] = random.choice([x for x in range(1, n+1) if x not in new_tour])
            # new_tour = self.create_new_tour(curr_tour)

            # print(new_tour)
            tmp = tuple(new_tour)
            if tmp not in explored_tour:
                explored_tour.add(tmp)
                d1 = curr_cost
                d2 = self.calculate_cost(new_tour)
                
                if d2 != -1:
                    if d2 < d1 or (random.random() < np.exp(-(d2 - d1) / temp)):
                        curr_tour[k], curr_tour[l] = curr_tour[l], curr_tour[k]
                        # curr_tour = new_tour.copy()
                        curr_cost = d2
                                    
                    if curr_cost < best_cost:
                        best_tour = curr_tour.copy()
                        best_cost = curr_cost
                        best_temp = temp
                        iter_to_opt = i
                temp *= cooling_rate
                if temp < stop_temp: 
                    print("out", i)
                    break
            
        # print(best_tour)
        assert (best_tour[-1], best_tour[0]) in self.graph.edges
        assert (best_tour[-1] != best_tour[0])
        best_tour.append(best_tour[0])
        best_edges = [(best_tour[j], best_tour[j+1], self.graph[best_tour[j]][best_tour[j+1]]['weight']) for j in range(len(best_tour) - 1)]
        return best_tour, best_cost, best_edges, best_temp, iter_to_opt


if __name__ == '__main__':
    sa = SA()
    sa.add_edges_nodes(4, [{'from': 1, 'to': 2, 'weight': 10},
                        {'from': 2, 'to': 3, 'weight': 15},
                        {'from': 3, 'to': 4, 'weight': 20},
                        {'from': 4, 'to': 1, 'weight': 25}])

    best_tour, best_cost, best_edges, best_temp, best_iter = sa.anneal(4)
    print("Best Solution:", best_tour)
    print("Best Cost:", best_cost)
    print("Best Edges", best_edges)
    print("Best temp:", best_temp)
    print("Best iter:", best_iter)