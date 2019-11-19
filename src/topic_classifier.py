from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle
import codecs


class TopicClassifier():

    """ Class constructor """
    def __init__(self,classes_dict:dict, tokenizer_path:str, max_words:int, path_to_h5_classifier:str=None, num_classes:int=None, vocab_size:int=None):
        """
        - tokenizer must be the same used for training
        """
        self._classes_dict = classes_dict
        with open(tokenizer_path, 'rb') as handle:
            self._tokenizer = pickle.load(handle)
        self._maxlen = max_words

        if path_to_h5_classifier:
            try:
                self._model = keras.models.load_model(path_to_h5_classifier)
                self._trained = True
            except:
                print("Unable to load file at path: "+path_to_h5_classifier)
        elif (max_words is not None) and (num_classes is not None) and (vocab_size is not None):
            
            # set parameters:
            self._max_features = vocab_size
            self._batch_size = 8
            self._embedding_dims = 20
            self._filters = 200
            self._kernel_size = 3
            self._hidden_dims = 200
            self._epochs = 16
            self._num_classes = num_classes

            # Build model
            model = Sequential()

            # we start off with an efficient embedding layer which maps
            # our vocab indices into embedding_dims dimensions
            model.add(Embedding(self._max_features,
                                self._embedding_dims,
                                input_length=self._maxlen))
            model.add(Dropout(0.2))

            # we add a Convolution1D, which will learn filters
            # word group filters of size filter_length:
            model.add(Conv1D(self._filters,
                            self._kernel_size,
                            padding='valid',
                            activation='relu',
                            strides=1))
            # we use max pooling:
            model.add(GlobalMaxPooling1D())

            # We add a vanilla hidden layer:
            model.add(Dense(self._hidden_dims))
            model.add(Dropout(0.2))
            model.add(Activation('relu'))

            # We project onto a single unit output layer, and squash it with a sigmoid:
            model.add(Dense(self._num_classes))
            model.add(Activation('softmax'))

            model.compile(loss='categorical_crossentropy',
                        optimizer='adam',
                        metrics=['accuracy'])

            self._model = model
            self._trained = False
            
        else:
            raise ValueError("When model is not specified you need to set model parameters")

                    

    """ Classifies a news topic according the the macro-topics EconomicsTopics and OtherTopics, and the specific
    economics topics CompaniesEconomy, Markets&Goods, NationalEconomy
    @:param news title of the news to classify
    @:return tuple indicating the specific topic of the news and the macro-topic """
    def classify_news(self, news: str) -> tuple:
        news_sequenced = self._tokenizer.texts_to_sequences([news])

        news_ready = pad_sequences(news_sequenced, padding='post', maxlen=self._maxlen)
        predicted = self._model.predict_classes(news_ready)
        return self._classes_dict[predicted[0]]
    
    def train_and_save(self, X_train, y_train, X_test, y_test, path):
        self._model.fit(X_train, y_train,
          batch_size=self._batch_size,
          epochs=self._epochs,
          validation_data=(X_test, y_test))
        
        self._model.save(path)
        



if __name__=="__main__":

    max_words = 400
    num_classes=4

    filepath_dict = {
                    'a': './resources/news_scraper_files/news_utf8.csv',
                    #'b': './resources/news_labeled/news_b.txt'
                    }

    df_list = []
    for source, filepath in filepath_dict.items():
        df = pd.read_csv(filepath, names=['date','sentence','link','label'], sep=',', encoding="utf8")
        df['source'] = source  # Add another column filled with the source name
        df_list.append(df)
    df = pd.concat(df_list)
    df = df.sample(frac=1).reset_index(drop=True)
    df = df.dropna()

    print(df['sentence'])
    

    sentences = df['sentence'].values
    labels = df['label'].apply(lambda x: x.replace(' ',''))
    labels = labels.apply(lambda x: x.replace(';','')).values
    
    print(labels)
    
    sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.25)

    le = LabelEncoder()
    y_train=le.fit_transform(y_train)
    y_test=le.fit_transform(y_test)

    dict_classes = {i:le.classes_[i] for i in range(len(le.classes_))}
    print(dict_classes)

    ohe = OneHotEncoder()
    y_train = ohe.fit_transform(y_train.reshape(-1,1)).toarray()
    y_test = ohe.fit_transform(y_test.reshape(-1,1)).toarray()

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(sentences_train)

    X_train = tokenizer.texts_to_sequences(sentences_train)
    X_test = tokenizer.texts_to_sequences(sentences_test)

    vocab_size = len(tokenizer.word_index) + 1  # Adding 1 because of reserved 0 index

    X_train = pad_sequences(X_train, padding='post', maxlen=max_words)
    X_test = pad_sequences(X_test, padding='post', maxlen=max_words)

    #Save Tokenizer
    with open('./resources/keras_model_classifier/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    tc = TopicClassifier(classes_dict=dict_classes,tokenizer_path='./resources/keras_model_classifier/tokenizer.pickle',max_words=max_words, num_classes=num_classes, vocab_size=vocab_size)
    tc.train_and_save(X_train,y_train,X_test,y_test, path="./resources/keras_model_classifier/model_prova.h5")

    print(sentences_test[0])
    print(tc.classify_news(sentences_test[0]))
    
