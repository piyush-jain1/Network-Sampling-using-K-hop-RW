#!/bin/sh
DATASET="acm"
GRAPHTYPE="clique"

SAMPLES_LENGTH=100
NUM_SAMPLES=30

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


