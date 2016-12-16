#!/usr/bin/env python

"""
This is a simple script to train an LSTM model for generating scientific 
article titles. 
To use default arguments, simply run in your terminal using

    python lstmtrainer.py

If you wish to use custom arguments, just run

    python lstmtrainer.py -h
    
to get a list of the arguments you can pass.

NOTE:
The following code is heavily based on the following keras example:
https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py
(see contributors for credits)

"""

from __future__ import print_function
import numpy as np
import random
import os
import sys
import argparse
from keras.models import Sequential 
from keras.layers import LSTM, Dense, Activation
from keras.optimizers import RMSprop

__author__ = "Jacopo Credi"
__license__ = "MIT"
__version__ = "1.4.1-rc"
__email__ = "jacopo.credi@gmail.com"

parser = argparse.ArgumentParser(description='Trains an LSTM for scientific paper titles generation.')
parser.add_argument('--dataDumpPath', dest='dump_file_path', default=os.getcwd()+'/data_dump/arxiv_dump.csv', 
    help='Path to text corpus file. Default: "<current_working_directory>/data_dump/arxiv_dump.csv"')
parser.add_argument('--sequenceLength', dest='seq_length', type=int, default=40, help='Length of sequences to be extracted from the corpus. Default: 40')
parser.add_argument('--step', dest='step', type=int, default=3, help='Steps by which the corpus will be cut into sequences. Default: 3')
parser.add_argument('--lstmUnits', dest='lstm_units', type=int, default=128, help='Number of LSTM units. Default: 128')
parser.add_argument('--epochs', dest='epochs', type=int, default=60, help='Number of training epochs. Default: 60')
parser.add_argument('--learningRate', dest='learning_rate', type=float, default=0.01, help='Learning rate used by the RMSprop optimizer. Default: 0.01')
parser.add_argument('--batchSize', dest='batch_size', type=int, default=128, help='Mini-batch size. Default: 128')
parser.add_argument('--temperature', dest='temperature', type=float, default=0.5, help='Controls the randomness level in the generation of new sequences. Default: 0.5')
parser.add_argument('--outputSequenceLength', dest='output_seq_length', type=int, default=400, help='Length of the generated text to be displayed after each epoch. Default: 400')

args = parser.parse_args()

# retrieve dumped data
titles = []
with open(args.dump_file_path, 'r') as data_dump_file:
    for line in data_dump_file:
        titles.append(line.rstrip())
        
corpus = '. '.join(titles)
print('Corpus length:', len(corpus))

chars = sorted(list(set(corpus)))
print('Total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = args.seq_length
step = args.step
sequences = []
next_chars = []
for i in range(0, len(corpus) - maxlen, step):
    sequences.append(corpus[i: i + maxlen])
    next_chars.append(corpus[i + maxlen])
print('Number of sequences:', len(sequences))

print('One-hot vectorization...')
X = np.zeros((len(sequences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
for i, sequence in enumerate(sequences):
    for t, char in enumerate(sequence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(args.lstm_units, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=args.learning_rate)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each epoch
for epoch in range(1, args.epochs):
    print()
    print('-' * 50)
    print('Epoch ', epoch)
    model.fit(X, y, batch_size=args.batch_size, nb_epoch=1)

    start_index = random.randint(0, len(corpus) - maxlen - 1)
    generated = ''
    sequence = corpus[start_index: start_index + maxlen]
    generated += sequence
    print('----- Generating with seed: "' + sequence + '"')
    sys.stdout.write(generated)

    for i in range(args.output_seq_length):
        x = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sequence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, args.temperature)
        next_char = indices_char[next_index]

        generated += next_char
        sequence = sequence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
print()
