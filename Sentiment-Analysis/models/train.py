import gensim
import numpy as np
import pandas as pd
from pyvi import ViTokenizer
import keras
from keras.utils.vis_utils import plot_model
import matplotlib.pyplot as plt
import sklearn.model_selection as sk
from keras.layers import LSTM, Bidirectional, Dropout
from keras.layers.core import Dense
from keras.models import Sequential
import numpy as np
from sklearn.utils import shuffle 
#pathModelBin='./data/vnw2v_classifier.bin'

pathModelBin='./data/vnw2v.bin'
word_size = 100
sen_size = 120
def get_data_rate(path):
    data = pd.read_csv(path)
    data = data.sample(frac=1)
    data= data[0:500]
    x_set = comments_to_vectors(data['Comment'])
    # Y_set
    y = data['Rate'].values
    y_set = np.zeros((len(x_set), 5))
    for i in range(len(x_set)): 
        y_set[i][y[i]-1] = 1 
    return x_set, y_set

def get_data_classifier(path):
    data = pd.read_csv(path)
    data = data.sample(frac=1)
    data= data[0:500]
    x_set = comments_to_vectors(data['Comment'])
    # Y_set
    y = data['Type'].values
    y_set = np.zeros((len(x_set), 2))
    for i in range(len(x_set)):
        y_set[i][y[i]] = 1
    return x_set, y_set

def comments_to_vectors(comments):
    w2v_model = gensim.models.KeyedVectors.load_word2vec_format(pathModelBin, fvocab=None, binary=True)
    sentences = [[word if (word in w2v_model.vocab) else 'gì' for word in ViTokenizer.tokenize(i).split(' ')] for i in comments] #mảng 2 chiều 1 chiều câu 1 chiều số từ trong câu
    vectors = np.zeros((len(sentences), sen_size, word_size)) #mảng 3 chiều
    for i in range(len(sentences)): #số các câu
        for j in range(len(sentences[i])): #số lượng các từ trong câu 
            if j < sen_size:
                vectors[i][j] = np.array(w2v_model.wv[sentences[i][j]]) # lstm k đọc đc list truyền về array (sentences[i][j] là từ thứ j của câu thứ i )(vector[i][j] là 1 câu 1 chiều là các từ 1 chiều là từ chuyển hóa vector) 
            else:
                break
    return vectors

def SAV():
    model = Sequential()
    model.add(Bidirectional(LSTM(16, return_sequences=False),
                            input_shape=(sen_size, word_size)))  
    model.add(Dropout(0.2))
    #model.add(Bidirectional(LSTM(32)))  
    #model.add(Dropout(0.2))
    model.add(Dense(5, activation="softmax"))
    optimizer = keras.optimizers.RMSprop(lr=0.0005, decay=1e-8)
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model

def Classifier():
    model = Sequential()
    model.add(Bidirectional(LSTM(32, return_sequences=False),
                            input_shape=(sen_size, word_size)))  
    model.add(Dropout(0.2))
    model.add(Dense(2, activation="softmax"))
    optimizer = keras.optimizers.RMSprop(lr=5e-5, decay=0)
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model

def visualize_model():
    model = SAV()
    model.summary()
    plot_model(model, to_file="./data/model_plot.png", show_shapes=True, show_layer_names=True)

def predict_comments(comments):
    model = SAV()
    model.load_weights('./weights-rate-new-lr=0.0005-decay=1e-8.h5')
    rates = model.predict(comments_to_vectors(comments))
    for rate, cmt in zip(rates, comments):
        starts = 0
        for i in range(5):
            starts = starts + (i + 1) * rate[i]
        print("Rate: {0}, Average rate: {1:.2f},  Comment: {2}".format(np.argmax(rate)+1, starts, cmt))
    pass

def predict_type(comments):
    comments = [cmt.lower() for cmt in comments]
    model = Classifier()
    approval.load_weights('./weights-filter-lr=5e-5-decay0-epoch100-lstm32.h5')
    types = model.predict(comments_to_vectors(comments))
    for type, cmt in zip(types, comments):
        print("Type: {0},  Comment: {1}".format(type, cmt))
    pass

def train_classifier(pathdata, epochs, is_continue=False):
    x_set, y_set = get_data_classifier(pathdata)
    x_set, y_set = shuffle(x_set, y_set, random_state=0)    
    x_train, x_val, y_train, y_val = sk.train_test_split(x_set, y_set, test_size=0.2, random_state=36)
    x_val, x_test, y_val, y_test = sk.train_test_split(x_val, y_val, test_size=0.5)
    model = Classifier()
    if is_continue:
        model.load_weights("./train-classifier/weights5.h5")
    # training
    print("Train.......")
    mc = keras.callbacks.ModelCheckpoint('./train-classifier/weights{epoch:02d}.h5', save_weights_only=True, period=2)
    history = model.fit(x_train, y_train, batch_size=128, epochs=epochs, validation_data=(x_val, y_val), callbacks=[mc]) #bắt đầu train

    evaluate = model.evaluate(x_test, y_test, verbose = 1)
    print(evaluate)

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

def train_rate(pathdata, epochs, is_continue=False):
    x_set, y_set = get_data_rate(pathdata)
    x_set, y_set = shuffle(x_set, y_set, random_state=0)        
    x_train, x_val, y_train, y_val = sk.train_test_split(x_set, y_set, test_size=0.2, random_state=36)
    x_val, x_test, y_val, y_test = sk.train_test_split(x_val, y_val, test_size=0.5)
    model = SAV()
    if is_continue:
        model.load_weights("./train-rate/weights.h5")
    # training
    print("Train.......")
    mc = keras.callbacks.ModelCheckpoint('./train-rate/weights{epoch:02d}.h5', save_weights_only=True, period=1)
    history = model.fit(x_train, y_train, batch_size=128, epochs=epochs, validation_data=(x_val, y_val), callbacks=[mc])

    evaluate = model.evaluate(x_test, y_test, verbose = 1)
    print(evaluate)
    
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

if __name__ == '__main__':
    visualize_model()
    #train_rate("./data/lazada-dongho-raw3.csv", is_continue=False, epochs=50)
    #train_classifier("./data/classifier_data.csv", is_continue=False, epochs=100)
