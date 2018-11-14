'''
Concatenate the samplings for k hop random walk.
ex. python concatenate_k_hop_embedding.py -d acm -graphtype clique
'''
import csv,sys,argparse
dataset = sys.argv[1]
def func(dataset, graphtype):
	print ("Reading", dataset+'/embeddings/'+dataset+'_word2vec_1_'+ graphtype +'.txt')
	print ("Reading", dataset+'/embeddings/'+dataset+'_word2vec_2_'+ graphtype +'.txt')
	print ("Reading", dataset+'/embeddings/'+dataset+'_word2vec_3_'+ graphtype +'.txt')
	reader1 = open(dataset+'/embeddings/'+dataset+'_word2vec_1_'+ graphtype +'.txt','r')
	reader2 = open(dataset+'/embeddings/'+dataset+'_word2vec_2_'+ graphtype +'.txt','r')
	reader3 = open(dataset+'/embeddings/'+dataset+'_word2vec_3_'+ graphtype +'.txt','r')
	node_dict = {}

	next(reader1,None)
	next(reader2,None)
	next(reader3,None)

	for line in reader1:
		line = line.rstrip("\n\r")
		node = line.split(" ")[0]
		node_dict[node] = line.split(" ")[1:]

	for line in reader2:
		line = line.rstrip("\n\r")
		node = line.split(" ")[0]
		node_dict[node] = node_dict[node] + line.split(" ")[1:]

	for line in reader3:
		line = line.rstrip("\n\r")
		node = line.split(" ")[0]
		node_dict[node] = node_dict[node] + line.split(" ")[1:]

	concat_filename = dataset+'/embeddings/'+dataset+'_word2vec_concat_'+ graphtype +'.txt'
	print("writing concat file", concat_filename)
	f = open(concat_filename, 'w')
	f.write(str(len(node_dict.keys()))+" "+"300\n")
	for node, emb in node_dict.items():
		f.write(node + " " + " ".join(node_dict[node]) + "\n")
	f.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Concatenate samplings.')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-graphtype','--graphtype', dest='graphtype', required=True,
			    help='graphtype: \nclique \nstart')
	args = parser.parse_args()
	func(args.dataset, args.graphtype)
