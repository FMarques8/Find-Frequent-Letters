# utils file with functions used in script 
# F Marques - January 2023
from collections import Counter
from random import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# COUNTERS
def exact_counter(stream: list[str], counts: Counter = Counter()) -> dict: 
    """
    Returns dict with exact counts of items in given list.
    """
    tmp_counts = Counter(stream) # Counts each letter in the stream
    counts = {l: counts.get(l, 0) + tmp_counts.get(l, 0)
                for l in set(counts).union(tmp_counts)}
        
    return counts

def approximate_counter(stream: list[str], counts: dict = {}, k: float = 0.125) -> dict:
    """
    Returns dict with approximate counts of items
    Counts are expected to be k = 1/8 of the exact counts, but as it uses probabilistic counting, results may difer from expected
    """
    for item in stream:
        try:
            if random() <= k: # fixed probability 1/8
                counts[item] += 1
                
        # if item not in dictionary, add it with value 1 if the toss coin is successful
        except KeyError:
            if random() <= k:
                counts[item] = 1
                
    return counts

def scale_counts(counts: dict, k: float = 0.125):
    """Returns dict with scaled counts from approximate counter."""
    new_counts = {item: int(total/k) for item, total in counts.items()}
    
    return new_counts

# STATISTICAL AND GRAPHICAL FUNCTIONS
def get_statistics(data: list) -> dict:
    """
    Returns dictionary with several statistical information
    Assumes list only has information about one of the letters counted
    """
    summary = {'mean': np.mean(data), 'median': np.median(data), 
               'stdev': np.std(data), 'var': np.var(data)}
    
    return summary


def plot_hist(data: list, item: str):
    "Plots the histogram of the input data"



def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))