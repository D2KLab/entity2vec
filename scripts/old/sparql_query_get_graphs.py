from __future__ import print_function
from SPARQLWrapper import SPARQLWrapper, JSON
import optparse
import codecs


def get_property_graphs(entities, properties, folder, output_folder):

	sparql = SPARQLWrapper("http://dbpedia.org/sparql")

	if entities == "all":

		with codecs.open('%s/%s'%(folder,properties),'r', encoding='utf-8') as p: #open property file, select only those properties

			for prop in p: #iterate on the properties

				prop = prop.strip('\n')

				print(prop)

				with codecs.open('%s/%s/%s' %(folder, output_folder, prop),'w', encoding='utf-8') as prop_graph: #open a property file graph

					sparql.setQuery("""
				     SELECT ?s ?o  WHERE {
				     ?s %s ?o.
				     FILTER (?s = %s)}""" %(prop,uri))

					sparql.setReturnFormat(JSON)

					for result in sparql.query().convert()['results']['bindings']:

						subj = result['s']['value']

						obj = result['o']['value']

						print(subj, obj)

						prop_graph.write('%s %s\n' %(subj, obj)) 

	else:

		with codecs.open('%s/%s'%(folder,entities),'r', encoding='utf-8') as f: #open entity file, select only those entities

			with codecs.open('%s/%s'%(folder,properties),'r', encoding='utf-8') as p: #open property file, select only those properties

				for prop in p: #iterate on the properties

					prop = prop.strip('\n')

					print(prop)

					with codecs.open('%s/%s/%s' %(folder, output_folder, prop),'w', encoding='utf-8') as prop_graph: #open a property file graph

						for uri in f: #for each entity

							print(uri)

							sparql = SPARQLWrapper("http://dbpedia.org/sparql")

							uri = uri.strip('\n')

							uri = '<'+uri+'>'

							sparql.setQuery("""
						     SELECT ?s ?o  WHERE {
						     ?s %s ?o.
						     FILTER (?s = %s) }""" %(prop,uri))

							sparql.setReturnFormat(JSON)

							for result in sparql.query().convert()['results']['bindings']:

								subj = result['s']['value']

								obj = result['o']['value']

								print(subj, obj)

								prop_graph.write('%s %s\n' %(subj, obj)) 

						f.seek(0) #reinitialize iterator

	return 



if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-e','--entities', dest = 'entity_file', help = 'entity file name', default = 'all')
    parser.add_option('-p','--properties', dest = 'property_file', help = 'property file name')
    parser.add_option('-f','--folder', dest = 'folder', help = 'property file name')
    parser.add_option('-o','--output', dest = 'output_folder', help = 'property file name')


    (options, args) = parser.parse_args()

    get_property_graphs(options.entity_file, options.property_file, options.folder, options.output_folder)