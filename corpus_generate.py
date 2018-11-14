'''
Generate corpus (create samples of the graph using k hop random graph)
khop: khop random walk
num_samples: samples for each node
samples_length: length of each sample

example: python corpus_generate.py -d acm -samples_length 100 -num_samples 30 -graphtype clique -k 3
'''
import csv
import math
import time
import random
import numpy as np
import networkx as nx
import multiprocessing as mp
import sys
import argparse

def display_time_taken(time_taken):
	'''
	time_taken: parameter to store the time taken
	the function for computing time taken
	'''
	time_str = ''
	if time_taken > 3600:
		hr = time_taken/3600
		time_taken = time_taken%3600
		time_str += str(int(hr)) + 'h '
	if time_taken > 60:
		mi = time_taken/60
		time_taken = time_taken%60
		time_str += str(int(mi)) + 'm '
	time_str += str(int(time_taken)) + 's'
	print('Time Taken: %s' % time_str)


def	create_graph(dataset, graphtype):
	'''
	Creates the newtworkx graph using the edgelist provided from train graph
	'''
	global G
	G = nx.Graph()

	mapping = {}
	cur_index = 0
	reader = csv.reader(open(dataset+'/'+dataset+'_train_'+ graphtype +'.csv'), delimiter='\t')
	for row in reader:
		[edge1, edge2] = [row[0], row[1]]
		edge1_idx = -1
		edge2_idx = -1

		if edge1 not in mapping:
			mapping[edge1] = cur_index
			edge1_idx = cur_index
			cur_index = cur_index + 1
		else:
			edge1_idx = mapping[edge1]

		if edge2 not in mapping:
			mapping[edge2] = cur_index
			edge2_idx = cur_index
			cur_index = cur_index + 1
		else:
			edge2_idx = mapping[edge2]
		
		G.add_edge(edge1_idx, edge2_idx)

	print(nx.info(G))

	mapping_filename = dataset+'/'+dataset+'_mapping_'+ graphtype +'.csv'
	print("mapping of node(a_) to integer index generated",mapping_filename)
	f = open(mapping_filename, "w")
	for key, value in mapping.iteritems():
		f.write("{0}\t{1}\n".format(key,value))
	f.close()


def func(node):
	'''
	Find num_samples for the given node using khop random walk
	'''
	writer = []
	for i in range(num_samples):
		source = node
		s = []
		s.append(source)
		r_neighbor = source
		for j in range(samples_length):
			i =0
			while(i<khop):
				r_neighbor = random.choice(list(G.neighbors(r_neighbor)))
				i = i+1
			s.append(r_neighbor)
		l = ' '.join(str(i) for i in s)
		writer.append(l)
	writ = '\n'.join(str(w) for w in writer )
	writ += "\n"
	return writ

		
def generate_corpus(dataset,workers, graphtype):
    
	print("Generating corpus!")
	
	node_list = list(G.nodes())
	
	pool = mp.Pool(workers)

	sampling_filename = dataset+'/'+dataset+'_sampling_' + str(khop) + '_'+ graphtype+'.csv'
	print("sampling file will be generated: ",sampling_filename)

	write_file = pool.map(func, node_list)

	f = open(sampling_filename,'w')
	
	for line in write_file:
		f.write(line)
	f.close()	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Corpus(samples) Generation using clique/star files')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-k','--khop', dest='khop', required=True,
			    help='Number of hop')
	parser.add_argument('-l','--samples_length', dest='samples_length', required=True,
			    help='length of samples')
	parser.add_argument('-n','--num_samples', dest='num_samples', required=True,
			    help='Number of samples')
	parser.add_argument('-g','--graphtype', dest='graphtype', default="clique",
			    help='Choose graphtype: \nclique \nstar')
	parser.add_argument('-workers','--workers', dest='workers', default=30,
			    help='number of cpu cores')
	args = parser.parse_args()

	global khop,samples_length,num_samples
	khop = int(args.khop)
	samples_length = int(args.samples_length)
	num_samples = int(args.num_samples)

	start = time.time()

	create_graph(args.dataset, args.graphtype)
	generate_corpus(args.dataset,args.workers,args.graphtype)

	finish = time.time()

	display_time_taken(finish - start)	
