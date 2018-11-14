'''
Creates random data.
Steps:
1. Create individual Author-Author graphs for train and test by reading their A-A edgelist files.
2. Get number of edges in positive (test file).
3. Find two random nodes from the above test graph, check if test and train files don't have that edgelist (i.e. negative edge)

Command: python create_random.py -d <dataset>
'''

import networkx as nx
from random import choice
import csv
import argparse
import os


# create random dataset for test (non-existing test edges)
def create_random(dataset):

	# create individual Author-Author graphs for train and test
	print("Creating individual Author-Author graphs for train and test")
	G_test = nx.Graph()
	G_train = nx.Graph()
	reader = csv.reader(open(dataset+'/'+dataset+'_test.csv'), delimiter='\t')
	for row in reader:
		[author1, author2] = [row[0], row[1]]
		G_test.add_edge(author1, author2)
	reader = csv.reader(open('all_edges_APA/' + dataset+'_train_raw.csv'), delimiter='\t')
	for row in reader:
		[author1, author2] = [row[0], row[1]]
		G_train.add_edge(author1, author2)
	print("Graphs created")

	out_file = dataset+'/'+dataset+'_random.csv'
	f = open(out_file, 'w')

	# get number of edges in positive (test file)
	g = open(dataset+'/'+dataset+'_test.csv', 'r')
	total = len(g.readlines())
	count = 0
	# find two random nodes from the above test graph, check if test and train files don't have that edgelist (i.e. negative edge)
	test_nodes = list(G_test.nodes())
	while(count < total):
		n1 = choice(G_test.nodes())
		n2 = choice(G_test.nodes())
		edges = dict()
		if not G_test.has_edge(n1, n2) and not G_train.has_edge(n1,n2) and not (n1,n2) in edges and n1<n2:
			edges[(n1,n2)]={}
			f.write(n1 + "\t" + n2 + "\n")
			count += 1

	f.close()

	print("Created test random data for " + dataset + " dataset: " + out_file)
	print('Number of edges: ')
	os.system('wc -l ' + out_file)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Create test data')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')

	args = parser.parse_args()

	dataset = args.dataset
	print("Creating test random data for " + dataset + " dataset")

	create_random(dataset)
	
