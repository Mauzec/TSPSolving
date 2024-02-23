import json
from algo import NN
import matplotlib.pyplot as plt

def read_json(name="test_graphs/test_1.json"):
    edges = []
    with open(f"{name}", 'r') as file:
        data = json.load(file)
        for i in range(len(data["edges"])):
            edges.append(data["edges"][i])
    return len(data['edges']), edges

s_weights=[]
nn_weights=[]
for i in range(30, 75):
    n, edges = read_json(name=f"test_graphs/test_{i}.json")
    nn = NN()
    nn.add_edges_nodes(i, edges)
    nn_edges = nn.search(i, heuristic=False)
    nn_weight = 0
    for _,_,w in nn_edges:
        nn_weight += w
    s_edges = nn.search(i)
    s_weight = 0
    for _,_,w in s_edges:
        s_weight += w
    while s_weight > nn_weight:
        s_edges = nn.search(i)
        s_weight = 0
        for _,_,w in s_edges:
            s_weight += w

    print(s_weight, nn_weight)
    nn_weights.append(nn_weight)
    s_weights.append(s_weight)
    
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(range(30, 75), s_weights, color='blue', linewidth=2.0, linestyle='-')
ax.plot(range(30, 75), nn_weights, color='green', linewidth=2.0, linestyle='-')
ax.grid()
ax.set_xlabel(r'Номер теста', fontsize=11)
ax.set_ylabel(r'Сумма', fontsize=11)
ax.legend(['Эвристический выбор', 'МБС'])
plt.show()