'''
Pick the hadamard score(which is embedding for the author pair result) for various models
-node2vec
-metapath2vec
-verse
-word2vec khop
	1
	2
	3
	concat
and do classification task using 
	lr
	dt
	rf
	nb

ex. python eval.py -d acm -m lr -model khop -k 2 -g clique
ex. python eval.py -d acm -m lr -model verse -g clique
'''
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import os
import os.path
import argparse
import pandas as pd
import numpy as np
from sklearn import linear_model, tree
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import csv


test_files = ['test', 'random']


def eval(files, dataset, classification_method, model, graphtype, khop="-1"):
	if model == "metapath2vec":
		filename_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[0] + '_metapath2vec' + '_'+ graphtype +'.txt'
		filename_non_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[1] + '_metapath2vec' + '_'+ graphtype +'.txt'
	elif model == "node2vec":
		filename_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[0] + '_node2vec' + '_'+ graphtype +'.txt'
		filename_non_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[1] + '_node2vec' + '_'+ graphtype +'.txt'
	elif model == "verse":
		filename_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[0] + '_verse' + '_'+ graphtype +'.txt'
		filename_non_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[1] + '_verse' + '_'+ graphtype +'.txt'
	elif model == "concat":
		filename_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[0] + '_concat' + '_'+ graphtype +'.txt'
		filename_non_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[1] + '_concat' + '_'+ graphtype +'.txt'
	elif model == "khop":
		filename_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[0] + '_khop_'+ khop + '_'+ graphtype +'.txt'
		filename_non_exists = dataset + '/hm_scores/' + dataset + '_' +test_files[1] + '_khop_'+ khop + '_'+ graphtype +'.txt'
	f_exist = csv.reader(open(filename_exists), delimiter=' ')
	f_non_exist = csv.reader(open(filename_non_exists), delimiter=' ')
	print ("reading the embeddings file(hadamard scores)", filename_exists)
	print ("reading the embeddings file(hadamard scores)", filename_non_exists)
	embeddings = []
	Eval_Measure = []
	for lines in f_exist:
		data1 = lines[2:]
		data1.append(1)
		embeddings.append(data1)
		
	for lines in f_non_exist:
		data2 = lines[2:]
		data2.append(0)
		embeddings.append(data2)
	
	if model == "concat":
		data_header = range(1,301)  
	else:
		data_header = range(1,101)  # for 100 features, since it discards last one
	data_header.append("Label")
	data_final = pd.DataFrame.from_records(embeddings, columns=data_header)
	result_final = []
	# train_percents = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	train_percents = [0.8]
	for train_percent in train_percents:
		macro_score = []
		micro_score = []
		auc_score = []
		avg_prec_score = []
		prec_rec_score = []
		accuracy = []
		count = 0
		print "Training " + classification_method + " Classifier for  ", train_percent, " % of data"
		for count in range(0,10):
			train_x, test_x, train_y, test_y = train_test_split(data_final[data_header[:-1]], data_final[data_header[-1]], train_size = train_percent)
			if classification_method == 'lr':
				lr = linear_model.LogisticRegression()
				train_model = lr.fit(train_x, train_y)

			elif classification_method == 'dt':
				clf = tree.DecisionTreeClassifier()
				train_model = clf.fit(train_x, train_y)

			elif classification_method == 'rf':
				clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
				train_model = clf.fit(train_x, train_y)

			elif classification_method == 'nb':
				clf = GaussianNB()
				train_model = clf.fit(train_x, train_y)
		
			mac_score = metrics.f1_score(test_y, train_model.predict(test_x), average = 'macro')
			macro_score.append(mac_score)
			mic_score = metrics.f1_score(test_y, train_model.predict(test_x), average = 'micro')
			micro_score.append(mic_score)
			ar_score = metrics.roc_auc_score(test_y, train_model.predict(test_x))
			auc_score.append(ar_score)
			avg_prec = metrics.average_precision_score(test_y, train_model.predict(test_x))
			avg_prec_score.append(avg_prec)
			acc = metrics.accuracy_score(test_y, train_model.predict(test_x), normalize=True)
			accuracy.append(acc)
		avg_mac = sum(macro_score)/10
		avg_mic = sum(micro_score)/10  
		avg_auc = sum(auc_score)/10
		avg_prec = sum(avg_prec_score)/10
		avg_acc = sum(accuracy)/10 
		result_final.append([classification_method, train_percent, avg_mac, avg_mic, avg_auc, avg_prec, avg_acc])
		
	Eval_Measure = ['Method', 'Train_Percent', 'F-1_Macro', 'F-1_Micro', 'AUC', 'Avg_Precision', 'Accuracy' ]
	result_table = pd.DataFrame.from_records(result_final, columns=Eval_Measure)
	if model == "metapath2vec":
		result_file_name = dataset+'/classification_results/'+dataset+'_'+ model +'.txt'
	elif model == "node2vec":
		result_file_name = dataset+'/classification_results/'+dataset+'_'+ model +'.txt'
	elif model == "verse":
		result_file_name = dataset+'/classification_results/'+dataset+'_'+ model +'.txt'
	elif model == "concat":
		result_file_name = dataset+'/classification_results/'+dataset+'_'+ model +'.txt'
	elif model == "khop":
		result_file_name = dataset+'/classification_results/'+dataset+'_'+ model + '_' + khop +'.txt'	
	print("Writing Evaluation in file", result_file_name)	
	with open(result_file_name, 'a+') as ff:
		ff.write(str(result_table))
		ff.write('\n')
	
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluate link prediction score using logistic regression classifier on edge features obtained using hadamard product.')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \naminer \nacm')
	parser.add_argument('-k','--khop', dest='khop', default=1,
			    help='khop')
	parser.add_argument('-m','--classification_method', dest='classification_method', required=True,
			    help='Choose training method. Choose among following: \nlr \ndt \nrf \nnb')
	parser.add_argument('-model','--model', dest='model', required=True,
			    help='Choose model. Choose among following: \nmetapath2vec \nnode2vec \nverse \nconcat \n khop')
	parser.add_argument('-g','--graphtype', dest='graphtype', required=True,
			    help='Choose graphtype. Choose among following: \nclique \nstar')
	args = parser.parse_args()
	eval(test_files, args.dataset, args.classification_method, args.model, args.graphtype, args.khop)
