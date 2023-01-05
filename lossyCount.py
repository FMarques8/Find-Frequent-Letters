# Class file for the implementation of a Lossy counter
# Based and adapted from http://www.cs.emory.edu/~cheung/Courses/584/Syllabus/07-Heavy/Manku.html
# https://gist.github.com/giwa/bce63f3e2bd493167d92
# and http://www.cs.emory.edu/~cheung/Courses/584/Syllabus/07-Heavy/Manku.html
# F Marques - Jan 2023

from collections import defaultdict


class LossyCounter():
    """
    Class for a Lossy counter
    """
    
    def __init__(self, epsilon: float = 0.1):
        self._epsilon = epsilon
        self._n = 0
        self._count = defaultdict(int)
        self._bucket_id = {}
        self._current_bucket_id = 1
        
    def get_count(self, item):
        """Return the number of the item"""
        return self._count[item]
    
    def get_bucket_id(self, item):
        """Return the bucket id corresponding to the item"""
        return self._bucket_id[item]
    
    def add_count(self, item):
        """Add item for counting"""
        self._n += 1
        if item not in self._count:
            self._bucket_id[item] = self._current_bucket_id - 1
        self._count[item] += 1
        
        # when bucket fills up, trim the data structure
        if self._n % int(1/ self._epsilon) == 0:
            self._trim()
            self._current_bucket_id += 1
    
    def _trim(self):
        "Trim data which does not fit the criteria"
        for item, total in self._count.copy().items():
            if total <= self._current_bucket_id - self._bucket_id[item]:
                del self._count[item]
                del self._bucket_id[item]


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))