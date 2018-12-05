## CODS COMAD 2019  

Network Sampling refers to the methodologies defined for preserving structural properties of the given network using representative node samples. Among various approaches, random walk based network sampling has received much popularity.  
Further, network sampling has many applications such as, 

Recently, it is observed that network sampling has been used widely for unsupervised network embedding tasks. 


Further, 
Network Sampling is an important pre-requisite for Unsupervised Network Embedding methods. 


The datasets used for experimentation are:
* **DBLP**
* **ACM**

You can download the datasets from this [link](https://drive.google.com/file/d/1wC1A_P3Gpe9GMXiN3akHqLTTwSCpQNVC/view?usp=sharing).


- DATASET = acm/dblp
- GRAPHTYPE = star/clique
- CLASSIFICATION_METHOD = lr/nb/rf/dt


## Dataset Preparation
1. We selected some of the top conferences for both ACM and DBLP from [here](http://www.conferencelist.info/targets.html).
2. We downloaded the bibiliographic information for both the datasets from [Aminer](https://aminer.org/citation) website.
3. We filtered the bibiliographic information for our selected list of conferences (step 1) which can be found in [acm/acm_conferences.txt](https://github.com/piyush-jain1/Network-Sampling-using-K-hop-RW/blob/master/acm/acm_conferences.txt) and [dblp/dblp_conferences.txt](https://github.com/piyush-jain1/Network-Sampling-using-K-hop-RW/blob/master/dblp/dblp_conferences.txt).


## Preparing Mapped file from unmapped [unmapped_to_mapped.py]
```
python unmapped_to_mapped.py -d ${DATASET} 	
```
## Preparing Train Dataset [create_train.py]
1. Read 'Title', 'Venue' , 'Year' & 'Author' columns for each row from the csv.
2. Checked for year prior to 2014 and 2016 for acm and dblp respectively
3. Star-based: added all title-author pairs and title-venue pairs.
   Clique-based: added all title-author pairs, author-venue pairs, and the corresponding title-venue pairs.

```
python create_train.py -d ${DATASET} -g ${GRAPHTYPE}
```

## Preparing Test Dataset [crate_test.py]
1. Read 'Title', 'Venue', 'Year' & 'Author' columns for each row from the csv.
2. For rows where year > 2013, cretaed a dictionary indexed by venue containing all the authors for that venue, a dictionary indexed by title containing all the authors for that title. Also stored a list of authors for year > 2013.
3. For rows where  year <= 2013, created a list of authors.
4. Iterated on all possible unique author-author pairs from year > 2013 (the list created in step 2) and checked following conditions: 
   a. If these two authors are connected directly to same venue
   b. If these two authors are connected directly to same title
   c. If any of the two authors are not present in train dataset (author list for year <= 2013, created in step 3)
   If none of the above three conditions are satisfied, add it to the list of test edges, otherwise not.

- For positive test edges
```
python create_test.py -d ${DATASET} 
```

- For negative test edges

```
python create_random.py -d ${DATASET} 
```

## CORPUS GENERATION and RW-k SAMPLING
```
python corpus_generate.py -d ${DATASET} --samples_length ${SAMPLES_LENGTH} --num_samples ${NUM_SAMPLES} --graphtype ${GRAPHTYPE} -k 1
```

##  EMBEDDING GENERATION
### WORD2VEC

```
python embedding_word2vec.py -f ${DATASET}/${DATASET}_sampling_1_${GRAPHTYPE}.csv
```


