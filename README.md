# Find-Frequent-Letters
### By Francisco Marques 
Exact, probabilistic and lossy counters to find most frequent letters in a given text file

![Data stream illustration](https://user-images.githubusercontent.com/73106020/218272786-8b12f911-0124-4dc7-88a9-66a2a36ec014.jpg)

Image sourced from slide 2 @ https://slideplayer.com/slide/12948043/

### Goal
Frequency count of letter in given data stream, currently simulated using downloaded books from Project Gutenberg (https://www.gutenberg.org/), in various languages

### Usage
Main file → find-frequent-items.py 

The functions <i>main</i> and <i>save_stats</i> are responsible for the frequency counting and the statistical data generation, respectively. Simply place downloaded books into the folder <i>books</i>.

### Final thoughts
Achieved expected results in every counter except in the Lossy counter which for most values of k did not performed the expected counting, displaying in most counters empty dictionaries.

In the future, it would be very interesting to implement a scraping algorithm to automatically downloaded books from the website and then count.

Feel free to use this algorithm and for any questions just message me directly.
