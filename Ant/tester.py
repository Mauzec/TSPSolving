import json
from algo import ANTA
import matplotlib.pyplot as plt
from test_nn import NN
from test_sa import SA
from time import time

def read_json(name="test_graphs/test_1.json"):
    edges = []
    with open(f"{name}", 'r') as file:
        data = json.load(file)
        for i in range(len(data["edges"])):
            edges.append(data["edges"][i])
    return len(data['edges']), edges

sa_costs=[]
nn_costs=[]
anta_costs=[]
iters = []; iters.append(list(range(10000, 100000, 1000)))
bads = {}

sa_times=[]
nn_times=[]
anta_times=[]

for i in range(5,201):
    n, edges = read_json(name=f"test_graphs/test_{i}.json")
    anta = ANTA(n=i)
    nn = NN()
    sa = SA()
    anta.add_edges_nodes(edges)
    nn.add_edges_nodes(i, edges)
    sa.add_edges_nodes(i, edges)
    time0 = time()
    _, anta_cost, _ = anta.acs()
    time1 = time(); anta_times.append(time1-time0)
    
    time0 = time()
    nn_edges = nn.search(i)
    nn_cost = 0
    for _, _, c in nn_edges:
        nn_cost += c
    time1 = time(); nn_times.append(time1-time0)

    time0 = time()
    _, sa_cost, _, _, _ = sa.anneal(i, iterations=1000)
    time1 = time(); sa_times.append(time1-time0)
    if (anta_cost >= sa_cost or anta_cost >= nn_cost):
        print(i, 'NSA', nn_cost, sa_cost, anta_cost, 'TIME:', nn_times[i-5], sa_times[i-5], anta_times[i-5], 'BAD')
        bads[i] = (nn_cost, sa_cost, anta_cost)
    else:
        print(i, 'NSA', nn_cost, sa_cost, anta_cost, 'TIME:', nn_times[i-5], sa_times[i-5], anta_times[i-5])
    nn_costs.append(nn_cost)
    sa_costs.append(sa_cost)
    anta_costs.append(anta_cost)



fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(range(5, 201), nn_costs, color='blue', linewidth=2.0, linestyle='-', label='NN', zorder=2)
ax.plot(range(5, 201), sa_costs, color='green', linewidth=2.0, linestyle='-', label='SA', zorder=2)
ax.plot(range(5, 201), anta_costs, color='red', linewidth=2.0, linestyle='-', label='ANT', zorder=2)
for n, cc in bads.items():
    print('BAD:', n, *cc)
    plt.scatter([n], cc[2], color='black', marker='x',zorder=3,s=50,linewidths=2)
ax.grid()
ax.set_xlabel(r'Номер теста', fontsize=11)
ax.set_ylabel(r'Сумма', fontsize=11)
ax.legend(['Метод ближ. соседей', 'Метод имитации отж.', 'Муравьин. алгоритм', 'Точки неудачи'])

plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(range(5, 201), nn_times, color='blue', linewidth=2.0, linestyle='-', label='NN', zorder=2)
ax.plot(range(5, 201), sa_times, color='green', linewidth=2.0, linestyle='-', label='SA', zorder=2)
ax.plot(range(5, 201), anta_times, color='red', linewidth=2.0, linestyle='-', label='ANT', zorder=2)
ax.grid()
ax.set_xlabel(r'Номер теста', fontsize=11)
ax.set_ylabel(r'Время', fontsize=11)
ax.legend(['Метод ближ. соседей', 'Метод имитации отж.', 'Муравьин. алгоритм', 'Точки неудачи'])

plt.show()