import networkx as nx
import pandas as pd

#this script is meant to remove all the pages with fewer than 5 incoming links
#noise reduction process

G0 = nx.read_edgelist('../graph/page_links_en.edgelist', nodetype=int)

G = nx.DiGraph()

for i,j in G0.edges():
    if G0.in_degree()[i] >= 5 and G0.in_degree()[j] >=5:
        G.add_edge(i,j)

nx.write_edgelist(G,'../graph/page_links_en_reduced.edgelist', data = False)