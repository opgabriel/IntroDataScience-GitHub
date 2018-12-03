import random
import networkx as nx

class MHRW():
    def __init__(self):
        self.G1 = nx.Graph()
        
    def mhrw(self,G,node,size):
        dictt = {}
        node_list = set()
        node_list.add(node)
        parent_node = node_list.pop()
        dictt[parent_node] = parent_node
        degree_p = G.degree(parent_node)
        related_list = list(G.neighbors(parent_node))
        node_list.update(related_list)

        while(len(self.G1.nodes()) < size):
            if(len(node_list) > 0):
                child_node = node_list.pop()
                p =  round(random.uniform(0,1),4)
                if(child_node not in dictt):
                    related_listt = list(G.neighbors(child_node))
                    degree_c = G.degree(child_node)
                    dictt[child_node] = child_node
                    if(p <= min(1,degree_p/degree_c) and child_node in list(G.neighbors(parent_node))):
                        self.G1.add_edge(parent_node,child_node)
                        parent_node = child_node
                        degree_p = degree_c
                        node_list.clear()
                        node_list.update(related_listt)
                    else:
                        del dictt[child_node]


            # node_list set becomes empty or size is not reached 
            # insert some random nodes into the set for next processing
            else:
                node_list.update(random.sample(set(G.nodes())-set(self.G1.nodes()),3))
                parent_node = node_list.pop()
                G.add_node(parent_node)
                related_list = list(G.neighbors(parent_node))
                node_list.clear()
                node_list.update(related_list)
        return self.G1

print("Reading graph...")
G = nx.read_edgelist('data/JS_topological_network.csv', delimiter=',')
#G = nx.read_edgelist('data/RB_sample_network.csv', delimiter=',')

nodes = nx.number_of_nodes(G)
size = int(nodes * 0.9)
#random_node = list(G.nodes())[0]
random_node = random.choice(list(G.nodes))
print(random_node)

print("Executing MHRW...")
sample = MHRW()
sample.mhrw(G, random_node, size)

print("Writing sample network...")
nx.write_edgelist(sample.G1, "data/JS_sample_network_90.csv", delimiter=",", data=False)

G.clear()
G = sample.G1

DG = nx.degree(G)

num_nodes = 0
sum_degree = 0

for i in DG:
	num_nodes += 1
	sum_degree += i[1]

print("Grau da rede:", sum_degree)
print("Grau médio:", (sum_degree/num_nodes))
print("Nodes:", nx.number_of_nodes(G))
print("Edges:", nx.number_of_edges(G))
print("Density:", nx.density(G))

AC = nx.average_clustering(G)
print("Average Clustering:", AC)

# Informações do maior componente conectado
print("Generating giant component...")
giant = max(nx.connected_component_subgraphs(G), key=len)
print("Nodes Giant:", nx.number_of_nodes(giant))
print("Edges Giant:", nx.number_of_edges(giant))

