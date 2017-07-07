from __future__ import print_function
from SPARQLWrapper import SPARQLWrapper, JSON
import optparse
import codecs
from os import mkdir
import json

################################################################
## contains SPARQL queries to get property-specific subgraphs ##
################################################################

class sparql(object):

	def __init__ (self, entities, config_file, dataset, endpoint, default_graph, entity_class):

		self.entities = entities #file containing a list of entities

		self.dataset = dataset

		self.wrapper = SPARQLWrapper(endpoint)

		self.wrapper.setReturnFormat(JSON)

		if default_graph:

			self.default_graph = default_graph

			self.wrapper.addDefaultGraph(self.default_graph)

		self.entity_class = entity_class

		self.query_prop = "SELECT ?s ?o  WHERE {?s %s ?o. }"

		self.query_prop_uri = "SELECT ?s ?o  WHERE {?s %s ?o. FILTER (?s = %s)}"

		self._define_properties(config_file)


	def _define_properties(self, config_file):

		with codecs.open(config_file, 'r', encoding = 'utf-8') as config_read:

			property_file = json.loads(config_read.read())

		try:

			self.properties = [i for i in property_file[self.dataset]]
			print(self.properties)

		except KeyError:

			print("No set of properties provided in the dataset")

			if self.entity_class == False:

				query_all_prop = "SELECT distinct ?p WHERE {?s ?p ?o. FILTER(!isLiteral(?o) && regex(STR(?p),\"dbpedia.org/ontology\"))}"

				self._get_properties(query_all_prop)

			else:

				query_category_prop = "select distinct ?p where { ?s a dbo:Band. ?s ?p ?o. FILTER(!isLiteral(?o) && regex(STR(?p),\"dbpedia.org/ontology\"))}"

				self._get_properties(query_category_prop)


	def _get_properties(self, query): #get all the properties from sparql endpoint if a list is not provided in config file

		self.properties = []

		self.wrapper.setQuery(query)

		self.wrapper.setReturnFormat(JSON)

		for results in self.wrapper.query().convert()['results']['bindings']:

			self.properties.append(results['p']['value'])

		self.properties.append("dct:subject")

		self.properties.append("rdf:type")


	def get_property_graphs(self):

		properties = self.properties

		if 'feedback' in properties:
			properties.remove('feedback') #don't query for the feedback property


		for prop in properties: #iterate on the properties

			prop_short = prop

			prop_namespace = prop

			if '/' in prop:

				# avoid creating file with a '/' in the name
				prop_short = prop.split('/')[-1]

				# if it is actually a URI, surround by "<>"
				if prop.startswith("http"):
					prop_namespace = '<'+prop+'>'

			try:
				mkdir('datasets/%s/'%(self.dataset))
				mkdir('datasets/%s/graphs' %(self.dataset))

			except:
				pass


			with codecs.open('datasets/%s/graphs/%s.edgelist' %(self.dataset, prop_short),'w', encoding='utf-8') as prop_graph: #open a property file graph

				if self.entities == "all":

					self.wrapper.setQuery(self.query_prop%prop_namespace)


					for result in self.wrapper.query().convert()['results']['bindings']:

						subj = result['s']['value']

						obj = result['o']['value']

						print((subj, obj))

						prop_graph.write('%s %s\n' %(subj, obj))


				else:

					with codecs.open('%s'%self.entities,'r', encoding='utf-8') as f: #open entity file, select only those entities

						for uri in f: #for each entity

							uri = uri.strip('\n')

							uri = '<'+uri+'>'

							self.wrapper.setQuery(self.query_prop_uri%(prop_namespace,uri))

							for result in self.wrapper.query().convert()['results']['bindings']:

								subj = result['s']['value']

								obj = result['o']['value']

								print((subj, obj))

								prop_graph.write('%s %s\n' %(subj, obj))

						f.seek(0) #reinitialize iterator


		return



	@staticmethod
	def get_uri_from_wiki_id(wiki_id):


		sparql = SPARQLWrapper("http://dbpedia.org/sparql")

		sparql.setQuery("""select ?s where {?s <http://dbpedia.org/ontology/wikiPageID> %d
		   }""" %int(wiki_id))

		sparql.setReturnFormat(JSON)

		try:
			uri = sparql.query().convert()['results']['bindings'][0]['s']['value']

		except:
			uri = None

		return uri


if __name__ == '__main__':

	parser = optparse.OptionParser()
	parser.add_option('-e','--entities', dest = 'entity_file', help = 'entity file name', default = 'all')
	parser.add_option('-c','--config_file', default='config/properties.json', help='Path to configuration file')
	parser.add_option('-k','--dataset', dest = 'dataset', help = 'dataset')
	parser.add_option('-m','--endpoint', dest = 'endpoint', help = 'sparql endpoint')
	parser.add_option('-d', '--default_graph', dest = 'default_graph', help = 'default graph', default = False)
	parser.add_option('--entity_class', dest = 'entity_class', help = 'entity class', default = False)

	(options, args) = parser.parse_args()

	sparql_query = sparql(options.entity_file, options.config_file, options.dataset, options.endpoint, options.default_graph, options.entity_class)

	sparql_query.get_property_graphs()
