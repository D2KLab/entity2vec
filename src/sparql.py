from __future__ import print_function
from SPARQLWrapper import SPARQLWrapper, JSON
import optparse
import codecs

class sparql(object):

	def __init__ (self, entities, properties, folder, output_folder, endpoint):

		self.entities = entities

		self.folder = folder

		self.output_folder = output_folder

		self.wrapper = SPARQLWrapper(endpoint)

		if properties == "all":

			self._get_all_properties()

		else:
			self.properties = []

			for p in codecs.open('%s/%s'%(folder,properties),'r', encoding='utf-8'):

				self.properties.append(p.strip('\n'))


	def _get_all_properties(self): #get all the properties if a list is not provided

		wrapper = self.wrapper

		self.properties = []

		wrapper.setQuery("""
				     SELECT ?p WHERE {
				     ?s ?p ?o.
				     }""")

		wrapper.setReturnFormat(JSON)

		for result in wrapper.query().convert()['results']['bindings']:

			self.properties.append(results['p']['value'])


	def get_property_graphs(self):

		wrapper = self.wrapper

		if self.entities == "all":

			for prop in self.properties: #iterate on the properties

				print(prop)

				with codecs.open('%s/%s/%s' %(folder, output_folder, prop),'w', encoding='utf-8') as prop_graph: #open a property file graph

					wrapper.setQuery("""
				     SELECT ?s ?o  WHERE {
				     ?s %s ?o.
				     }""" %(prop,uri))

					wrapper.setReturnFormat(JSON)

					for result in wrapper.query().convert()['results']['bindings']:

						subj = result['s']['value']

						obj = result['o']['value']

						print(subj, obj)

						prop_graph.write('%s %s\n' %(subj, obj)) 

		else:

			with codecs.open('%s/%s'%(self.folder,self.entities),'r', encoding='utf-8') as f: #open entity file, select only those entities

					for prop in self.properties: #iterate on the properties

						print(prop)

						with codecs.open('%s/%s/%s' %(self.folder, self.output_folder, prop),'w', encoding='utf-8') as prop_graph: #open a property file graph

							for uri in f: #for each entity

								print(uri)

								uri = uri.strip('\n')

								uri = '<'+uri+'>'

								wrapper.setQuery("""
							     SELECT ?s ?o  WHERE {
							     ?s %s ?o.
							     FILTER (?s = %s) }""" %(prop,uri))

								wrapper.setReturnFormat(JSON)

								for result in wrapper.query().convert()['results']['bindings']:

									subj = result['s']['value']

									obj = result['o']['value']

									print(subj, obj)

									prop_graph.write('%s %s\n' %(subj, obj)) 

							f.seek(0) #reinitialize iterator

		return 


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-e','--entities', dest = 'entity_file', help = 'entity file name', default = 'all')
    parser.add_option('-p','--properties', dest = 'property_file', help = 'property file name', default = 'all')
    parser.add_option('-f','--folder', dest = 'folder', help = 'folder')
    parser.add_option('-o','--output', dest = 'output_folder', help = 'output folder')
    parser.add_option('-e','--endpoint', dest = 'endpoint', help = 'sparql endpoint')


    (options, args) = parser.parse_args()

    get_property_graphs(options.entity_file, options.property_file, options.folder, options.output_folder, options.endpoint)