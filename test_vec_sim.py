import vectorizer
import numpy as np
import pandas as pd
from vectorizer import vectorize
import similarity
from similarity import find_all_cos, get_top_n
def load_corpus(file_name):
    """
    Loads the corpus from the given file.

    Parameters:
    file_name (str): The name of the file containing the corpus.

    Returns:
    pd.dataframe: a pandas dataframe containing the corpus.
    """
    return pd.read_csv(file_name, header=None,encoding="utf-8")

def pick_columns(corpus, columns):
    """
    Picks the given columns from the given matrix.

    Parameters:
    corpus (pd.DataFrame):a pandas dataframe the corpus loaded from a csv
    columns (list): The list of columns to be picked.

    Returns:
    a pandas dataframe containing the picked columns.
    """
    return corpus[columns].dropna()
    


def vectorize_selection(titles, contents, ngrams, test_type, representation):
    """
    Does all the tests for the given data.

    Parameters:
    titles (pd.DataFrame): The titles of the documents.
    contents (pd.DataFrame): The contents of the documents.
    ngrams (tuple): The range of ngrams to be used.
    type (str): if the test is only the titles, contents or both.
    representation (str): The representation to be used. Binary, frequency or tfidf.    

    Returns:
    np.array: The vectorized representation of the contents.
    """
    
    if test_type == 'titles':
        test_corpus = titles
    elif test_type == 'contents':
        test_corpus = contents
    else: #it concatenates the titles and contents in a single string
        test_corpus = titles + ' ' + contents
        
    #it makes the vectorzation of the corpus and 
    return vectorize(representation, test_corpus, ngrams).toarray() #it returns the vectorized representation of the corpus


def main():
    # Load the corpus
    corpus = load_corpus('corpus.csv') #into a dataframe

    titles = pick_columns(corpus, 1)
    contents = pick_columns(corpus, 2)

    test_type = ['titles', 'contents', 'both']
    representation = ['binary', 'frequency', 'tfidf']
    ngrams = [1, 2]
    
    #Given a new o a set of new documents, it vectorizes the documents and finds the most similar documents in the corpus. Using all combinations of the given parameters.
    new_entry = {"titles": "Ciegos y débiles visuales viven experiencia sensorial en torno al fenómeno de abril",
                 "contents": "Mazatlán, Sin., Las comunidades ciega y débil visual recibieron capacitación para percibir a través del tacto el eclipse solar total, que se observará el 8 de abril, en un taller impartido por el astrofísico Mario De Leo Winkler, director de comunicación del Conocimiento de la Universidad Autónoma Metropolitana (UAM).", 
                 "both": "Ciegos y débiles visuales viven experiencia sensorial en torno al fenómeno de abril Mazatlán, Sin., Las comunidades ciega y débil visual recibieron capacitación para percibir a través del tacto el eclipse solar total, que se observará el 8 de abril, en un taller impartido por el astrofísico Mario De Leo Winkler, director de comunicación del Conocimiento de la Universidad Autónoma Metropolitana (UAM)."}
    
    all_test = []
    for t in test_type:
        for r in representation:
            for n in ngrams:
                
                vec = vectorize_selection(titles, contents, n, t, r)
                #vectorize new entry but keeping the same representation (Same vector) as the vocabulary in the corpus (titles ans contents)
                
                all_test.append([[t, r, n, i] for i in all_similarities])
                
                
                print("\n")
    print(all_test)
    
   
   
    
    

    


if __name__ == "__main__":
    main()