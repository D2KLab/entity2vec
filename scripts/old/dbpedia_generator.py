dbpedia_instances = {}


with open('datasets/dbpedia_instances.txt') as f:
	for line in f.readlines():
		if line == '#':
			print 'commento'
			continue
		else:
			print line
			dbpedia_instances[line] = 1

dbpedia_graph = open('dbpedia_graph.ttl','w')

with open('datasets/mappingbased_objects_en.ttl') as g:
	for line in g.readlines():

		if line == '#':
			print 'commento'
			continue
		print line
		line = line.split(' ')
		left = line[0]
		right = line[2]

		try:
			print dbpedia_instances[left], dbpedia_instances[right]
			dbpedia_graph.write(line)
			dbpedia_graph.write('\n')

		except KeyError: #if one of the two entities is not a dbpedia instances, the edge is removed
			continue


dbpedia_graph.close()


