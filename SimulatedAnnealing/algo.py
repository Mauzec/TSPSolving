import networkx as nx
import matplotlib.pyplot as plt
import random
import math


class SA:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_edges_nodes(self, n: int, edges: list):
        self.graph.add_nodes_from([(x+1) for x in range(n)])
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])
    
            
    def initial_solution(self, n: int):
        tour = list(range(1, n+1))
        random.shuffle(tour)
        return tour

    def calculate_cost(self, tour):
        # Рассчитываем общую стоимость маршрута
        cost = 0
        for i in range(len(tour) - 1):
            if self.graph.has_edge(tour[i], tour[i+1]):
                cost += self.graph[tour[i]][tour[i+1]]['weight']
            else: return -1
        return cost

    def anneal(self, n, init_temp=10000000, stop_temp=0.0000000001,cooling_rate=0.99999995, iterations=10000000):
        curr_tour = []
        curr_cost = -1
        while curr_cost == -1:
            curr_tour = self.initial_solution(n)
            curr_cost = self.calculate_cost(curr_tour)
        

        best_tour = curr_tour.copy()
        best_cost = curr_cost

        temp = init_temp

        print('Initial tour, weight:', curr_tour, curr_cost)
        
        iteration = 1

        while temp >= stop_temp and iteration < iterations:
            new_tour = curr_tour.copy()
            i, j = random.sample(range(n), 2)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_cost = self.calculate_cost(new_tour)

            if new_cost == -1: continue

            if random.random() < self.accept(new_cost, curr_cost, temp):
                curr_tour = new_tour.copy()
                curr_cost = new_cost

            if curr_cost < best_cost:
                best_tour = curr_tour.copy()
                best_cost = curr_cost

            iteration += 1
            temp *= cooling_rate

        best_edges = []
        for i in range(len(best_tour) - 1):
            best_edges.append((best_tour[i], best_tour[i+1], 
                               self.graph[best_tour[i]][best_tour[i+1]]['weight']))
        
        if self.graph.has_edge(best_tour[-1], best_tour[0]):
            best_cost += self.graph[best_tour[-1]][best_tour[0]]['weight']
            best_edges.append((best_tour[-1], best_tour[0], 
                               self.graph[best_tour[-1]][best_tour[0]]['weight']))
            best_tour.append(best_tour[0])

        return best_tour, best_cost, best_edges


    def accept(self, new_cost, curr_cost, temp):
        if new_cost < curr_cost:
            return 1.0
        return math.exp(-abs(new_cost - curr_cost) / temp)

if __name__ == '__main__':
    sa = SA()
    sa.add_edges_nodes(4, [{'from': 1, 'to': 2, 'weight': 10},
                        {'from': 2, 'to': 3, 'weight': 15},
                        {'from': 3, 'to': 4, 'weight': 20},
                        {'from': 4, 'to': 1, 'weight': 25},
                        {'from': 3, 'to': 1, 'weight': 10}])

    best_tour, best_cost, best_edges = sa.anneal(4)
    print("Best Solution:", best_tour)
    print("Best Cost:", best_cost)
    print("Best Edges:", best_edges)