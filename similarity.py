# Description: This file contains the similarity functions used in the project
import numpy as np
import scipy.sparse
    
def vec_cos(v1: list[int], v2:list[int]):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def find_all_cos(v1: list[int], all_vectors: scipy.sparse._csr.csr_matrix):
    """
        all_vectors ('scipy.sparse._csr.csr_matrix'): The vectorized representation of the corpus.
    """ 
    return np.dot(all_vectors, v1) / (np.linalg.norm(all_vectors, axis=1) * np.linalg.norm(v1))
    
def get_top_n(similarity: list[int], n: int):
    """
    similarity (list): The list of similarities.
    n (int): The number of top similarities to be returned.
    """
    return np.argsort(similarity)[-n:][::-1]