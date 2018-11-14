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


test_files = [ 'test', 'random']


def eval(files, dataset, khop, method):
	f_exist = csv.reader(open(dataset+'/'+dataset+'_'+files[0]+'_scores_hadamard_concat'+'.txt'), delimiter=' ')
	f_non_exist = csv.reader(open(dataset+'/'+dataset+'_'+files[1]+'_scores_hadamard_concat'+'.txt'), delimiter=' ')
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
		
	data_header = range(1,301)  # for 100 features, since it discards last one
	data_header.append("Label")
	data_final = pd.DataFrame.from_records(embeddings, columns=data_header)
	result_final = []
	train_percents = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	# train_percents = [0.9]
	for train_percent in train_percents:
		macro_score = []
		micro_score = []
		auc_score = []
		avg_prec_score = []
		prec_rec_score = []
		accuracy = []
		count = 0
		print "Training " + method + " Classifier for  ", train_percent, " % of data"
		for count in range(0,10):
			train_x, test_x, train_y, test_y = train_test_split(data_final[data_header[:-1]], data_final[data_header[-1]], train_size = train_percent)
    #Train using logistic regression
			
			if method == 'lr':
				lr = linear_model.LogisticRegression()
				model = lr.fit(train_x, train_y)

			elif method == 'dt':
				clf = tree.DecisionTreeClassifier()
				model = clf.fit(train_x, train_y)

			elif method == 'rf':
				clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
				model = clf.fit(train_x, train_y)

			elif method == 'nb':
				clf = GaussianNB()
				model = clf.fit(train_x, train_y)
		
			mac_score = metrics.f1_score(test_y, model.predict(test_x), average = 'macro')
			macro_score.append(mac_score)
			mic_score = metrics.f1_score(test_y, model.predict(test_x), average = 'micro')
			micro_score.append(mic_score)
			ar_score = metrics.roc_auc_score(test_y, model.predict(test_x))
			auc_score.append(ar_score)
			avg_prec = metrics.average_precision_score(test_y, model.predict(test_x))
			avg_prec_score.append(avg_prec)
			acc = metrics.accuracy_score(test_y, model.predict(test_x), normalize=True)
			accuracy.append(acc)
		avg_mac = sum(macro_score)/10
		avg_mic = sum(micro_score)/10  
		avg_auc = sum(auc_score)/10
		avg_prec = sum(avg_prec_score)/10
		avg_acc = sum(accuracy)/10 
		result_final.append([method, train_percent, avg_mac, avg_mic, avg_auc, avg_prec, avg_acc])
		
	Eval_Measure = ['Method', 'Train_Percent', 'F-1_Macro', 'F-1_Micro', 'AUC', 'Avg_Precision', 'Accuracy' ]
	result_table = pd.DataFrame.from_records(result_final, columns=Eval_Measure)
	print(result_table)
	
	result_file_name = dataset+'/'+dataset+'_concat_result'+'.txt'
	print("Writing Evaluation in file")	
	with open(result_file_name, 'a+') as ff:
		ff.write(str(result_table))
		ff.write('\n')
	
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluate link prediction score using logistic regression classifier on edge features obtained using hadamard product.')
	parser.add_argument('-d','--dataset', dest='dataset', required=True,
			    help='Dataset. Choose among following: \ndblp \naminer \nacm')
	parser.add_argument('-k','--khop', dest='khop', required=True,
			    help='Number of hop')
	parser.add_argument('-m','--method', dest='method', required=True,
			    help='Choose training method. Choose among following: \nlr \ndt \nrf \nnb')
	args = parser.parse_args()
	# files = []
	# for f in args.file:
	# 	files.append(f)
	
	eval(test_files, args.dataset, args.khop, args.method)


