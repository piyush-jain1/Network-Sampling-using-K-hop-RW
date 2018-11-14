# ICADL-18

## Pipeline:

### Step 1
The datasets used for experimentation are:
* **DBLP**
* **AMiner**
* **DBIS**

Create edgelists from raw data.
```
python3.6 graphs.py -d dblp
```

### Step 2
  Create embeddings from edgelists.

The methods for generating embeddings are:
* **Node2Vec**
* **Metapth2Vec**
* **Verse**

Replace _dblp_ with required dataset, _aca_ with required graph type and _100_ with required number of embedding dimension. The embeddings file is saved as _embeddings/dblp/**method**/aca.txt_ for below commands, where **method** is _node2vec_ or _verse_.

#### Node2Vec
First generate the binary embedding file:
```
python node2vec/src/main.py --input graphs/dblp/aca.edgelist --output node2vec/emb/dblp/aca.bin --dimensions 100 --workers 44
```
Now we need to convert this binary embedding file to word2vec format:
```
python3.6 node2vec/run.py -d dblp -f node2vec/emb/dblp/aca.bin -g aca
```

#### Metapath2Vec
First generate the contexts for each graph (ACA, APA and APC):
```
python3.6 metapath2vec.py -d dblp
```
The contexts are saved in _m2v_data/dblp_.

Now for generating the embedding vectors for ACA:
```
./metapath2vec/metapath2vec -train metapath2vec/m2v_data/dblp/aca.txt -output metapath2vec/m2v_data_emb/dblp/aca -pp 0 -size 100 -window 7 -negative 5 -threads 44
```
The crude embedding file is saved as _metapath2vec/m2v_data_emb/dblp/aca.txt_.

To generate required embeddings:
```
python3.6 metapath2vec/run.py -d dblp -f metapath2vec/m2v_data_emb/dblp/aca.txt -g aca
```
The embeddings file is saved as _embeddings/dblp/metapath2vec/aca.txt_

#### Verse
First convert the edgelist format of the graph to bcsr format:
```
python3.6 verse/python/convert.py --format edgelist graphs/dblp/aca.edgelist verse/data/dblp/aca.bcsr
```

Now, generate the embeddings using verse:
```
./verse/src/verse -input verse/data/dblp/aca.bcsr -output verse/data/dblp/aca.bin -dim 100 -threads 44
```

Now we need to convert this binary embedding file to word2vec format:
```
python3.6 verse/run.py -d dblp -g aca -dim 100
```

### Optional
Before going to step 3, make sure test and random edges exist for the required dataset. To create these files, run the following:
```
# Change dbis to your required dataset
python3.6 test.py -d dbis
```
This will create random.txt and test.txt in _test/dbis_. The number of edges in test.txt and random.txt can be configured by changing the value of SAMPLE_TEXT and SAMPLE_RANDOM in test.py.

### Step 3 
Compute hadamard similarites of authors in test data.
```
python3.6 compute_hadamard.py -d dblp -g aca -m verse
```
The author-author hadamard similarities is saved in _test_scores_hadamard/dblp/verse/aca/random.txt_ and _test_scores_hadamard/dblp/verse/aca/test.txt_.

### Step 4
Evaluation:
```
python eval.py test_scores_hadamard/dblp/verse/aca/test.txt test_scores_hadamard/dblp/verse/aca/random.txt eval/dblp/verse/aca.txt
```
This will save evaluation results as _eval/dblp/verse/aca.txt_.
