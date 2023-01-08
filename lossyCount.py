# Class file for the implementation of a Lossy counter
# Based and adapted from http://www.cs.emory.edu/~cheung/Courses/584/Syllabus/07-Heavy/Manku.html
# and https://gist.github.com/giwa/bce63f3e2bd493167d92
# F Marques - Jan 2023

from collections import defaultdict


class LossyCounter():
    """
    Class for a Lossy counter
    """
    
    def __init__(self, k: int = 3):
        self._k = k
        self._n = 0
        self._count = defaultdict(int)
        self._delta = {}
        self._current_bucket_id = 1
    
    def add_count(self, item):
        """Add item for counting"""
        self._n += 1
        if item not in self._count:
            self._delta[item] = self._current_bucket_id - 1 # delta/error
        self._count[item] += 1
        
        # when bucket fills up, trim the data structure
        if self._n % self._k == 0:
            self._trim()
            self._current_bucket_id += 1
    
    def _trim(self):
        "Trim data which does not fit the criteria"
        for item, total in self._count.copy().items():
            if total + self._delta[item] <= self._current_bucket_id: 
                del self._count[item]
                del self._delta[item]


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))