# The WikiTextExtractor
WikiTextExtractor.py is a Python script for a web scraper which extracts and cleans visible English text from Wikipedia Articles using their html content, to create a frequency list in order to study Zipf’s Law in Wikipedia articles. This script is designed for the creation of small to medium datasets.

## Necessary Libraries
-
## Usage
The user interacts with the WikiTextExtractor by running the WikiTextExtractor.py and defining the following inputs for initialization: 
- *The root url*: The WikiTextExtractor must be given a starting url. This url must be a Wikipedia article and must follow Wikipedia’s [Robots Exclusion Protocol ](https://en.wikipedia.org/wiki/Robots.txt) (see [https://en.wikipedia.org/robots.txt](https://en.wikipedia.org/robots.txt)).
- *The depth*: The WikiTextExtractor enters the article links on each article page in order of occurrence using a breadth-first traversal, therefore the inputted depth specifies the height of the breadth-first traversal. If the depth is set to '0', the WikiTextExtractor will only visit the root and a width will not need to be given.
- *The width*: This is how many article links the WikiTextExtractor will visit on each article page. Since the WikiTextExtractor enters the article links on each article page in order of occurrence, the visited article links for a width 'n' will be the first 'n' article links. Setting the width to 'None' visits all the article links.

Since the WikiTextExtractor is designed to build small to medium data sets, the depth and width have an upper limit. If you want to develop larger data sets from Wikipedia content, please scrape data from [Wikipedia database backup dumps](https://dumps.wikimedia.org/) ([for example](https://github.com/attardi/wikiextractor)).

## Code Walkthrough
-
## Output
-
## Limitations
[PLACEHOLDER]
- TEXT EXTRACTION:
- Puncutation is stripped from words after extraction, this includes full-stops at the ends of abbreviations such as "Vol." creating a miss-count in word length (3 instead of 4).
- URLs of the form "domain.com" are counted.
- "Only english words are counted" - really means only words using english letters, e.g., Latin is still counted in some cases.
- Roman numerals create a bias as "V" will not be counted, but "I" or "II" will.
## My To Do List
-
