from keras.layers import Input, Embedding, LSTM, Dense, merge, Bidirectional, Dropout
from keras.optimizers import Adagrad
from keras.models import Model
from keras.preprocessing import sequence
from flask import Flask, request,jsonify
from flask_cors import CORS
from keras.models import Sequential
import keras
import gensim
import numpy as np
from pyvi import ViTokenizer
import config as cf
import tensorflow as tf
global graph, chatbot, sav, approval
import json
graph = tf.get_default_graph()

app = Flask(__name__)
CORS(app)

@app.route('/chatbot', methods=['POST'])
def rep():
    question = request.form['Question']
    answer = get_answer_from_question(question)
    return answer.replace(' . ', '. ').replace('_', ' ')



def get_answer_from_question(question):
    # string to vector for question
    question = [word_to_index[word] if word in vocab else word_to_index['gì'] for word in ViTokenizer.tokenize(question.lower()).split(' ')]
    question = np.asarray(question)
    question = sequence.pad_sequences([question], maxlen=maxlen_input)

    # predict
    ans_partial = np.zeros((1, maxlen_input))
    ans_partial[0, -1] = 1  # the index of the symbol BOS (begin of sentence)
    for k in range(maxlen_input - 1):
        with graph.as_default():
            ye = chatbot.predict([question, ans_partial])
        mp = np.argmax(ye)
        ans_partial[0, 0:-1] = ans_partial[0, 1:]
        ans_partial[0, -1] = mp
        if mp == 0:  # the index of EOS
            break

    # array to string for rep result
    results = ''
    for k in ans_partial[0]:
        k = k.astype(int)
        if k < (dictionary_size - 2):
            w = index_to_word[k]
            results = results + w + ' '
    start = results.index('BOS') + 3
    end = results.rindex('EOS')
    results = results[start: end]
    return results


def ChatbotModel():
    ad = Adagrad()

    input_context = Input(shape=(maxlen_input,), dtype='int32', name='input_context')
    input_answer = Input(shape=(maxlen_input,), dtype='int32', name='input_answer')
    LSTM_encoder = LSTM(sentence_embedding_size, kernel_initializer='lecun_uniform')
    LSTM_decoder = LSTM(sentence_embedding_size, kernel_initializer='lecun_uniform')

    Shared_Embedding = Embedding(output_dim=word_embedding_size, input_dim=dictionary_size,
                                     input_length=maxlen_input)

    word_embedding_context = Shared_Embedding(input_context)
    context_embedding = LSTM_encoder(word_embedding_context)

    word_embedding_answer = Shared_Embedding(input_answer)
    answer_embedding = LSTM_decoder(word_embedding_answer)

    merge_layer = merge([context_embedding, answer_embedding], mode='concat', concat_axis=1)
    out = Dense(int(dictionary_size / 2), activation="relu")(merge_layer)
    out = Dense(dictionary_size, activation="softmax")(out)

    model = Model(input=[input_context, input_answer], output=[out])
    model.compile(loss='categorical_crossentropy', optimizer=ad)
    model.load_weights(weights_file)
    return model

# for chat bot
word_embedding_size = 100
sentence_embedding_size = 128
maxlen_input = 100
maxlen_output = 100
weights_file = 'weights_bot.h5'
w2v_model = gensim.models.KeyedVectors.load_word2vec_format('./data/word2vec.bin', fvocab=None, binary=True)
vocab = w2v_model.vocab
dictionary_size = len(vocab) + 1  # +1 for unknow token
index_to_word = [x for x in w2v_model.vocab]
word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])
chatbot = ChatbotModel()


if __name__ == '__main__':
    app.run(host='localhost', port=9874, debug=True)
