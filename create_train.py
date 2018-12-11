'''
Creates train data in star and clique fashion : heterogeneous edgelist [Author, Paper, Conference]
Steps:
1. Read the list of selected conferences for a given dataset type.
2. Find the id mappings of those conferences from the mapping file cerated earlier.
3. Read the given mapped file row wise and based on the threshold decide if it is part of train (year <= threshold_year).
4. Star fashion:
	write all co-occuring title-author pairs
	write all co-occuring title-venue pairs 
   Clique fashion:
   	write all co-occuring title-author pairs
	write all co-occuring title-venue pairs
	write all co-occuring title-venue pairs

Command: python create_train.py -d <dataset> -g <graphtype>
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


# creating star-based train dataset
def create_train_star(dataset):

	print('Creating star-based train data for ' + dataset + ' dataset')

	# threshold year
	if dataset == 'dblp':
		threshold_year = dblp_threshold_year
	elif dataset == 'acm':
		threshold_year = acm_threshold_year

	out_file = dataset+'/'+dataset + '_train_star.csv'
	f = open(out_file, 'w')

	# write edges in star fashion
	reader = csv.reader(open(dataset+"/"+dataset + '_mapped.csv'), delimiter='\t')
	for row in reader:
		[title, venue, year, author] = [row[0], row[1], int(row[2]), eval(row[3])]
		if venue in venue_mapped:
			if year <= threshold_year:
				for a in author:
					f.write(title + "\t" + a + "\n")
				f.write(title + "\t" + venue + "\n")
	f.close()
	print('Created star-based train data for ' + dataset + ' dataset: ' + out_file)
	print('Number of edges: ')
	os.system('wc -l ' + out_file)


# creating clique-based train dataset
def create_train_clique(dataset):

	print('Creating clique-based train data for ' + dataset + ' dataset')

	a_dict = {}
	a_idx = 0 
	v_dict = {}
	v_idx = 0 	
	c_dict = {}
	c_idx = 0 

	# threshold year
	if dataset == 'dblp':
		threshold_year = dblp_threshold_year
	elif dataset == 'acm':
		threshold_year = acm_threshold_year

	out_file = dataset+'/'+dataset + '_train_clique.csv'
	f = open(out_file, 'w')

	# write edges in clique fashion
	reader = csv.reader(open(dataset+"/"+dataset + '_mapped.csv'), delimiter='\t')
	for row in reader:
		[title, venue, year, author] = [row[0], row[1], int(row[2]),  eval(row[3])]
		if venue in venue_mapped:
			if year <= threshold_year:
				for a in author:
					f.write(title + "\t" + a + "\n")
					f.write(a + "\t" + venue + "\n")
				f.write(title + "\t" + venue + "\n")
	f.close()
	print('Created clique-based train data for ' + dataset + ' dataset: ' + out_file)
	print('Number of edges: ')
	os.system('wc -l ' + out_file)
	


def create_train(dataset, graphtype):

	if graphtype == 'clique':
		create_train_clique(dataset)
	elif graphtype == 'star':
		create_train_star(dataset)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Create training data')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')
	parser.add_argument('-g','--graphtype', dest='graphtype', default="clique",
			    help='Type of edgelist. Choose among following: \nclique \nstar')

	args = parser.parse_args()

	# create train data
	pre(args.dataset)
	create_train(args.dataset, args.graphtype)
