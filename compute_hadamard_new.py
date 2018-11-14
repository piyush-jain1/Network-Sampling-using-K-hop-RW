'''
Compute hadamard product for all the author pair in test and random file
Note that the test and random file has author like a_123
Thus we pick the mapping file for corresponding dataset and pick mapping from there

python compute_hadamard_new.py -d dblp -m khop -k 1 -g clique
'''
import os, csv
import shutil
import argparse
import multiprocessing as mp

from gensim.models import KeyedVectors

model = None


def compute_hadamard(authors):
	'''
	Given a author pair, compute hadamard 
	'''
	hadamard = model.wv[authors[0]] *  model.wv[authors[1]]
	return (authors[0], authors[1], hadamard)


def compute_similarities(dataset, method, khop, num_threads, graphtype):
	'''
	Read the embedding files from the embedding folder for given dataset and graphtype
	'''
	global model
	if method == "metapath2vec":
		model_file = dataset + '/embeddings/' + dataset + '_metapath2vec_embedding_aca_'+ graphtype +'.txt'
	elif method == "node2vec":
		model_file = dataset + '/embeddings/' + dataset + '_node2vec_'+ graphtype +'.txt'
	elif method == "verse":
		model_file = dataset + '/embeddings/' + dataset + '_verse_'+ graphtype +'.txt'
	elif method == "concat":
		model_file = dataset + '/embeddings/' + dataset + '_word2vec_concat_'+ graphtype +'.txt'
	elif method == "khop":
		model_file = dataset + '/embeddings/' + dataset + '_word2vec_' + khop + '_'+ graphtype +'.txt'
	print("Reading the embedding file", model_file)
	model = KeyedVectors.load_word2vec_format(model_file)
	
	authors_test = set()
	pool = mp.Pool(num_threads)

	test_files = [dataset + '_test', dataset + '_random']

	mapping_filename = dataset+'/'+dataset+'_mapping_'+ graphtype +'.csv'
	print("reading the mapping file", mapping_filename)
	mapping_reader = csv.reader(open(mapping_filename), delimiter='\t')
	mapping_dict = {}

	for line in mapping_reader:
		mapping_dict[line[0]] = line[1]

	for test_file in test_files:
		author_edges = []
		# lines = open('test_clique/' + dataset + '/' + test_file)
		reader = csv.reader(open(dataset+'/'+test_file+'.csv'), delimiter='\t')
		for line in reader:
			author1 = mapping_dict[line[0]]
			author2 = mapping_dict[line[1]]
			authors_test.add(author1)
			authors_test.add(author2)
			
			if author1 not in model.wv.vocab:
				continue
			if author2 not in model.wv.vocab:
				continue
			
			author_edges.append((author1, author2))
		scores = ''
		author_edges_scores = pool.map(compute_hadamard, author_edges)
		if method == "metapath2vec":
			filename = dataset + '/hm_scores/' + test_file + '_metapath2vec' + '_'+ graphtype +'.txt'
		elif method == "node2vec":
			filename = dataset + '/hm_scores/' + test_file + '_node2vec' + '_'+ graphtype +'.txt'
		elif method == "verse":
			filename = dataset + '/hm_scores/' + test_file + '_verse' + '_'+ graphtype +'.txt'
		elif method == "concat":
			filename = dataset + '/hm_scores/' + test_file + '_concat' + '_'+ graphtype +'.txt'
		elif method == "khop":
			filename = dataset + '/hm_scores/' + test_file + '_khop_'+ khop + '_'+ graphtype +'.txt'
		print("writing the scores file", filename)
		f = open(filename, 'w')
		for z in author_edges_scores:
			scores = z[0] + ' ' + z[1] 
			for item in z[2]:
				scores = scores + ' ' + str(item)
			f.write(scores)
			f.write('\n')
		f.close()
	   

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Compute hadamard operation on nodes participating to form an edge in test data.')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-m','--method', dest='method', required=True,
			    help='The method used for generating embeddings. Choose among following: \nnode2vec \nmetapath2vec \nverse \nconcat\n khop')
	parser.add_argument('-t','--num_threads', dest='num_threads', default=30,
			    help='Number of threads used for parallelization(default: 30)')
	parser.add_argument('-k','--khop', dest='khop', default=1,
			    help='Number of hop')
	parser.add_argument('-g','--graphtype', dest='graphtype', default="clique",
			    help='Choose graphtype: \nclique \nstar')

	args = parser.parse_args()
	compute_similarities(args.dataset, args.method, args.khop, int(args.num_threads), args.graphtype)
