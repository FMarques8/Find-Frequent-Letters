# Main script for Finding Frequent Letters
# F Marques - January 2023

import utils
import stream
import pandas as pd
import numpy as np
import os
from IPython.display import display

def run_trials(stream: stream.Stream, n: int = 10):
    """
    Perform statistical analysis of n trials of the approximate counter
    """
    # Initialization
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = [*alphabet]

    # First pass dataframes, use the values from already available stream counters
    # Adds 0s to non counted letter here and not in the class as it would defeat the purpose of the Lossy counter
    tmp_df = pd.DataFrame([stream.approx_count[x] if x in stream.approx_count else 0 for x in alphabet],
                            index = alphabet, columns=['run1']).T
    
    # Now run the trials
    # Only the approx counter since exact and lossy (if epsilon == const) are constant
    for i in range(2,n+2):
        stream.reprocess()
        # get new dataframe for run i
        approx_df = pd.DataFrame([stream.approx_count[x] if x in stream.approx_count else 0 for x in alphabet],
                                index = alphabet, columns=[f'run{i}']).T
        tmp_df = pd.concat([tmp_df, approx_df], axis = 0) # adds new values as new row
        
    stream.approx_stats = utils.get_stats(stream.approx_count, tmp_df, n)
    utils.plot_hist(tmp_df, ['A'])
    display(tmp_df)
    return tmp_df

def load_streams() -> dict:
    """Loads Stream objects and returns dictionary with all of the data"""
    cwd = os.getcwd() + "/books" # folder with books
    data = {}
    K = [3, 5, 10] # diferent k values
    
    for file in os.listdir(cwd):
        file_stream = []
        for k in K:
            S = stream.Stream(file, k) # processes file with k value
            file_stream.append(S) # append to list with all k values
        data[file] = file_stream # appends list of Streams to main dictionary
    return data


def main():
    data = load_streams()


data = stream.Stream("Metamorphosis_Kafka.txt", k = 10)

print(data)
main()
#run_trials(data, 30)
# display(data.approx_stats)