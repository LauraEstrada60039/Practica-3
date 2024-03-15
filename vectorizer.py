from sklearn.feature_extraction.text import CountVectorizerThe
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def vectorize_frequency(corpus, ngram_len):
    """
    Vectorizes the given corpus using a frequency-based approach.

    Parameters:
    corpus (list): A list of strings representing the corpus to be vectorized.
    ngram_len (int): The length of the n-grams to be considered.

    Returns:
    sparse matrix: A sparse matrix representing the vectorized corpus.
    """

    # Load the vectorizer if it exists
    try:
        with open('freq_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
    except:
        vectorizer = CountVectorizer(ngram_range=(1, ngram_len))
        vectorizer.fit(corpus)
        with open('freq_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
    return vectorizer.transform(corpus)


def vectorize_binary(corpus, ngram):
    """
    Vectorizes the given corpus using a binary vectorizer.

    Parameters:
    corpus (list): A list of strings representing the corpus to be vectorized.
    ngram (int): The maximum size of the n-grams to be considered.

    Returns:
    scipy.sparse.csr_matrix: The binary vectorized representation of the corpus.
    """
    # Load the vectorizer if it exists
    try:
        with open('binary_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
    except:
        vectorizer = CountVectorizer(ngram_range=(1, ngram), binary=True)
        vectorizer.fit(corpus)
        with open('binary_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
    return vectorizer.transform(corpus)


def vectorize_tfidf(corpus, ngram):
    """
    Vectorizes the given corpus using TF-IDF representation.

    Parameters:
    corpus (list): A list of strings representing the corpus to be vectorized.
    ngram (int): The maximum number of consecutive words to consider as a single feature.

    Returns:
    scipy.sparse.csr_matrix: The TF-IDF representation of the input corpus.
    """
    # Load the vectorizer if it exists
    try:
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
    except:
        vectorizer = TfidfVectorizer(ngram_range=(1, ngram))
        vectorizer.fit(corpus)
        with open('tfidf_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
    return vectorizer.transform(corpus)


def vectorize(type:str, corpus:str, ngram_len:int):
    """
    Vectorizes the given corpus based on the specified type and ngram length.

    Parameters:
    - type (str): The type of vectorization to perform. Valid options are 'frequency', 'binary', and 'tfidf'.
    - corpus (str): The input corpus to be vectorized.
    - ngram_len (int): The length of the ngrams to be used for vectorization.

    Returns:
    - The vectorized representation of the input corpus.

    Raises:
    - ValueError: If an invalid type is specified.
    """
    if type == 'frequency':
        return vectorize_frequency(corpus,ngram_len)
    elif type == 'binary':
        return vectorize_binary(corpus,ngram_len)
    elif type == 'tfidf':
        return vectorize_tfidf(corpus,ngram_len)
    else:
        raise ValueError('Invalid type')