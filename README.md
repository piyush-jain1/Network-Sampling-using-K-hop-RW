## CODS COMAND 2019  

The datasets used for experimentation are:
* **DBLP**
* **ACM**

- DATASET = acm/dblp
- GRAPHTYPE = star/clique
- CLASSIFICATION_METHOD = lr/nb/rf/dt

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

#### Node2Vec
```
python convert_mapped_to_int.py -d ${DATASET} -g ${GRAPHTYPE}
```
```
python node2vec/src/main.py --input ${DATASET}/${DATASET}_train_int_${GRAPHTYPE}.txt --output node2vec/emb/${DATASET}/${DATASET}_${GRAPHTYPE}.bin --dimensions 100 --workers 44
```
Now we need to convert this binary embedding file to word2vec format:
```
python node2vec/run.py -d ${DATASET} -f node2vec/emb/${DATASET}/${DATASET}_${GRAPHTYPE}.bin -g ${GRAPHTYPE}
```

#### Metapath2Vec
First generate the contexts for each graph (ACA, APA and APC):
```
python metapath2vec.py -d ${DATASET} -g ${GRAPHTYPE}
```

Now for generating the embedding vectors for ACA:
```
./metapath2vec/metapath2vec -train metapath2vec/m2v_data/${DATASET}/aca.txt -output metapath2vec/m2v_data_emb/${DATASET}/aca -pp 0 -size 100 -window 7 -negative 5 -threads 44
```

To generate required embeddings:
```
python metapath2vec/run.py -d {DATASET} -f metapath2vec/m2v_data_emb/${DATASET}/aca_clique.txt -g ${GRAPHTYPE}
```

#### Verse
First convert the edgelist format of the graph to bcsr format:
```
python verse/python/convert.py --format edgelist ${DATASET}/${DATASET}_train_${GRAPHTYPE}.csv verse/data/${DATASET}_${GRAPHTYPE}.bcsr
```

Now, generate the embeddings using verse:
```
./verse/src/verse -input verse/data/${DATASET}_${GRAPHTYPE}.bcsr -output verse/data/${DATASET}/${DATASET}_${GRAPHTYPE}.bin -dim 100 -threads 44
```

Now we need to convert this binary embedding file to word2vec format:
```
python verse/run.py -d ${DATASET} -g ${GRAPHTYPE} -dim 100
```

### HADAMARD PRODUCT GENERATION FOR TEST EDGE (compute_hadamard.py)
Compute hadamard similarites of authors in test data.
```
python compute_hadamard_new.py -d ${DATASET} -m khop -k 1 -g ${GRAPHTYPE}
```

### EVALUATION OF CLASSIFICATION TASK
Evaluation:
```
python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model khop -k 1 -g ${GRAPHTYPE}
```
