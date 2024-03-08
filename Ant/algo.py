import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from copy import deepcopy


class ANTA:
    def __init__(self, n: int, colony_size=15, alpha=1.0, beta=3, rho=0.1, initial_pheromone=1.0, steps=150) -> None:
        self.graph = nx.DiGraph()
        self.pheromones = dict()
        self.colony_size = colony_size
        # if n < 200: self.colony_size = 25
        # elif 200 <= n < 400: self.colony_size = 50
        # else: self.colony_size = 100
        self.rho = rho
        self.initial_pheremone = initial_pheromone
        self.steps = steps
        self.num_nodes = n
        self.alpha = alpha
        self.beta = beta
        # print('n alpha beta rho, colonysize steps')
        # print(n, alpha, beta, rho, colony_size, steps)
        self.global_best_tour = []
        self.global_best_cost = float('inf')
        

    def add_edges_nodes(self, edges: list):
        self.graph.add_nodes_from([(x+1) for x in range(self.num_nodes)])
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])
        self.pheromones = {(i, j): self.initial_pheremone for i, j in self.graph.edges} 
    
    def ant_find_tour(self):
        tour = [random.randint(1, self.num_nodes)]
        cost = 0
        while len(tour) < self.num_nodes:
            curr = tour[-1]
            available_neighbors = [n for n in self.graph.neighbors(tour[-1]) if n not in tour]
            if len(available_neighbors) == 0: break

            pheromone_distance_pairs = [(self.pheromones[curr, neighbor], 1 / self.graph[curr][neighbor]['weight']) for neighbor in available_neighbors]
            summary_wish = sum((pheromone ** self.alpha * distance ** self.beta) for pheromone, distance in pheromone_distance_pairs)
            if summary_wish == 0: break
            probabilities = [(pheromone ** self.alpha * distance ** self.beta) / summary_wish for pheromone, distance in pheromone_distance_pairs]

            r = random.uniform(0, 1)
            cprob = 0
            for i, prob in enumerate(probabilities):
                cprob += prob
                if r <= cprob:
                    cost += self.graph[curr][available_neighbors[i]]['weight']
                    tour.append(available_neighbors[i])
                    break
        if len(tour) == self.num_nodes and self.graph.has_edge(tour[-1], tour[0]):
            cost += self.graph[tour[-1]][tour[0]]['weight']
            return tour, cost
        else: return [], float('inf')
    
    def add_pheromone(self, tour, weight):
        padd = 1 / weight
        for i in range(self.num_nodes - 1):
            edge = (tour[i], tour[i+1])
            self.pheromones[edge] = self.pheromones[edge] + padd 
        edge = (tour[-1], tour[0])
        self.pheromones[edge] = self.pheromones[edge] + padd 

    def acs(self):
        for step in range(self.steps):
            for _ in range(self.colony_size):
                ant_tour, ant_cost = self.ant_find_tour()
                if len(ant_tour) != 0:
                    self.add_pheromone(ant_tour, ant_cost)
                    if ant_cost < self.global_best_cost:
                        self.global_best_cost = ant_cost
                        self.global_best_tour = ant_tour.copy()
            
            for (i, j), p in self.pheromones.items():
                self.pheromones[i, j] = p * (1.0 - self.rho) 

        global_best_edges = [(self.global_best_tour[i], self.global_best_tour[i + 1], self.graph[self.global_best_tour[i]][self.global_best_tour[i+1]]['weight']) for i in range(len(self.global_best_tour) - 1)]
        global_best_edges.append((self.global_best_tour[-1], self.global_best_tour[0], self.graph[self.global_best_tour[-1]][self.global_best_tour[0]]['weight']))
        self.global_best_tour.append(self.global_best_tour[0])
        return self.global_best_tour, self.global_best_cost, global_best_edges

    def elitist(self):
        for step in range(self.steps):
            for _ in range(self.colony_size):
                ant_tour, ant_cost = self.ant_find_tour()
                if len(ant_tour) == self.num_nodes:
                    self.add_pheromone(ant_tour, ant_cost)
                    if ant_cost < self.global_best_cost:
                        self.global_best_cost = ant_cost
                        self.global_best_tour = ant_tour.copy()
            # Amout of pheromone depends upon the quality of the solution.
            self.add_pheromone(self.global_best_tour, self.global_best_cost)
            for (i, j), p in self.pheromones.items():
                self.pheromones[i, j] = p * (1.0 - self.rho) 

        global_best_edges = [(self.global_best_tour[i], self.global_best_tour[i + 1], self.graph[self.global_best_tour[i]][self.global_best_tour[i+1]]['weight']) for i in range(len(self.global_best_tour) - 1)]
        global_best_edges.append((self.global_best_tour[-1], self.global_best_tour[0], self.graph[self.global_best_tour[-1]][self.global_best_tour[0]]['weight']))
        self.global_best_tour.append(self.global_best_tour[0])
        return self.global_best_tour, self.global_best_cost, global_best_edges

if __name__ == '__main__':
    anta = ANTA()
    anta.add_edges_nodes(4, [{'from': 1, 'to': 2, 'weight': 10},
                        {'from': 2, 'to': 3, 'weight': 15},
                        {'from': 3, 'to': 4, 'weight': 20},
                        {'from': 4, 'to': 1, 'weight': 25}])

    best_tour, best_cost, best_edges = anta.ant_search()
    print("Best Solution:", best_tour)
    print("Best Cost:", best_cost)
    print("Best Edges", best_edges)