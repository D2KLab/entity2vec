from __future__ import print_function
from SPARQLWrapper import SPARQLWrapper, JSON
import optparse
import codecs
from os import mkdir


class sparql(object):

	def __init__ (self, entities, properties, dataset, endpoint, default_graph):

		self.entities = entities #file containing a list of entities

		self.dataset = dataset

		self.wrapper = SPARQLWrapper(endpoint)

		if default_graph:

			self.default_graph = default_graph

			self.wrapper.addDefaultGraph(self.default_graph)

		if properties == "all":

			self.get_all_properties()

		else:

			self.properties = properties

		self.query_all_prop = "SELECT ?p WHERE {?s ?p ?o.}"

		self.query_prop = "SELECT ?s ?o  WHERE {?s %s ?o. }"

		self.query_prop_uri = "SELECT ?s ?o  WHERE {?s %s ?o. FILTER (?s = %s)}"



	def get_all_properties(self): #get all the properties from sparql endpoint if a list is not provided in config file

		self.properties = []

		self.wrapper.setQuery(self.query_all_prop)

		self.wrapper.setReturnFormat(JSON)

		for result in self.wrapper.query().convert()['results']['bindings']:

			self.properties.append(results['p']['value'])

		return self.properties



	def get_property_graphs(self):

		properties = self.properties

		if 'feedback' in properties:
			properties.remove('feedback') #don't query for the feedback property

		if self.entities == "all": #select all the entities

			for prop in properties: #iterate on the properties

				prop_short = prop

				if '/' in prop:
					prop_short = prop.split('/')[-1]

					prop_short = prop_short[0:-1]

				print(prop)

				try:
					mkdir('datasets/%s/'%(self.dataset))
					mkdir('datasets/%s/graphs' %(self.dataset))

				except:
					pass

				with codecs.open('datasets/%s/graphs/%s.edgelist' %(self.dataset, prop_short),'w', encoding='utf-8') as prop_graph: #open a property file graph

					self.wrapper.setQuery(self.query_prop%prop)

					self.wrapper.setReturnFormat(JSON)

					for result in self.wrapper.query().convert()['results']['bindings']:

						subj = result['s']['value']

						obj = result['o']['value']

						print(subj, obj)

						prop_graph.write('%s %s\n' %(subj, obj)) 

		else: # a file is provided

			with codecs.open('%s'%self.entities,'r', encoding='utf-8') as f: #open entity file, select only those entities

					for prop in properties: #iterate on the properties

						prop_short = prop

						if '/' in prop:

							prop_short = prop.split('/')[-1]

							prop_short = prop_short[0:-1]


						print(prop)

						try:
							mkdir('datasets/%s/'%(self.dataset))
							mkdir('datasets/%s/graphs' %(self.dataset))

						except:
							pass					

						with codecs.open('datasets/%s/graphs/%s.edgelist' %(self.dataset, prop_short),'w', encoding='utf-8') as prop_graph: #open a property file graph

							for uri in f: #for each entity

								uri = uri.strip('\n')

								uri = '<'+uri+'>'

								self.wrapper.setQuery(self.query_prop_uri%(prop,uri))

								self.wrapper.setReturnFormat(JSON)

								for result in self.wrapper.query().convert()['results']['bindings']:

									subj = result['s']['value']

									obj = result['o']['value']

									print(subj, obj)

									prop_graph.write('%s %s\n' %(subj, obj)) 

							f.seek(0) #reinitialize iterator

		return 



	@staticmethod
	def get_uri_from_wiki_id(wiki_id):


		sparql = SPARQLWrapper("http://dbpedia.org/sparql")

		sparql.setQuery("""select ?s where {?s <http://dbpedia.org/ontology/wikiPageID> ?%d 
		   }""" %wiki_id)

		sparql.setReturnFormat(JSON)

		return sparql.query().convert()['results']['bindings'][0]['s']['value']


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-e','--entities', dest = 'entity_file', help = 'entity file name', default = 'all')
    parser.add_option('-p','--properties', dest = 'properties', help = 'property_file', default = 'all')
    parser.add_option('-k','--dataset', dest = 'dataset', help = 'dataset')
    parser.add_option('-e','--endpoint', dest = 'endpoint', help = 'sparql endpoint')
    parser.add_option('-d', '--default_graph', dest = 'default_graph', help = 'default graph', default = False)


    (options, args) = parser.parse_args()

    sparql_query = sparql(options.entity_file, options.properties, options.dataset, options.endpoint, options.default_graph)

    sparql_query.get_property_graphs()