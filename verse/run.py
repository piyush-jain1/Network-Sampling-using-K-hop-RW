import pickle
import argparse
import numpy as np

from argparse import RawTextHelpFormatter

def convert(dataset, dimensions, graphtype):
	W = np.fromfile('verse/data/' + dataset + '.bin', np.float32).reshape(-1, dimensions)
	f = open(dataset + '/' + 'embeddings/' +  dataset + '_verse_'+ graphtype +'.txt', 'w')
	f.write(str(len(W)) + ' ' + str(dimensions) + '\n')

	for w in range(len(W)):
		f.write(str(w) + ' ' + ' '.join([str(x) for x in W[w]]) + '\n')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate Embeddings for ACA, APA and APC graphs using verse.',
									 formatter_class=RawTextHelpFormatter)
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-dim','--dimensions', dest='dimensions', required=True,
			    help='The number of dimensions of each embedding.')
	parser.add_argument('-g','--graphtype', dest='graphtype', required=True,
			    help='g clique/star')

	args = parser.parse_args()
	convert(args.dataset, int(args.dimensions), args.graphtype)