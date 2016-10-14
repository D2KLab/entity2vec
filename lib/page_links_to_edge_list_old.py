import optparse
import os
import csv

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

lines = read_input_file.readlines()

dictionary = {}

ids = []

#create a dictionary that assigns to each id a unique integer

for index in range(1,len(lines) - 1): #first and last line are headings
    line = lines[index]
    line = line.split(' ')
    id1 = line[0]
    id2 = line[2]
    ids.append(id1)
    ids.append(id2)

print ids   

for index in range(len(ids)):
    ID = ids[index]
    try:
        print dictionary[ID] 

    except KeyError:
        dictionary[ID] = index


output_file = options.output_file

write_output_file = open(output_file, 'w')

for line in lines[1:-1]:
    line = line.split(' ')
    id1 = line[0]
    id2 = line[2]
    write_output_file.write('%d %d\n'%(dictionary[id1], dictionary[id2]))


with open('dictionaries/dictionary_%s.csv'%name,'wb') as f:
    w = csv.writer(f)
    w.writerows(dictionary.items())

read_input_file.close()
write_output_file.close()
