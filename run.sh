#!/bin/sh
DATASET="acm"
GRAPHTYPE="clique"

SAMPLES_LENGTH=100
NUM_SAMPLES=30

CLASSIFICATION_METHODS='lr dt rf nb'

# # creating mapped file from unmapped
echo "running unmapped_to_mapped.py"
python unmapped_to_mapped.py -d ${DATASET} 	

# # Creating train data from mapped
echo "running create_train.py"
python create_train.py -d ${DATASET} -g ${GRAPHTYPE}

# # Creating test data from mapped
echo "running create_test.py"
python create_test.py -d ${DATASET} 

# # Creating random data from mapped
echo "running create_random.py"
python create_random.py -d ${DATASET} 

# crorpus and sampling genreations
echo "running corpus_generate.py"
python corpus_generate.py -d ${DATASET} --samples_length ${SAMPLES_LENGTH} --num_samples ${NUM_SAMPLES} --graphtype ${GRAPHTYPE} -k 1
python corpus_generate.py -d ${DATASET} --samples_length ${SAMPLES_LENGTH} --num_samples ${NUM_SAMPLES} --graphtype ${GRAPHTYPE} -k 2
python corpus_generate.py -d ${DATASET} --samples_length ${SAMPLES_LENGTH} --num_samples ${NUM_SAMPLES} --graphtype ${GRAPHTYPE} -k 3

echo "running embedding_word2vec.py"
python embedding_word2vec.py -f ${DATASET}/${DATASET}_sampling_1_${GRAPHTYPE}.csv
python embedding_word2vec.py -f ${DATASET}/${DATASET}_sampling_2_${GRAPHTYPE}.csv
python embedding_word2vec.py -f ${DATASET}/${DATASET}_sampling_3_${GRAPHTYPE}.csv

echo "running compute_hadamard_new.py"
python compute_hadamard_new.py -d ${DATASET} -m khop -k 1 -g ${GRAPHTYPE}
python compute_hadamard_new.py -d ${DATASET} -m khop -k 2 -g ${GRAPHTYPE}
python compute_hadamard_new.py -d ${DATASET} -m khop -k 3 -g ${GRAPHTYPE}

echo "running eval.py"
for CLASSIFICATION_METHOD in $CLASSIFICATION_METHODS;
do
	echo ${CLASSIFICATION_METHOD}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model khop -k 1 -g ${GRAPHTYPE}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model khop -k 2 -g ${GRAPHTYPE}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model khop -k 3 -g ${GRAPHTYPE}
done

echo "STARTING FOR NODE2VEC"
# -----------------------------------
# FOR NODE2VEC

# CONVERT a_132 to all integer indexed since node2vec requires that
echo "running convert_mapped_to_int.py"
python convert_mapped_to_int.py -d ${DATASET} -g ${GRAPHTYPE}

# build intermediate node2vec file
echo "running node2vec/main.py"
python node2vec/src/main.py --input ${DATASET}/${DATASET}_train_int_${GRAPHTYPE}.txt --output node2vec/emb/${DATASET}/${DATASET}_${GRAPHTYPE}.bin --dimensions 100 --workers 44

# converting to required format
echo "running node2vec/run.py"
python node2vec/run.py -d ${DATASET} -f node2vec/emb/${DATASET}/${DATASET}_${GRAPHTYPE}.bin -g ${GRAPHTYPE}

echo "running compute_hadamard_new.py"
python compute_hadamard_new.py -d ${DATASET} -m metapath2vec -g ${GRAPHTYPE}

echo "running eval.py"
for CLASSIFICATION_METHOD in $CLASSIFICATION_METHODS;
do
	echo ${CLASSIFICATION_METHOD}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model node2vec -g ${GRAPHTYPE}
done
# -----------------------------------



# -----------------------------------
# FOR METAPATH2VEC

# GENERATE THE ACA METAPATHS FILE
python metapath2vec.py -d ${DATASET} -g ${GRAPHTYPE}

# generate the intermediate methapath2vec file
./metapath2vec/metapath2vec -train metapath2vec/m2v_data/${DATASET}/aca.txt -output metapath2vec/m2v_data_emb/${DATASET}/aca -pp 0 -size 100 -window 7 -negative 5 -threads 44

# craete the embedding file in required format
python metapath2vec/run.py -d {DATASET} -f metapath2vec/m2v_data_emb/${DATASET}/aca_clique.txt -g ${GRAPHTYPE}

python compute_hadamard_new.py -d ${DATASET} -m metapath2vec -g ${GRAPHTYPE}

for CLASSIFICATION_METHOD in $CLASSIFICATION_METHODS;
do
	echo ${CLASSIFICATION_METHOD}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model metapath2vec -g $GRAPHTYPE
done
# -----------------------------------


# -----------------------------------
# FOR VERSE

# GENERATE THE ACA VERSE FILE
python verse/python/convert.py --format edgelist ${DATASET}/${DATASET}_train_${GRAPHTYPE}.csv verse/data/${DATASET}_${GRAPHTYPE}.bcsr

# generate the intermediate verse file
./verse/src/verse -input verse/data/${DATASET}_${GRAPHTYPE}.bcsr -output verse/data/${DATASET}/${DATASET}_${GRAPHTYPE}.bin -dim 100 -threads 44

# craete the embedding file in required format
python verse/run.py -d ${DATASET} -g ${GRAPHTYPE} -dim 100

python compute_hadamard_new.py -d ${DATASET} -m verse -g ${GRAPHTYPE}

for CLASSIFICATION_METHOD in $CLASSIFICATION_METHODS;
do
	echo ${CLASSIFICATION_METHOD}
	python eval.py -d ${DATASET} -m ${CLASSIFICATION_METHOD} -model verse -g ${GRAPHTYPE}
done
# -----------------------------------
