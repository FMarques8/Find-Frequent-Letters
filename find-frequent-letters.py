# Main script for Finding Frequent Letters
# F Marques - January 2023

import utils
import stream
import pandas as pd
import os
from numpy import mean
from random import choice
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
    trial_df = pd.DataFrame([stream.approx_count[x] if x in stream.approx_count else 0 for x in alphabet],
                            index = alphabet, columns=['run1']).T
    
    exact_counts = stream.exact_most_common # exact most frequent counts
    # accuracy rating
    acc = []
    
    # adds if most frequent letters are in same order as exact
    if exact_counts.keys() == stream.approx_most_common.keys():
        acc.append(1)
    else:
        acc.append(0)
    
    # Now run the trials
    # Only the approx counter since exact and lossy (if epsilon == const) are constant
    for i in range(2,n+2):
        stream.reprocess()
        # get new dataframe for run i
        approx_df = pd.DataFrame([stream.approx_count[x] if x in stream.approx_count else 0 for x in alphabet],
                                index = alphabet, columns=[f'run{i}']).T
        trial_df = pd.concat([trial_df, approx_df], axis = 0) # adds new values as new row
        
        if exact_counts.keys() == stream.approx_most_common.keys():
            acc.append(1)
        
    stream.approx_stats = utils.get_stats(stream.approx_count, trial_df, n)
    
    return trial_df, acc

def load_streams(K: list[int]) -> dict[str, list[stream.Stream]]:
    """Loads Stream objects and returns dictionary with all of the data"""
    cwd = os.getcwd() + "/books" # folder with books
    data = {}
    
    for file in os.listdir(cwd):
        file_stream = []
        for k in K:
            S = stream.Stream(cwd + r"\\" + file, k) # processes file with k value
            file_stream.append(S) # append to list with all k values
        data[file] = file_stream # appends list of Streams to main dictionary
    return data



def save_stats(stats_data: tuple[str, list[stream.Stream]], K: list[int] = [3, 5, 10]) -> None:
    "Saves statistical data given dict with streams to text file."
    
    key, value = stats_data # unpack tuple
    author, title = utils.author_and_title(key)
    stats_data = value 

    # save statistical results to file
    with open("stats_results.txt", 'w') as f:
        f.write(f"statistics for {title} by {author}\n########################\n\n")
        for i, k in enumerate(K):
            # iterate over the streams and run trials
            curr_stream = stats_data[i]
            trial_df, acc = run_trials(curr_stream, n=100)
            f.write(f"""k = {k}\n
                    statistical data:\n\n
                    {trial_df.to_string(header=True)}\n\n
                    
                    statistical measures:\n\n
                    {curr_stream.approx_stats.to_string(header=True)}\n\n
                    
                    average accuracy rating:\n\n
                    {mean(acc)*100} %\n\n\n
                    """)
            
            most_frequent = [letter for letter in curr_stream.approx_most_common]
            utils.plot_counts(trial_df, most_frequent)
            utils.plot_hist(trial_df, most_frequent)


def main():
    K = [3, 5, 10] # diferent k values
    data = load_streams(K)
    
    # Save k-most frequent letters to text file
    with open("counter_results.txt", 'w') as f:
        f.write("results from counters\n######################\n\n")
        for key, item in data.items():
            author, title = utils.author_and_title(key)
            f.write(f"{title} by {author}:\n\n")
            for strm in item:
                f.write(str(strm))
                f.write("\n\n")
            f.write("\n")
    
    # Statistical data treatment
    stats_data = choice(list(data.items())) # choose a random file for the statistical testing
    save_stats(stats_data, K)


if __name__ == '__main__':
    main()