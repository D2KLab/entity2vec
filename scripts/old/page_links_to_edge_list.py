import optparse
import os
import json

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'input_file', help = 'input_file')
parser.add_option('-o','--output', dest = 'output_file', help = 'output_file')
parser.add_option('-n','--name', dest = 'name', help = 'name of the dataset')

(options, args) = parser.parse_args()

if options.input_file is None:
   options.input_file = raw_input('Enter input file:')

if options.output_file is None:
    options.output_file = raw_input('Enter output file:')

if options.name is None:
    options.name = raw_input('Enter name of the dataset')

input_file = options.input_file

name = options.name

read_input_file = open(input_file,'rU')

output_file = options.output_file

write_output_file = open(output_file, 'w')

dictionary = {}

#create a dictionary that assigns to each id a unique integer
index = 0

for line in read_input_file: 


    line = line.split(' ')
    if line[0] == '#':
        continue

    id1 = line[0]
    id2 = line[2]

    try:
    #id1 has already an index

        print dictionary[id1]

        try:
        #id2 has already an index, thus index is free
            print dictionary[id2]

        #id2 does not have an index, so index is assigned and then incremented      
        except KeyError:
            dictionary[id2] = index
            index += 1

    except KeyError:
    #id1 does not have an index yet

        dictionary[id1] = index
        index += 1

        #id2 has an index
        try:
            print dictionary[id2]

        #id2 does not have an index, so index+1 is assigned and then incremented
        except KeyError:
            dictionary[id2] = index
            index += 1

    write_output_file.write('%d %d\n'%(dictionary[id1], dictionary[id2]))

read_input_file.close()
write_output_file.close()

print dictionary


with open('dictionaries/dictionary_%s.json'%name,'w') as f:
    json.dump(dictionary,f)

f.close()
