import networkx as nx
from itertools import chain

#this script is meant to remove all the pages with fewer than 5 incoming links
#noise reduction process

G = nx.read_edgelist('../datasets/dbpedia_resources_wiki.edgelist', nodetype=int, create_using=nx.DiGraph())
print 'read graph'

remove_nodes_out = (node for node,degree in G.out_degree().iteritems() if degree == 0) #nodes with out_degree = 0

remove_nodes_in = (node for node,degree in G.in_degree().iteritems() if degree == 0) #nodes with in_degree = 0

remove_nodes = chain(remove_nodes_out, remove_nodes_in)

G.remove_nodes_from(remove_nodes)

print 'graph has %d nodes and %d edges' %(len(G.nodes()), len(G.edges()))


print "writing graph"

nx.write_edgelist(G,'../graph/dbpedia_resources_wiki_reduced_1_out_1_in.edgelist', data = False)


