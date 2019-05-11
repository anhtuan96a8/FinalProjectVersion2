from keras.layers import Input, Embedding, LSTM, Dense, merge, Concatenate
from keras.optimizers import Adam, Adagrad
from keras.models import Model
import numpy as np

np.random.seed(1234)  # for reproducibility
import _pickle as cPickle
import os
import gensim
import json
import random

word_embedding_size = 100
sentence_embedding_size = 320
maxlen_input = 100
maxlen_output = 100
num_subsets = 100
Epochs = 100
BatchSize = 128  # Check the capacity of your GPU
dropout = .25
n_test = 1000

questions_file = 'Padded_context'
answers_file = 'Padded_answers'
weights_file = 'my_model_weights.h5'


def print_result(input):
    in_text = ''
    for t in input[0]:
        t = t.astype(int)
        if t < (dictionary_size - 2):
            w = index_to_word[t]
            in_text = in_text + w + ' '
    print('{0} :'.format(in_text))
    ans_partial = np.zeros((1, maxlen_input))
    ans_partial[0, -1] = 2  # the index of the symbol BOS (begin of sentence)
    for k in range(maxlen_input - 1):
        ye = model.predict([input, ans_partial])
        mp = np.argmax(ye)
        ans_partial[0, 0:-1] = ans_partial[0, 1:]
        ans_partial[0, -1] = mp
        if mp == 1:  # the index of EOS
            break
    text = ''
    for k in ans_partial[0]:
        k = k.astype(int)
        if k < (dictionary_size - 2):
            w = index_to_word[k]
            text = text + w + ' '
    return (text)


# **********************************************************************
# Reading a pre-trained word embedding and addapting to our vocabulary:
# **********************************************************************

w2v_model = gensim.models.KeyedVectors.load_word2vec_format('./data/word2vec.bin', fvocab=None, binary=True)
dictionary_size = len(w2v_model.vocab) + 1  # +1 for unknow token
index_to_word = [x for x in w2v_model.vocab]

embeddings_index = {}
for word in w2v_model.vocab:
    embeddings_index[word] = w2v_model.wv[word]

print('Found %s word vectors.' % len(embeddings_index))
embedding_matrix = np.zeros((dictionary_size, word_embedding_size))

i = 0
for word in w2v_model.vocab:
    embedding_vector = embeddings_index.get(word)

    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector
    i += 1

# ************************************************************************
# Loading the data:
# ************************************************************************

q = cPickle.load(open(questions_file, 'rb'))
a = cPickle.load(open(answers_file, 'rb'))
n_exem, n_words = a.shape

qt = q[0:n_test, :]
at = a[0:n_test, :]
q = q[n_test + 1:, :]
a = a[n_test + 1:, :]

print('Number of exemples = %d' % (n_exem - n_test))
step = int((n_exem - n_test) / num_subsets)
round_exem = step * num_subsets

# *******************************************************************
# Keras model of the chatbot:
# *******************************************************************

ad = Adagrad()

input_context = Input(shape=(maxlen_input,), dtype='int32', name='input_context')
input_answer = Input(shape=(maxlen_input,), dtype='int32', name='input_answer')
LSTM_encoder = LSTM(sentence_embedding_size, kernel_initializer='lecun_uniform')
LSTM_decoder = LSTM(sentence_embedding_size, kernel_initializer='lecun_uniform')
if os.path.isfile(weights_file):
    Shared_Embedding = Embedding(output_dim=word_embedding_size, input_dim=dictionary_size, input_length=maxlen_input)
else:
    Shared_Embedding = Embedding(output_dim=word_embedding_size, input_dim=dictionary_size, weights=[embedding_matrix], input_length=maxlen_input)
word_embedding_context = Shared_Embedding(input_context)
context_embedding = LSTM_encoder(word_embedding_context)

word_embedding_answer = Shared_Embedding(input_answer)
answer_embedding = LSTM_decoder(word_embedding_answer)

merge_layer = merge([context_embedding, answer_embedding], mode='concat', concat_axis=1)
out = Dense(int(dictionary_size/2), activation="relu")(merge_layer)

out = Concatenate()([context_embedding, out])

out = Dense(dictionary_size, activation="softmax")(out)

model = Model(input=[input_context, input_answer], output=[out])
model.summary()
model.compile(loss='categorical_crossentropy', optimizer=ad)

if os.path.isfile(weights_file):
    model.load_weights(weights_file)
# *************************************************************************
# Bot training:
# *************************************************************************
start_epoch = 0
start_step = 0
with open('status.txt', 'r') as file:
    line = file.readline()
    while line:
        [start_epoch, start_step, _] = line.split(',')
        line = file.readline()
    start_step = int(start_step) + step
    start_epoch = int(start_epoch)
print('Start frome epoch {0}, step {1}'.format(start_epoch, start_step))

for m in range(start_epoch, Epochs, 1):
    print('Start epoch {0}'.format(m))
    # Loop over training batches due to memory constraints:
    for n in range(start_step, round_exem, step):

        q2 = q[n:n + step]
        a2 = a[n:n + step]
        count = 0
        for i, sent in enumerate(a2):
            l = np.where(sent == 1)  # the position od the symbol EOS
            limit = l[0][0]
            count += limit + 1

        Q = np.zeros((count, maxlen_input))
        A = np.zeros((count, maxlen_input))
        Y = np.zeros((count, dictionary_size))

        # Loop over the training examples:
        count = 0
        for i, sent in enumerate(a2):
            ans_partial = np.zeros((1, maxlen_input))

            # Loop over the positions of the current target output (the current output sequence):
            l = np.where(sent == 1)  # the position of the symbol EOS
            limit = l[0][0]

            for k in range(1, limit + 1):
                # Mapping the target output (the next output word) for one-hot codding:
                y = np.zeros((1, dictionary_size))
                y[0, sent[k]] = 1

                # preparing the partial answer to input:
                ans_partial[0, -k:] = sent[0:k]

                # training the model for one epoch using teacher forcing:

                Q[count, :] = q2[i:i + 1]
                A[count, :] = ans_partial
                Y[count, :] = y
                count += 1

        print('Training epoch: %d, training examples: %d - %d' % (m, n, n + step))
        history = model.fit([Q, A], Y, batch_size=BatchSize, initial_epoch=m, epochs=m + 1, verbose=1)
        loss = history.history['loss'][0]
        # save status and weights
        with open('status.txt', 'a') as file:
            file.write('{0},{1},{2}\n'.format(m, n, loss))
        model.save_weights(weights_file, overwrite=True)

        num = random.randint(1, 900)
        test_input = qt[num:num + 1]
        print(print_result(test_input))
        train_input = q[num:num + 1]
        print(print_result(train_input))

    model.save_weights('./history/weights_{0}'.format(m), overwrite=True)
    start_step = 0