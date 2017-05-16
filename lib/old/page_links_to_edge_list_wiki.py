import optparse
import pickle

#converts urls to wiki_id

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'input_file', help = 'input_file')
parser.add_option('-o','--output', dest = 'output_file', help = 'output_file')

(options, args) = parser.parse_args()

if options.input_file is None:
   options.input_file = raw_input('Enter input file:')

if options.output_file is None:
    options.output_file = raw_input('Enter output file:')


input_file = options.input_file

output_file = options.output_file

#define the dictionary url:wiki_id

wiki_from_url_dict = {}

with open('../../datasets/dbpedia/page_ids_en_2016.ttl','r') as f:

    for line in f:

        line = line.split(' ')

        if line[0] == '#':
            continue

        url = line[0] 

        wiki_id_list = line[2].split('\"')

        wiki_id = wiki_id_list[1]

        print(url, wiki_id)

        wiki_from_url_dict[url] = int(wiki_id)

output_file_write = open(output_file,'w')

#iterate through the page links and turn urls into wiki_ids

max_wiki_id = max(wiki_from_url_dict.values()) + 1

local_id = {}

count = 0

with open(input_file) as page_links:

    for line in page_links:

        line = line.split(' ')

        if line[0] == '#':
            continue

        url_1 = line[0]
        url_2 = line[2]

        #if wiki_id not found, assign an id = max_wiki_id and increment max_wiki_id

        try:

            wiki_id1 = wiki_from_url_dict[url_1] #first entity has wiki_id

            try:
                wiki_id2 = wiki_from_url_dict[url_2] #first and second entities have wiki_ids

            except (KeyError, IndexError): #first entity has wiki_id, second entity doesn't

                try: #check if a local id has already been assigned

                    wiki_id2 = local_id[url_2]

                except (KeyError, IndexError):

                    wiki_id2 = max_wiki_id

                    local_id[url_2] = wiki_id2

                    max_wiki_id +=1

        except (KeyError, IndexError): #first entity doesn't have wiki_id

            try:
                wiki_id1 = local_id[url_1]

            except (KeyError, IndexError):

                wiki_id1 = max_wiki_id

                local_id[url_1] = wiki_id1

                max_wiki_id += 1

            try: #first entity doesn't have wiki_id, second entity has it

                wiki_id2 = wiki_from_url_dict[url_2]

            except (KeyError, IndexError): #neither first nor second entity have wiki_ids


                try: #check if a local id has already been assigned

                    wiki_id2 = local_id[url_2]

                except (KeyError, IndexError):

                    wiki_id2 = max_wiki_id

                    local_id[url_2] = wiki_id2

                    max_wiki_id +=1


        output_file_write.write('%d %d\n' %(wiki_id1,wiki_id2))

        print count

        count += 1

output_file_write.close()


pickle.dump(local_id,open('../../datasets/dbpedia/local_id_to_url_full_mapping_based.p','wb'))
