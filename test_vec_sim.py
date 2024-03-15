import vectorizer
import similarity
import numpy as np
def load_corpus(file_name):
    """
    Loads the corpus from the given file.

    Parameters:
    file_name (str): The name of the file containing the corpus.

    Returns:
    list: A list of strings representing the corpus.
    """
    with open(file_name, 'r', encoding= 'utf-8') as f:
        return f.readlines()

def pick_colums(corpus, columns):
    """
    Picks the given columns from the given matrix.

    Parameters:
    corpus (list[list]): A list of lists representing the corpus loaded from a csv
    columns (list): The list of columns to be picked.

    Returns:
    list[list]: A list of lists representing the corpus with only the selected columns.
    """
    return [[row[i] for i in columns] for row in corpus]



def main():
    # Load the corpus
    corpus = load_corpus('corpus.csv')
    

    titles = pick_colums(corpus, [1])
    contents = pick_colums(corpus, [2])
    
    # Vectorize the corpus
    vectorized = vectorizer.vectorize('binary', corpus, 1)
    
    print (vectorized)
 
    


if __name__ == "__main__":
    main()