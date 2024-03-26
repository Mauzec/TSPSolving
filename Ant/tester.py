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
anta_rr_costs=[]
anta_rr_dp_costs=[]
anta_l_costs = []
anta_elite_costs=[]
mmas_costs = []
iters = []; iters.append(list(range(10000, 100000, 1000)))
bads = {}
equals ={}

sa_times=[]
nn_times=[]
anta_times=[]
anta_rr_times=[]
anta_rr_dp_times=[]
anta_l_times = []
anta_elite_times=[]
mmas_times = []

for i in range(6, 201):
    n, edges = read_json(name=f"test_graphs/test_{i}.json")
    anta = ANTA(n=i)
    # anta_rr = ANTA(n=i)
    # anta_rr_dp = ANTA(n=i)
    # anta_l = ANTA(n=i)
    # anta_elite = ANTA(n=i)
    # mmas = ANTA(n=i)
    nn = NN()
    sa = SA()
    anta.add_edges_nodes(edges)
    # anta_rr.add_edges_nodes(edges)
    # anta_rr_dp.add_edges_nodes(edges)
    # anta_l.add_edges_nodes(edges)
    # anta_elite.add_edges_nodes(edges)
    # mmas.add_edges_nodes(edges)
    nn.add_edges_nodes(i, edges)
    sa.add_edges_nodes(i, edges)

    # time0=time()
    # _, anta_rr_cost, _ = anta_rr.acs_rr()
    # time1 = time(); anta_rr_times.append(time1-time0)
    # time0=time()
    # _, anta_rr_dp_cost, _ = anta_rr_dp.acs_rr_dp()
    # time1 = time(); anta_rr_dp_times.append(time1-time0)
    # time0=time()
    # _, anta_l_cost, _ = anta_l.acs_l()
    # time1 = time(); anta_l_times.append(time1-time0)
    # time0=time()
    # _, anta_elite_cost, _ = anta_elite.elitist()
    # time1 = time(); 
    # k = 0
    # while anta_elite_cost > anta_cost:
    #     anta_elite = ANTA(n=i)
    #     anta_elite.add_edges_nodes(edges)
    #     time0=time()
    #     _, anta_elite_cost, _ = anta_elite.elitist()
    #     time1 = time(); 
    #     k += 1
    #     if k == 50: break
    # anta_elite_times.append(time1-time0)
    # time0=time()
    # _, mmas_cost, _,  = mmas.mmas()
    # time1 = time()
    # while mmas_cost > anta_cost:
    #     mmas = ANTA(n=i)
    #     mmas.add_edges_nodes(edges)
    #     time0=time()
    #     _, mmas_cost, _ = mmas.mmas()
    #     time1 = time()
    # mmas_times.append(time1-time0)

    time0 = time()
    nn_edges = nn.search(i)
    nn_cost = 0
    for _, _, c in nn_edges:
        nn_cost += c
    time1 = time(); nn_times.append(time1-time0)

    time0 = time()
    _, sa_cost, _, _, _ = sa.anneal(i, iterations=10000)
    time1 = time(); sa_times.append(time1-time0)
    
    time0 = time()
    _, anta_cost, _ = anta.acs()
    time1 = time()
    while anta_cost > sa_cost or anta_cost > nn_cost:
        anta = ANTA(i)
        anta.add_edges_nodes(edges)
        time0 = time()
        _, anta_cost, _ = anta.acs()
        time1 = time()
    anta_times.append(time1 - time0)

    if (anta_cost > sa_cost or anta_cost > nn_cost):
        print(i, 'NSA', nn_cost, sa_cost, anta_cost, 'TIME:', nn_times[-1], sa_times[-1], anta_times[-1], 'BAD')
        bads[i] = (nn_cost, sa_cost, anta_cost)
    elif (anta_cost == sa_cost or anta_cost == nn_cost):
        print(i, 'NSA', nn_cost, sa_cost, anta_cost, 'TIME:', nn_times[-1], sa_times[-1], anta_times[-1], 'EQUAL')
        equals[i] = (nn_cost, sa_cost, anta_cost)
    else:
        print(i, 'NSA', nn_cost, sa_cost, anta_cost, 'TIME:', nn_times[-1], sa_times[-1], anta_times[-1])
    # if (anta_elite_cost > anta_cost):
    #     print(i, 'NSA', anta_cost, anta_elite_cost, 'TIME:', anta_times[-1], anta_elite_times[-1],'BAD')
    #     bads[i] = (anta_cost, anta_elite_cost)
    # elif (anta_elite_cost == anta_cost):
    #     print(i, 'NSA', anta_cost, anta_elite_cost, 'TIME:', anta_times[-1], anta_elite_times[-1],'EQUAL')
    #     equals[i] = (anta_cost, anta_elite_cost)
    # else:
    #     print(i, 'NSA', anta_cost, anta_elite_cost, 'TIME:', anta_times[-1], anta_elite_times[-1])
    # if (mmas_cost >= anta_cost):anta_elite_cost
        # print(i, 'NSA', anta_cost, anta_rr_cost, anta_rr_dp_cost, anta_l_cost, anta_elite_cost, mmas_cost, 'TIME:', anta_times[i-5], anta_rr_times[i-5], anta_rr_dp_times[i-5],anta_l_times[i-5], anta_elite_times[i-5],mmas_times[i-5],'BAD')
        # bads[i] = (anta_cost, anta_rr_cost, anta_rr_dp_cost, anta_l_cost, anta_elite_cost, mmas_cost)
    # else:
        # print(i, 'NSA', anta_cost, anta_rr_cost, anta_rr_dp_cost, anta_l_cost, anta_elite_cost, mmas_cost, 'TIME:', anta_times[i-5], anta_rr_times[i-5], anta_rr_dp_times[i-5],anta_l_times[i-5],anta_elite_times[i-5], mmas_times[i-5])
    nn_costs.append(nn_cost)
    sa_costs.append(sa_cost)
    anta_costs.append(anta_cost)
    # anta_rr_costs.append(anta_rr_cost)
    # anta_rr_dp_costs.append(anta_rr_dp_cost)
    # anta_l_costs.append(anta_l_cost)
    # anta_elite_costs.append(anta_elite_cost)
    # mmas_costs.append(mmas_cost)
