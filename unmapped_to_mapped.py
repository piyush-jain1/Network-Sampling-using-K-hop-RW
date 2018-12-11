'''
Generates mapped data file from unmapped data file.
Steps:
1. Read the list of selected conferences for a given dataset type.
2. Find the id mappings of those conferences from the mapping file cerated earlier.
3. Read unmapped data and generate its mapped data
4. Write the generated mappings in the file

Note: acm contains venue in dirty manner. 
Same venue with year is appended in some and in some no. of that conf is appended.
Thus from the list of acm_conf_list, we have picked a conf if some conf in acm_conf_list is subset of conference present in file

Command: python unmapped_to_mapped.py -d <dataset>
'''


import sys, csv, argparse


# generate unmapped to mapped
def unmapped_to_mapped(dataset):

	venue_dict = {}
	venue_idx = 0
	author_dict = {}
	author_idx = 0
	title_dict = {}
	title_idx = 0

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


	print("Creating mappings for " + dataset)
	# read unmapped data and generate it as mapped data
	reader = csv.reader(open(dataset+"/"+dataset+'_unmapped.csv'), delimiter='\t')
	f = open(dataset+"/"+dataset+'_mapped.csv', 'w')
	next(reader,None)


	if dataset == 'acm':
		for row in reader:
			[title, venue, year, author] = [row[0], row[2], int(row[3]), row[5]]
			author = author.split(",")
			# acm conf cleaning
			venue_cleaned = venue.lower()
			venue_cleaned = "".join(venue_cleaned.split(' '))
			if venue_cleaned not in venue_dict:
				venue_dict[venue_cleaned] = "v_" + str(venue_idx)
				venue_idx = venue_idx + 1
			for a in author:
					if a not in author_dict:
						author_dict[a] = "a_" + str(author_idx)
						author_idx = author_idx + 1
			if title not in title_dict:
				title_dict[title] = "t_" + str(title_idx)
				title_idx = title_idx + 1
		
		reverse_map = {}
		# iteration over conf in conf list
		for conf in conf_list:
			reader = csv.reader(open(dataset+"/"+dataset+'_unmapped.csv'), delimiter='\t')
			next(reader,None)
			for row in reader:
				[title, venue, year, author] = [row[0], row[2], int(row[3]), row[5]]
				venue_cleaned = venue.lower()
				venue_cleaned = "".join(venue_cleaned.split(' '))
				# if the conf in list is substring of current venue
				if conf in venue_cleaned and (not conf==venue_cleaned):
					if conf in venue_dict:
						if venue_cleaned in venue_dict:
							reverse_map[venue_cleaned] = conf
							venue_dict.pop(venue_cleaned)
					else:
						venue_dict[conf] = "v_" + str(venue_idx)
						venue_idx = venue_idx+1
						reverse_map[venue_cleaned] = conf	
						venue_dict.pop(venue_cleaned)

		reader = csv.reader(open(dataset+"/"+dataset+'_unmapped.csv'), delimiter='\t')
		next(reader,None)
		for row in reader:
			[title, venue, year, author] = [row[0], row[2], int(row[3]), row[5]]	
			author = author.split(",")
			to_print = "[" + (",").join(["'" + author_dict[_] + "'" for _ in author]) +"]"
			venue_cleaned = venue.lower()
			venue_cleaned = "".join(venue_cleaned.split(' '))	
			if venue_cleaned in venue_dict:
				f.write(title_dict[title]+'\t'+venue_dict[venue_cleaned]+'\t'+str(year)+'\t'+to_print+'\n')
			else:
				f.write(title_dict[title]+'\t'+venue_dict[reverse_map[venue_cleaned]]+'\t'+str(year)+'\t'+to_print+'\n')


	if dataset == 'dblp':
		for row in reader:
			[title, venue, year, author] = [row[0], row[2], int(row[3]), eval(row[6])]
			if venue not in venue_dict:
				venue_dict[venue] = "v_" + str(venue_idx)
				venue_idx = venue_idx + 1
			for a in author:
				if a not in author_dict:
					author_dict[a] = "a_" + str(author_idx)
					author_idx = author_idx + 1
			if title not in title_dict:
				title_dict[title] = "t_" + str(title_idx)
				title_idx = title_idx + 1
			to_print = "[" + (",").join(["'"+author_dict[_]+"'" for _ in author]) +"]"
			f.write(title_dict[title]+'\t'+venue_dict[venue]+'\t'+str(year)+'\t'+to_print+'\n')
	f.close()


	# write the generated mappings in the file
	venue_file = dataset+"/mappings/"+dataset+'_venue_mapping.txt'
	f1 = open(venue_file, 'w')
	author_file = dataset+"/mappings/"+dataset+'_author_mapping.txt'
	f2 = open(author_file, 'w')
	title_file = dataset+"/mappings/"+dataset+'_title_mapping.txt'
	f3 = open(title_file, 'w')

	print("Writing venue mappings in " + venue_file)
	for venue in venue_dict:
		venue_cleaned = venue.lower()
		venue_cleaned = "".join(venue_cleaned.split(' '))		
		f1.write(venue_dict[venue_cleaned]+"\t"+venue+"\n")

	print("Writing author mappings in " + author_file)
	for author in author_dict:
		f2.write(author_dict[author]+"\t"+author+"\n")

	print("Writing title mappings in " + title_file)
	for title in title_dict:
		f3.write(title_dict[title]+"\t"+title+"\n")

	f1.close()
	f2.close()
	f3.close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Create test data')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \nacm')

	args = parser.parse_args()

	dataset = args.dataset

	print("Converting unmapped data to mapped data for " + dataset + " dataset")

	unmapped_to_mapped(dataset)


