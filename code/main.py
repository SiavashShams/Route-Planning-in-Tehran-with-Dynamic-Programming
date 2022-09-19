import pandas as pd
import networkx as nx
from gurobipy import *
import matplotlib.pyplot as plt

data = pd.read_csv("Dataset2.csv", sep=";", on_bad_lines='skip', header=None)
data.columns = ["index", "Name", "Latitude,Longitude", "Neighbours", "Distances"]
links = data["Neighbours"]
Destination = int(input("Please enter destination node: "))
Origin = int(input("Please enter origin node: "))

NUM_NODES = 10
cost = data["Distances"]
costt = {}
j = 1
linkss = tuplelist()
# preparing links and costs
for i in links.values.tolist():
    jj = 0
    for k in range(len(i.split(","))):
        costt[j, int(i.split(",")[k])] = int(cost[j - 1].split(",")[jj])
        linkss.append((j, int(i.split(",")[k])))
        jj = jj + 1
    j = j + 1

links = tuplelist()
cost = {}
links = linkss
cost = costt
# define the model
m = Model('SP')
x = m.addVars(links, obj=cost, name="flow")
# add constraints
for i in range(1, NUM_NODES + 1):
    m.addConstr(sum(x[i, j] for i, j in links.select(i, '*')) - sum(x[j, i] for j, i in links.select('*', i)) ==
                (1 if i == Origin else -1 if i == Destination else 0), 'node%s_' % i)

m.optimize()
if m.status == GRB.Status.OPTIMAL:
    print("We are going form place: ", Origin, "with coordinates: ", data.loc[Origin - 1]["Latitude,Longitude"],
          " To: ",
          Destination, "with coordinates: ", data.loc[Destination - 1]["Latitude,Longitude"])
    print('The optimal route is:')
    for i, j in links:
        if j > i:
            if (x[i, j].x > 0):
                print(i, " --> ", j)
        else:
            if (x[i, j].x > 0):
                print(j, " <-- ", i)

    G = nx.DiGraph()
    list_nodes = list(range(1, NUM_NODES + 1))
    G.add_nodes_from(list_nodes)
    for i, j in links:
        G.add_edge(i, j)

    # Adding the position attribute to each node
    node_pos = {1: (0, 0), 2: (2, 2), 3: (2, -2), 4: (5, 2), 5: (5, -2), 6: (8, 2), 7: (8, -2), 8: (11, 2), 9: (11, -2),
                10: (13, 0)}

    # Create a list of edges in shortest path
    red_edges = [[(i, j), (j, i)] for i, j in links if x[i, j].x > 0]
    red_edges = [item for sublist in red_edges for item in sublist]
    # Create a list of nodes in shortest path
    shortest_path = [i for i, j in links if x[i, j].x > 0]
    shortest_path.append(Destination)

    # If the node is in the shortest path, set it to red, else set it to grey color
    node_col = ['grey' if not node in shortest_path else 'red' for node in G.nodes()]
    # If the edge is in the shortest path set it to red, else set it to black color
    edge_col = ['red' if edge in red_edges else 'black' for edge in G.edges()]
    # Draw the nodes
    nx.draw_networkx(G, node_pos, node_color=node_col, node_size=450)
    # Draw the edges
    nx.draw_networkx_edges(G, node_pos, edge_color=edge_col)
    plt.axis('off')
    plt.show()

else:
    print("Optimal solution not found")
