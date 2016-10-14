import optparse


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

with open('datasets/page_ids_en.ttl','r') as f:

    for line in f:

        line = line.split(' ')

        if line[0] == '#':
            continue

        url = line[0] 

        wiki_id_list = line[2].split('\"')

        print wiki_id_list

        wiki_id = wiki_id_list[1]

        wiki_from_url_dict[url] = int(wiki_id)

output_file_write = open(output_file,'w')

#iterate through the page links and turn urls into wiki_ids

with open(input_file) as page_links:

    for line in page_links:

        line = line.split(' ')

        if line[0] == '#':
            continue

        url_1 = line[0]
        url_2 = line[2]

        try:

        	wiki_id1 = wiki_from_url_dict[url_1]

        	wiki_id2 = wiki_from_url_dict[url_2]

        except (KeyError, IndexError):
        	continue

        output_file_write.write('%d %d' %(wiki_id1,wiki_id2))


output_file_write.close()
