
dataset = 'page_links_en_2015'
index = {}

with open('datasets/dbpedia/%s_index.txt' %dataset, 'r') as index_read:
	for line in index_read:

		line_split = line.split(' ')

		index[line_split[0]] = line_split[1].strip('\n')


with open('datasets/dbpedia/graphs/%s.edgelist' %dataset, 'r') as edgelist_read:

	with open('datasets/dbpedia/graphs/%s_indexed.edgelist' %dataset, 'w') as indexed_edgelist:

		for line in edgelist_read:

			if line[0] != "#":

				line_split = line.split(' ')

				node_left = line_split[0]

				node_left_index = index[node_left]

				node_right = line_split[1].strip('\n')

				node_right_index = index[node_right]

				indexed_edgelist.write('%s %s\n' %(node_left_index, node_right_index))



