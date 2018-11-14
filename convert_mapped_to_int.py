'''
Create train files with integer index
Read the mapping file and the train_clique/train_star file.
Write the mapped results in train_ini_clique/train_ini_star


'''
import csv, sys, argparse


def func(dataset, graphtype):
	mapping_reader = csv.reader(open(dataset+'/'+dataset+'_mapping_'+ graphtype +'.csv'), delimiter='\t')
	mapping_dict = {}

	for line in mapping_reader:
		mapping_dict[line[0]] = line[1]

	file_reader = csv.reader(open(dataset+'/'+dataset+'_train_' + graphtype +'.csv'), delimiter='\t')
	file_reader_int = open(dataset+'/'+dataset+'_train_int_'+ graphtype +'.txt', 'w')
	
	print("creating clique with int index", dataset+'/'+dataset+'_train_int_'+ graphtype +'.txt')

	for line in file_reader:
		file_reader_int.write(mapping_dict[line[0]]+" "+mapping_dict[line[1]]+"\n")

	file_reader_int.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Concatenate samplings.')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-g','--graphtype', dest='graphtype', required=True,
			    help='graphtype. Choose among following: \nclique \nstar')
	args = parser.parse_args()
	func(args.dataset, args.graphtype)