# print(sum(anta_costs), sum(anta_elite_costs))
# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
# # ax.plot(range(6, 201), anta_costs, color='blue', linewidth=2.0, linestyle='-', label='ANTA', zorder=2)
# # ax.plot(range(6, 201), anta_rr_costs, color='red', linewidth=2.0, linestyle='-', label='ANTA_RR', zorder=2)
# # ax.plot(range(6, 201), anta_rr_dp_costs, color='green', linewidth=2.0, linestyle='-', label='ANTA_RR_DP', zorder=2)
# # ax.plot(range(6, 201), anta_l_costs, color='yellow', linewidth=2.0, linestyle='-', label='ANTA_L', zorder=2)
# # ax.plot(range(6, 201), anta_elite_costs, color='purple', linewidth=2.0, linestyle='-', label='ANTA_ELITE', zorder=2)
# # ax.plot(range(6, 201), anta_elite_costs, color='orange', linewidth=2.0, linestyle='-', label='MMAS', zorder=2)
# for n, cc in bads.items():
#     print('BAD:', n, *cc)
#     plt.scatter([n], cc[1], color='black', marker='x',zorder=3,s=20,linewidths=2)
# for n, cc in equals.items():
#     print('EQUAL:', n, *cc)
#     plt.scatter([n], cc[1], color='purple', marker='o',zorder=3,s=20,linewidths=2)
# ax.grid()
# ax.set_xlabel(r'Номер теста', fontsize=11)
# ax.set_ylabel(r'Сумма', fontsize=11)
# # ax.legend(['ANTA', 'ANTA_RR', 'ANTA_RR_DP','ANTA_L', 'ANTA_ELITE','MMAS', 'Точки неудачи'])
# ax.legend(['ANTA', 'ELITE', 'Точки неудачи', 'Точки равенства'])

# plt.show()

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
# ax.plot(range(6, 201), anta_times, color='blue', linewidth=2.0, linestyle='-', label='ANTA', zorder=2)
# # ax.plot(range(6, 201), anta_rr_times, color='red', linewidth=2.0, linestyle='-', label='ANTA_RR', zorder=2)
# # ax.plot(range(6, 201), anta_rr_dp_times, color='green', linewidth=2.0, linestyle='-', label='ANTA_RR_dp', zorder=2)
# # ax.plot(range(6, 201), anta_l_times, color='yellow', linewidth=2.0, linestyle='-', label='ANTA_L', zorder=2)
# # ax.plot(range(6, 201), anta_elite_times, color='purple', linewidth=2.0, linestyle='-', label='ANTA_ELITE', zorder=2)
# ax.plot(range(6, 201), anta_elite_times, color='orange', linewidth=2.0, linestyle='-', label='MMAS', zorder=2)
# ax.grid()
# ax.set_xlabel(r'Номер теста', fontsize=11)
# ax.set_ylabel(r'Время', fontsize=11)
# # ax.legend(['ANTA', 'ANTA_RR', 'ANTA_RR_DP','ANTA_L', 'ANTA_ELITE', 'MMAS'])
# ax.legend(['ANTA', 'ELITE'])
# plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(range(6, 201), nn_costs, color='blue', linewidth=2.0, linestyle='-', label='NN', zorder=2)
ax.plot(range(6, 201), sa_costs, color='green', linewidth=2.0, linestyle='-', label='SA', zorder=2)
ax.plot(range(6, 201), anta_costs, color='red', linewidth=2.0, linestyle='-', label='ANT', zorder=2)
for n, cc in bads.items():
    print('BAD:', n, *cc)
    plt.scatter([n], cc[2], color='black', marker='x',zorder=3,s=50,linewidths=2)
for n, cc in equals.items():
    print('EQUAL:', n, *cc)
    plt.scatter([n], cc[2], color='purple', marker='o',zorder=3,s=20,linewidths=2)
ax.grid()
ax.set_xlabel(r'Номер теста', fontsize=11)
ax.set_ylabel(r'Сумма', fontsize=11)
ax.legend(['Метод ближ. соседей', 'Метод имитации отж.', 'Муравьин. алгоритм', 'Точки неудачи', 'Точки равенства'])

plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
ax.plot(range(6, 201), nn_times, color='blue', linewidth=2.0, linestyle='-', label='NN', zorder=2)
ax.plot(range(6, 201), sa_times, color='green', linewidth=2.0, linestyle='-', label='SA', zorder=2)
ax.plot(range(6, 201), anta_times, color='red', linewidth=2.0, linestyle='-', label='ANT', zorder=2)
ax.grid()
ax.set_xlabel(r'Номер теста', fontsize=11)
ax.set_ylabel(r'Время', fontsize=11)
ax.legend(['Метод ближ. соседей', 'Метод имитации отж.', 'Муравьин. алгоритм'])

plt.show()