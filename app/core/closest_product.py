from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode
import pandas as pd
import numpy as np
import string


def find_closest(dataframe, product):
    x_train = dataframe['product']
    x_train = ["".join([char for char in desc if char not in string.punctuation]) for desc in x_train]
    x_train = [unidecode(desc) for desc in x_train]
    x_train = pd.DataFrame(data=x_train)
    x_train = x_train[0]

    x_test = "".join([char for char in product.lower() if char not in string.punctuation])
    x_test = unidecode(x_test)
    x_test = pd.DataFrame(data=[x_test])
    x_test = x_test[0]

    tfidfvectorizer = TfidfVectorizer(analyzer='char', ngram_range = (1,3))
    tfidf_wm = tfidfvectorizer.fit(x_train)

    tfidf_train = tfidf_wm.transform(x_train)
    tfidf_test = tfidf_wm.transform(x_test)
    
    result = []
    for product_tfidf in tfidf_test:
        vector_cosine = cosine_similarity(product_tfidf, tfidf_train)
        index = np.argmax(vector_cosine[0])
        result.append((dataframe['product'][index], vector_cosine[0][index]))

    return result[0]