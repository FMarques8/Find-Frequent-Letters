# utils file with functions used in script 
# F Marques - January 2023
from collections import Counter
from random import random
import numpy as np
import pandas as pd
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
def mean_absolute_error(exact_count: dict, approx_df: pd.DataFrame, n: int) -> dict:
    """
    Returns mean absolute errors of dataframe.
    """
    error = {item: 0 for item in exact_count} # initialize error dict

    for i in range(n+1):
        tmp_data = approx_df.iloc[i, :]
        error = {col: error[col] + abs(exact_count[col] - tmp_data[col]) for col in error}
        
    error = {col: error[col]/n for col in error}
    return error

def mean_relative_error(mae: dict, approx_df: pd.DataFrame, n: int) -> dict:
    """
    Returns mean relative errors of dataframe.
    """
    
    for i in range(n+1):
        tmp_data = approx_df.iloc[i, :]
        error = {col: mae[col] / tmp_data[col] for col in mae}
        
    return error

def get_stats(approx_count: dict, df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Returns DataFrame with several statistical measures"""

    stats_df = df.describe().round(4) # describe() already produces several statistical information 
    mae = mean_absolute_error(approx_count, approx_df = df, n= n) # mean absolute error
    stats_df.loc['mae',:] = mae
    mre = mean_relative_error(mae, approx_df = df, n = n) # mean relative error
    stats_df.loc['mre',:] = mre 
    mad = (df - df.mean()).abs().mean() # mean absolute deviation
    stats_df.loc['mad',:] = mad

    return stats_df

def plot_hist(data: list, items: list[str]):
    "Plots the histogram of the input data"
    sns.histplot(data = data[items], stat = 'count', bins = 10)
    plt.xlabel('Frequency')
    plt.ylabel("Counts of the letter")
    plt.title("Histogram of the counts of given letters")
    plt.show()


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))