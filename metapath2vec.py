# creating 
import argparse
import random, csv

import networkx as nx
import multiprocessing as mp

max_walk_len = None
gtype = 'aca'

mapping_dict = {}
S = set()
G = nx.Graph()

def choose_neighbor(G,node):
	neighbors = list(G.neighbors(node))
	return random.choice(neighbors)	


def random_walk(G,v):
	path, walk_length,curr_node = [v], 0, v
	while walk_length != max_walk_len:
		# Choose a neighbour of current node
		neighbor = choose_neighbor(G,curr_node)
		path.append(neighbor)
		curr_node = neighbor
		walk_length += 1
	return [str(n) for n in path]		


def run_surfer(i):
	metapaths = []

	for v in S:
		metapath = random_walk(G,v)
		metapaths.append(' '.join(metapath) + '\n')
	return ''.join(metapaths)


def generate_metapaths(dataset, max_walk_length, graphtype, num_threads):
	global max_walk_len
	max_walk_len = max_walk_length
	
	# graphs.main(dataset)
	
	num_walks = 1000
	metapath_datafile = 'metapath2vec/m2v_data/' + dataset + '/' + gtype + '_' + graphtype + '.txt'			

	print('Writing metapaths to ' + metapath_datafile)	
	metapath_file = open(metapath_datafile, 'w')
	print('Generating metapaths for ' + dataset)
	# Run random surfers
	pool = mp.Pool(num_threads)
	for metapaths in pool.imap(run_surfer, [i for i in range(num_walks)]):
		metapath_file.write(metapaths)

	print('\nFinished generating metapaths!')
	metapath_file.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate metapaths for given author-venue edge list')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \naminer \ndbis')
	parser.add_argument('-l','--len', dest='max_walk_length', default=100,
					help='maximum walk length of random walker(default: 100)')
	parser.add_argument('-n','--threads', dest='num_threads', default=30,
					help='number of threads (default: 30)')
	parser.add_argument('-g','--graphtype', dest='graphtype', default="clique",
			    help='Type of edgelist. Choose among following: \nclique \nstar')

	args = parser.parse_args()
	dataset = args.dataset
	graphtype = args.graphtype
	# reading the mapping file
	mapping_reader = csv.reader(open(dataset+'/'+dataset+'_mapping_'+graphtype+'.csv'), delimiter='\t')

	for line in mapping_reader:
		mapping_dict[line[0]] = line[1]

	reader = csv.reader(open(dataset+'/'+dataset+'_train_'+ graphtype +'.csv'), delimiter='\t')
	for row in reader:
		[n1, n2] = [row[0], row[1]]
		if n1.startswith('v_'):
			S.add(mapping_dict[n1])
		if n2.startswith('v_'):
			S.add(mapping_dict[n2])

	reader = csv.reader(open(dataset+'/'+dataset+'_train_'+ graphtype +'.csv'), delimiter='\t')
	for row in reader:
		[n1, n2] = [row[0], row[1]]
		if n1.startswith('t_') or n2.startswith('t_'):
			continue
		else:
			G.add_edge(mapping_dict[n1], mapping_dict[n2])		
	
	print(nx.info(G))

	generate_metapaths(dataset=args.dataset, max_walk_length=int(args.max_walk_length), graphtype=args.graphtype, num_threads=int(args.num_threads))	
	
