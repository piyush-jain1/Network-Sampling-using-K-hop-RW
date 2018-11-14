import csv
import math
import time
import random
import numpy as np
import networkx as nx
import multiprocessing as mp
import sys

def	create_venue_mapping(dataset):
	venue_mapping = {}
	cur_index = 0

	reader = csv.reader(open(dataset+'/'+dataset+'_unmapped.csv'), delimiter='\t')

	for row in reader:
		venue = row[2]
		venue_cleaned = venue.lower()
		venue_cleaned = "".join(venue_cleaned.split(' '))
		if venue_cleaned in venue_mapping:
			venue_mapping[venue_cleaned] = venue_mapping[venue_cleaned] + 1
		else:
			venue_mapping[venue_cleaned] = 1

	f = open((dataset+'/'+dataset+'_venue_count.csv'), "w")
	venue_sorted_mapping = sorted(venue_mapping, key=venue_mapping.get, reverse=True)
	for key in venue_sorted_mapping:
		f.write("{0}\t{1}\n".format(key,venue_mapping[key]))
	f.close()

if __name__ == "__main__":
	create_venue_mapping("acm")