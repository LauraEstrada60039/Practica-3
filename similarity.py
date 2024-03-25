# Description: This file contains the similarity functions used in the project
import numpy as np
import scipy.sparse
    
def vec_cos(v1: list[int], v2:list[int]):
    
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def find_all_cos(v1, all_vectors):
    return [vec_cos(v1,v2) for v2 in all_vectors]


    