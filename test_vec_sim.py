import vectorizer
import numpy as np
import pandas as pd
from vectorizer import vectorize
import similarity
from similarity import find_all_cos #, get_top_n
from normalizer import normalize_text
np.set_printoptions(precision=15, suppress=True, threshold=np.inf, linewidth=np.inf)

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
    vect, vectorizer = vectorize(representation, test_corpus, ngrams)
    #it makes the vectorzation of the corpus and 
    return  vect.toarray(), vectorizer#it returns the vectorized representation of the corpus

def get_table(corpus='corpus.csv', new_entry=None, ngrams=[1], representation=["binary"],top=5):
    '''
    Given a new o a set of new documents, it vectorizes the documents and finds the most similar documents in the corpus. Using all combinations of the given parameters.
    Parameters:
        corpus (str): The name of the file containing the corpus.
        new_entry (dict): A dictionary containing the new documents to be compared.
        ngrams (list): The range of ngrams to be used.
        representation (list): The representation to be used. Binary, frequency or tfidf.
        top (int): The number of top similar documents to be returned.
    Returns:
        str: A string containing the html table with the results.
    '''
    # Load the corpus
    corpus = load_corpus('corpus.csv') #into a dataframe

    titles = pick_columns(corpus, 1)
    contents = pick_columns(corpus, 2)    
    all_test = []
    all_similarities = []
    for t in new_entry:
        for r in representation:
            for n in ngrams:
                
                vec, vectorizer = vectorize_selection(titles, contents, n, t, r)
                #vectorizes new entry but keeping the same representation (Same vector) as the vocabulary in the corpus (titles ans contents)

                new_vec = vectorizer.transform([new_entry[t]]).toarray()
                #dump new_vec and vec into a file                
                all_cosines = find_all_cos(new_vec,vec)

                all_cosines_indexed = [(i, all_cosines[i]) for i in range(len(all_cosines))]
                all_cosines_indexed.sort(key=lambda x: x[1], reverse=True)

                #get_top_n Returns index and value
                get_top_n = lambda x, n: [x[i] for i in range(n)]
                top_n = get_top_n(all_cosines_indexed, 5)
                
                all_test.append([t, r, n, top_n])   
   #uses all_test to create a html table with the results
    html = "<html><head><title>Test Results</title></head><body><table><tr><th>Test Type</th><th>Representation</th><th>Ngram</th><th>Top 5 similar documents</th></tr>"
    for test in all_test:
        test[3] = [f'{i[0]}: {i[1][0]}' for i in test[3]]
        test[3] = '<br>'.join(test[3])  
        html += f"<tr><td>{test[0]}</td><td>{test[1]}</td><td>{test[2]}</td><td>{test[3]}</td></tr>"
    html += "</table></body></html>"

    return html
    #Para poner el resultado en un archivo
    #with open('test_results.html', 'w') as f:
    #    f.write(html)
    
#Test main
'''  
def main():
    # Load the corpus
    corpus = load_corpus('corpus.csv') #into a dataframe

    titles = pick_columns(corpus, 1)
    contents = pick_columns(corpus, 2)

    test_type = ['titles', 'contents', 'both']
    representation = ['binary', 'frequency', 'tfidf']
    ngrams = [1, 2]
    
    #Given a new o a set of new documents, it vectorizes the documents and finds the most similar documents in the corpus. Using all combinations of the given parameters.
    new_entry = {"inversion de contenido":"Durante el año pasado, los mexicanos invirtieron 6 mil 429 millones de dólares en proyectos de largo plazo en el extranjero. Ese monto –principalmente destinado a la ampliación de operaciones de empresas nacionales en América Latina, España, Francia, Alemania y Estados Unidos– representa una caída de más de 50 por ciento a tasa anual, revelan datos oficiales"}
    
    new_entry["inversion de contenido"] = normalize_text(new_entry["inversion de contenido"])

    
    all_test = []
    all_similarities = []
    for t in new_entry:
        for r in representation:
            for n in ngrams:
                
                vec, vectorizer = vectorize_selection(titles, contents, n, t, r)
                #vectorizes new entry but keeping the same representation (Same vector) as the vocabulary in the corpus (titles ans contents)

                new_vec = vectorizer.transform([new_entry[t]]).toarray()
                #dump new_vec and vec into a file                
                all_cosines = find_all_cos(new_vec,vec)

                all_cosines_indexed = [(i, all_cosines[i]) for i in range(len(all_cosines))]
                all_cosines_indexed.sort(key=lambda x: x[1], reverse=True)

                #get_top_n Returns index and value
                get_top_n = lambda x, n: [x[i] for i in range(n)]
                top_n = get_top_n(all_cosines_indexed, 5)
                
                all_test.append([t, r, n, top_n])
                
            
    
               # print(f"Test type: {t}, Representation: {r}, Ngram: {n}, Top 5 similar documents: {top_n}")
                
   #uses all_test to create a html table with the results
    html = "<html><head><title>Test Results</title></head><body><table><tr><th>Test Type</th><th>Representation</th><th>Ngram</th><th>Top 5 similar documents</th></tr>"
    for test in all_test:
        test[3] = [f'{i[0]}: {i[1][0]}' for i in test[3]]
        test[3] = '<br>'.join(test[3])  
        html += f"<tr><td>{test[0]}</td><td>{test[1]}</td><td>{test[2]}</td><td>{test[3]}</td></tr>"
    html += "</table></body></html>"
   
    with open('test_results.html', 'w') as f:
        f.write(html)

    #print(all_test)
    #print(all_similarities)
    #print(all_cosines_indexed)
    #print(top_n)
    #print(new_vec)
    #print(vec)
    #print(vectorizer)  


if __name__ == "__main__":
    main()
'''