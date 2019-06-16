import pandas as pd
from gensim.models import Word2Vec
from pyvi import ViTokenizer

pathData = './data/classifier_data.csv'
pathModelBin='./data/vnw2v_classifier.bin'
pathModelTxt='./data/vnw2v.txt'

if __name__ == '__main__':
    data = pd.read_csv(pathData)
    sentences = [ViTokenizer.tokenize(cmt).split(' ') for cmt in data['Comment']]
    # Create CBOW model
    model = Word2Vec(sentences, size=100, min_count=1, window=10, workers=4, sg=1)
    model.wv.save_word2vec_format(pathModelBin, fvocab=None, binary=True)
