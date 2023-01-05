# Main script for Finding Frequent Letters
# F Marques - January 2023

import utils
import stream
import pandas as pd
import os

data = stream.Stream("Metamorphosis_Kafka.txt")

# print("Exact count")
# print(data.exact_count)
# print("Lossy count")
# print(data.lossy_count._count)
# print("Approximate counter with probability 1/8")
# print(data.approx_count)

# print("scaled counts")
# print(utils.scale_counts(data.approx_count, k = 1/8))

def run_trials(stream: stream.Stream, n: int = 10):
    """
    Runs given Stream n times to gather statistical data
    """
    
    for i in range(n):
        stream._process()