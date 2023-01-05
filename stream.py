# Processes text files as a 'stream' 
# F Marques - December 2022
import string
import nltk
from nltk.corpus import stopwords
import unidecode
from utils import exact_counter, approximate_counter, scale_counts
from collections import Counter
from lossyCount import LossyCounter
from itertools import chain

nltk.download('stopwords') #downloads stopwords list

######
# a medida que se le o ficheiro
# usar dicionarios, nao e preciso usar hash tables
# verificar se a ordem das k most frequent letters se mantem
# usar muitos contadores
# Use Counter class for exact counting
# repetir contagem para varios epsilons (no caso do lossy count) 
# para encontrar optimal width
######


class Stream:
    """
    A class for converting text files into a data stream for use with counters and hashtables.
    
    It has one parameter:
    - 'path' the path to the text file.
    """
    def __init__(self, path: str):
        self._path = path
        # Counters for the data stream
        self.exact_count = Counter() 
        self.approx_count = {}
        self.lossy_count = LossyCounter(0.02) # epsilon < 1 to produce results
        self._nlines = 0 # number of lines read, might be interesting for some statistics
        self._process() # cleans file and counts while streaming
        
    # class methods
    def _process(self):
        """
        Process the file, cleaning and counting while streaming the file
        """
        with open(self._path, 'r', encoding= 'UTF-8') as file:
            header = True # line  where Project Gutenberg header ends
            language = None # language input for stopwords
            
            # COUNT WHILE PROCESSING EACH LINE
            for line in file:
                if line.startswith('Language: '):
                    language = line.strip().split()[-1].lower()
                    continue
                elif line.startswith("*** START OF THE PROJECT GUTENBERG EBOOK"): # end of Project Gutenberg's header
                    header = False
                    continue
                elif header:
                    continue
                elif line.startswith("End of Project Gutenberg's") or line.startswith("*** END OF THE PROJECT GUTENBERG"): # end of text 
                    break
                
                line = self._clean_line(line, language)
                if line == []: # skips empty lines
                    continue
                
                self._nlines += 1 # increments the number of lines read

                # COUNTERS
                # Creates list with list of letters in line, ready to be used by the counters
                stream = list(chain.from_iterable(line))
                
                # Exact counter
                self.exact_count = exact_counter(stream, self.exact_count)
                
                # Lossy counter and approximate counter
                for item in stream:
                    self.lossy_count.add_count(item)

                # Approximate counter with fixed probability 1/8
                self.approx_count = approximate_counter(stream, self.approx_count, 0.125)

    def _clean_line(self, line: list[str], language: str) -> list[str]:
        """
        Returns clean line that is stripped, split and has had the stopwords removed, accordingly to nltk.corpus.stopwords
        """
        
        stop_words = list(map(str.upper,stopwords.words(language))) # converts stopwords list to uppercase
        punctuation = string.punctuation + '—'+'“'+ '’'+ '”' # these extra characters flared up for certain texts, might be other ones that were missed
        line_split = unidecode.unidecode(line).translate(str.maketrans('', '', punctuation)).split() #removes all punctuation
        #removes stop words and numbers, 'not any' to remove numbers with type str, unidecode removes string accents 
        line_split_nostop = [word.upper() for word in line_split if word not in stop_words and not any(letter.isdigit() for letter in word)]
        
        return line_split_nostop


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))