from joblib import load
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer

import youtube_api

model = load('model/model_PPL.pkl')
vec = load('model/vectorizer_CV.pkl')
tdidf = load('model/tfidf.pkl')

comments = pd.DataFrame([], columns=['Comments'])  # Shared comments variable


def analyze_comments(url, comments_number):
    global comments
    try:
        if comments.empty:
            comments = youtube_api.get_comments(url, comments_number)
        original_comments = comments.copy()

        # preprocessing
        def preprocess(text):
            webnet_lemmatizer = WordNetLemmatizer()
            stemmer = SnowballStemmer('english')
            stop_words = set(stopwords.words('english'))
            tokens = nltk.word_tokenize(text)
            tokens = [token.lower() for token in tokens if token.isalpha()]
            tokens = [token for token in tokens if token not in stop_words]
            tokens = [webnet_lemmatizer.lemmatize(token) for token in tokens]
            tokens = [stemmer.stem(token) for token in tokens]
            return ' '.join(tokens)

        comments['Comments'] = comments['Comments'].apply(preprocess)

        comments_vec = vec.transform(comments['Comments'])
        comments_vec = tdidf.transform(comments_vec)

        comments['SentimentRating'] = model.predict(comments_vec)

        res = pd.concat([original_comments['Comments'], comments['SentimentRating']], axis=1)

        return res
    except Exception as e:
        print("Analyzer comments failed")
        print(e)
        return pd.DataFrame([], columns=['Comments'])


def most_frequent_words(url, comments_number):
    global comments
    try:
        if comments.empty:
            comments = youtube_api.get_comments(url, comments_number)

        def preprocess(text):
            tokens = nltk.word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            tokens = [token.lower() for token in tokens if token.isalpha()]
            tokens = [token for token in tokens if token not in stop_words]
            return ' '.join(tokens)

        comments['Comments'] = comments['Comments'].apply(preprocess)

        words = nltk.tokenize.word_tokenize(' '.join(comments['Comments']))

        freq = nltk.FreqDist(words)

        return list(map(list, freq.most_common(10)))
    except Exception as e:
        print("Most frequent words failed")
        print(e)
        return list()


def sentiment_of_most_frequent_words(words):
    try:
        sentiment = []

        for word in words:
            words_vec = vec.transform([word[0]])
            words_vec = tdidf.transform(words_vec)
            sentiment.append([word[0], word[1], int(model.predict(words_vec)[0]), ''])

        for _ in sentiment:
            if _[2] < 0:
                _[3] = 'negative'
            elif _[2] > 0:
                _[3] = 'positive'
            else:
                _[3] = 'neutral'

        return sentiment
    except Exception as e:
        print("Sentiment of most frequent failed")
        print(e)
        return []
