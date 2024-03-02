import json
from algo import SA
from test_nn import NN
import matplotlib.pyplot as plt

def read_json(name="test_graphs/test_1.json"):
    edges = []
    with open(f"{name}", 'r') as file:
        data = json.load(file)
        for i in range(len(data["edges"])):
            edges.append(data["edges"][i])
    return len(data['edges']), edges

sa_weights=[]

iters = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
nn_weights = [817 for i in iters]
for i in iters:
    n, edges = read_json(name=f"test_graphs/test_{400}.json")
    # nn = NN()
    # nn.add_edges_nodes(400, edges)
    # nn_edges = nn.search(400, heuristic=False)
    # nn_weight = 0
    # for _,_,w in nn_edges:
    #     nn_weight += w

    sa = SA()
    sa.add_edges_nodes(400, edges)
    _, sa_weight, sa_edges, _, _= sa.anneal(400, iterations=i)

    if sa_weight > 817:
        print(i, sa_weight, 817, 'False')
    elif sa_weight == 817:
        print(i, sa_weight, 817, 'Equal')
    else:
        print(i, sa_weight, 817)
    # nn_weights.append(nn_weight)
    sa_weights.append(sa_weight)
    
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(iters, sa_weights, color='blue', linewidth=1.5, linestyle='-')
ax.plot(iters, nn_weights, color='green', linewidth=1.5, linestyle='-')
ax.grid()
ax.set_xlabel(r'Итерация', fontsize=11)
ax.set_ylabel(r'Сумма', fontsize=11)
ax.legend(['МАИО', 'Метод ближайшего соседа'])

print('sum:', sum(sa_weights), sum(nn_weights))
plt.show()