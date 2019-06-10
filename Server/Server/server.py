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
graph = tf.get_default_graph() # gộp model và flask cùng luồng

app = Flask(__name__)
CORS(app)

@app.route('/chatbot', methods=['POST'])
def rep():
    question = request.form['Question']
    answer = get_answer_from_question(question)
    print(question)
    print(answer)
    return answer.replace(' . ', '. ').replace('_', ' ')

@app.route('/sav', methods=['POST'])
def get_sentiment():
    comment = request.form['Comment']
    rate = predict_sentiment([comment])
    #x = int(float(rate))
    #y = float(rate)%1
    #if(y<0.5):
    #    y=0
    #else:
    #    y=1
    #rate = x+y
    return '{0}'.format(rate)

@app.route('/approval', methods=['POST'])
def get_type():
    comment = request.form['Comment']
    type = predict_type([comment])
    print(comment)
    print(type)
    if type[1] > 0.5:
        return '1'
    else:
        return '0'
def predict_type(comments):
    comments = [cmt.lower() for cmt in comments]
    with graph.as_default(): 
        types = approval.predict(comments_classifier_to_vectors(comments))
    return types[0]

def Classifier():
    approval = Sequential()
    approval.add(Bidirectional(LSTM(32, return_sequences=False),
                            input_shape=(cf.sen_size, cf.word_size)))  
    approval.add(Dropout(0.2))
    #approval.add(Bidirectional(LSTM(32)))  # return a single vector of dimension 32
    #approval.add(Dropout(0.2))
    approval.add(Dense(2, activation="softmax"))
    optimizer = keras.optimizers.RMSprop(lr=5e-5, decay=0)
    approval.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=optimizer,
                  metrics=['accuracy'])
    approval.load_weights('./weights-filter-lr=5e-5-decay0-epoch100-lstm32.h5')
    return approval

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
    try:
        end = results.rindex('EOS')
    except:
        end = len(results - 1)
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

w2v_rate = gensim.models.KeyedVectors.load_word2vec_format(cf.pathModelRateBin, fvocab=None, binary=True)
def comments_to_vectors(comments):
    sentences = [[word if (word in w2v_rate.vocab) else 'gì' for word in ViTokenizer.tokenize(i).split(' ')] for i in comments]
    #vectors = np.zeros((len(sentences), cf.sen_size, cf.word_size))
    vectors = np.zeros((len(sentences), 120, 100))
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            if j < cf.sen_size:
                vectors[i][j] = np.array(w2v_rate.wv[sentences[i][j]])
            else:
                break
    return vectors

w2v_classifier = gensim.models.KeyedVectors.load_word2vec_format(cf.pathModelClassifierBin, fvocab=None, binary=True)
def comments_classifier_to_vectors(comments):
    sentences = [[word if (word in w2v_classifier.vocab) else 'gì' for word in ViTokenizer.tokenize(i).split(' ')] for i in comments]
    vectors = np.zeros((len(sentences), cf.sen_size, cf.word_size))
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            if j < cf.sen_size:
                vectors[i][j] = np.array(w2v_classifier.wv[sentences[i][j]])
            else:
                break
    return vectors


def SAVModel():
    model = Sequential()
    model.add(Bidirectional(LSTM(16, return_sequences=False),
                            input_shape=(120, 100)))  # returns a sequence of vectors of dimension 64 input_shape=(cf.sen_size, cf.word_size)
    model.add(Dropout(0.2))
    #model.add(Bidirectional(LSTM(32)))  # return a single vector of dimension 32
    #model.add(Dropout(0.2))
    model.add(Dense(5, activation="softmax"))
    optimizer = keras.optimizers.RMSprop(lr=0.0005, decay=1e-8) #tối ưu hóa - learning rate 
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=optimizer,
                  metrics=['accuracy']) #optimizer hàm tối ưu
    #model.load_weights('./weights-rate-new-lr=0.0005-decay=1e-8.h5')
    #model.load_weights('./weights100.h5') #ngon
    model.load_weights('./weights100ratenew.h5') 
    return model


def predict_sentiment(comments):
    with graph.as_default():
        rates = sav.predict(comments_to_vectors(comments))
        print(comments)
        print(rates)
    max_rate_index = np.argmax(rates)
    print(max_rate_index+1)
    #for rate, cmt in zip(rates, comments):
    #    starts = 0
    #    for i in range(5):
    #        starts = starts + (i + 1) * rate[i]
    return '{0}'.format(max_rate_index + 1)


#for sentiment predict
sav = SAVModel()
approval = Classifier()

if __name__ == '__main__':
    app.run(host='localhost', port=9874, debug=True)
