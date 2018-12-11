'''
Creates test data.
Steps:
1. Read the list of selected conferences for a given dataset type.
2. Find the id mappings of those conferences from the mapping file cerated earlier.
3. Read the given mapped file row wise and based on the threshold decide if it is part of test (year > threshold_year).
4. Create A-A edgelists for train and test (raw files) : Read the mapped file and write all co-occuring author-author pairs 
	(having A-P-A links) in raw files, both for train and test data 
5. Remove edges from test_raw which are in train_raw
6. Create set of nodes present in train, store as embedded_author
7. Write edges to test where both nodes are in embedded_author

Command: python create_test.py -d <dataset>
'''

import csv 
import argparse
import os


# threshold year to divide the dataset into train and test
acm_threshold_year = 2014
dblp_threshold_year = 2016


# List of conferences selected and get their id mappings
def pre(dataset):

	# to store the id mapping of the venues
	global venue_mapped
	venue_mapped = []

	# read list of conferences for each dataset
	conf_list = ''
	if dataset == 'dblp':
		conf_list = 'dblp_all_conf.txt'
	elif dataset == 'acm':
		conf_list = 'acm_all_conf.txt'
	f = open(conf_list,'r')
	temp = f.readlines()
	conf_list = [ _.rstrip() for _ in temp ]
	f.close()

	# find id mapping of the venues in conf_list
	reader = csv.reader(open(dataset+"/mappings/"+dataset+'_venue_mapping.txt'), delimiter='\t')
	for row in reader:
		venue = row[1]
		venue_cleaned = venue.lower()
		venue_cleaned = "".join(venue_cleaned.split(' '))
		if venue_cleaned in conf_list:
			venue_mapped.append(row[0])


# create A-A edgelists for train and test
def create_raw(dataset):

	f = open('all_edges_APA/' + dataset + '_train_raw.csv', 'w')
	g = open('all_edges_APA/' + dataset + '_test_raw.csv', 'w')
	
	# threshold year
	if dataset == 'dblp':
		threshold_year = dblp_threshold_year
	elif dataset == 'acm':
		threshold_year = acm_threshold_year

	# read the mapped file and write all co-occuring author-author pairs (having A-P-A links) in raw files
	# both for train and test data 
	reader = csv.reader(open(dataset+'/'+dataset + '_mapped.csv'), delimiter='\t')
	for row in reader:
		[title, venue, year, authors] = [row[0], row[1], int(row[2]), eval(row[3])]
		if venue in venue_mapped:
			for author1 in authors:
				for author2 in authors:
					if author1<author2:
						if year <= threshold_year:
							f.write(author1 + "\t" + author2 + "\n")
						else:
							g.write(author1 + "\t" + author2 + "\n")
	f.close()
	g.close()


# create test dataset
def create_test(dataset):

	# remove edges from test_raw which are in train_raw
	command = 'sort ' + 'all_edges_APA/' + dataset + '_test_raw.csv ' + 'all_edges_APA/' + dataset + '_train_raw.csv ' + 'all_edges_APA/' + dataset + '_train_raw.csv | uniq -u > ' + dataset+'/'+dataset+'_diff.csv'
	os.system(command)

	# threshold year
	if dataset == 'dblp':
		threshold_year = dblp_threshold_year
	elif dataset == 'acm':
		threshold_year = acm_threshold_year

	# create set of nodes present in train, store as embedded_author
	embedded_author = set()
	reader = csv.reader(open(dataset+'/'+dataset+'_mapped.csv'), delimiter='\t')
	for row in reader:
		[title, venue, year, authors] = [row[0], row[1], int(row[2]), eval(row[3])]
		if venue in venue_mapped:
			if year <= threshold_year:
				for author in authors:
					embedded_author.add(author)
			
	# write edges to test where both nodes are in embedded_author
	out_file = dataset+'/'+dataset+'_test.csv'
	f = open(dataset+'/'+dataset+'_diff.csv', 'r')
	g = open(out_file, 'w')

	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		[author1, author2] = [row[0], row[1]]
		if author1 in embedded_author and author2 in embedded_author:
			g.write(author1 + "\t" + author2 + "\n")
	f.close()
	g.close()

	# delete the diff files
	command = 'rm ' + dataset+'/'+dataset+'_diff.csv'
	os.system(command)

	print("Created test data for " + dataset + " dataset: " + out_file)
	print('Number of edges: ')
	os.system('wc -l ' + out_file)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Create test data')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')

	args = parser.parse_args()

	dataset = args.dataset

	print("Creating test data for " + dataset + " dataset")

	# create test data
	pre(dataset)
	create_raw(dataset)
	create_test(dataset)
