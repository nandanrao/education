import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice
import os

def network_group(g, directed = True, folder = 'educatalyst/Data/Raw/1612_jesuites'):
    path = os.path.join(folder, g+'_1612_q6.csv')
    df = pd.read_csv(path)
    nodes = df['User Id'].unique()
    friends = [[int(n) for n in i if not np.isnan(n)] for i in df.iloc[:, 4:9].as_matrix()]
    edges = [[(n,f) for f in fs] for n,fs in zip(nodes, friends)]
    edges = [e for i in edges for e in i]
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def get_out_of_sample_nodes(g):
    nodes = set([e[0] for e in g.edges()])
    in_nodes = set([e[1] for e in g.edges()])
    return in_nodes.difference(nodes)


def get_girvan(g, n):
    girv = nx.girvan_newman(g)
    return list(islice(girv, 0, n))[n - 1]
