# The WikiTextExtractor
WikiTextExtractor.py is a Python script for a web scraper which extracts and cleans visible English text from Wikipedia Articles using their html content, to create a frequency list in order to study Zipf’s Law in Wikipedia articles. This script is designed for the creation of small to medium datasets.

## Necessary Libraries
-
## Usage
The user interacts with the WikiTextExtractor by running the `WikiTextExtractor.py` and defining the following inputs for initialization: 
- *The root url*: The WikiTextExtractor must be given a starting url. This url must be a Wikipedia article and must follow Wikipedia’s [Robots Exclusion Protocol ](https://en.wikipedia.org/wiki/Robots.txt) (see [https://en.wikipedia.org/robots.txt](https://en.wikipedia.org/robots.txt)).
- *The depth*: The WikiTextExtractor enters the article links on each article page in order of occurrence using a breadth-first traversal, therefore the inputted depth specifies the height of the breadth-first traversal. If the depth is set to `0`, the WikiTextExtractor will only visit the root and a width will not need to be given.
- *The width*: This is how many article links the WikiTextExtractor will visit on each article page. Since the WikiTextExtractor enters the article links on each article page in order of occurrence, the visited article links for a width `n` will be the first `n` article links. Setting the width to `None` visits all the article links.

Since the WikiTextExtractor is designed to build small to medium data sets, the depth and width have an upper limit. If you want to develop larger data sets from Wikipedia content, please scrape data from [Wikipedia database backup dumps](https://dumps.wikimedia.org/) ([for example](https://github.com/attardi/wikiextractor)).

## Code Walkthrough
The WikiTextExtractor is formed from 3 scripts:
-	`WikiTextExtractor.py`: Acts as the UI and produces the output.
-	`Wiki_Crawler.py`: The `Crawler` class which creates an instance of the WikiTextExtractor. Traverses through the article pages using their article links to extract observed text and other necessary contents.
-	`Content.py`: The `Content` class, creates an object which stores the contents of a visited article page to allow for easier retrieval of data.

Once the crawler is initialised using the user’s inputs (See *Usage*), an instance of the WikiTextExtractor is created from the `Crawler` class. 

The class method `parse` is called, which adopts the procedural programming paradigm to act as a readable entry and exit point for the WikiTextExtractor. 

The first step of the WikiTextExtractor is to call the `breadth_first_traversal` class method. This method moves the WikiTextExtractor according to a breadth-first travel – starting at the root Wikipedia article, the  WikiTextExtractor visits all of the article links on the root page (which can be thought of as the child nodes of the root node in a tree) before moving to the article links within the on the article pages of the article links (the next level of the tree, the child nodes of the root’s children nodes) and so on.

At each “visit” the Wikipedia article’s url is passed to the class method `get_content`. This method extracts the html content of the url as a `BeautifulSoup` object using the class method `get_html`, raising errors and returning `None` if no html content is available or if the url is not from a Wikipedia article page using the class method `is_wiki_url`. 

The class method `get_content` checks if the url has visited before – if not, the url is stored in the class attribute `visited` which maintains a reference to the urls of the Wikipedia articles that have been visited already.

Non-visible text is removed from the html (e.g., [hidden categories](https://en.wikipedia.org/wiki/Category:Hidden_categories)) and the article links are extracted to be used in the future for the breadth-first traversal.

From the html, the visible text of the article is extracted, and “non-words” are removed using regular expressions by calling the `clean_text` class method. 

An object is created in the `Content` class, which then stores a reference to the visited Wikipedia article’s url, cleaned visible text, and article links that have been extracted from the html. For testing purposes, the `return_removed` argument of the `clean_text` class method can be manually set to `True` to return a list of the “non-words” removed by the regular expressions, this will be then stored as an attribute in the `Content` class and returned in the output.

The `Content` object (referred to as a ‘webpage’ in the `parse` class method) is returned to the `parse` class method where the list of extracted words is formed into a frequency list (a `Counter()` container from the `collections` module).

The WikiTextExtractor is then repositioned to a new Wikipedia article using the `breadth_first_traversal` class method, and the algorithm repeats.

Once the journey is complete, the formed frequency list is returned as well as the lists of removed text if specified. The user is then able to select the output format of their extracted frequency list, either as a csv or excel spreadsheet.  
## Limitations
[PLACEHOLDER]
- TEXT EXTRACTION:
- Puncutation is stripped from words after extraction, this includes full-stops at the ends of abbreviations such as "Vol." creating a miss-count in word length (3 instead of 4).
- URLs are counted.
- Roman numerals create a bias as "V" will not be counted, but "I" or "II" will.
- Biases between languages due to the WikiTextExtractor only handling words formed of letters within the english alphabet.
## My To Do List
- Implement the 'good robot' check according to Wikipedia’s [Robots Exclusion Protocol ](https://en.wikipedia.org/wiki/Robots.txt) (see *Code Walkthrough*).
- Implement csv output, and implement the excel output to include a Zipf's law plot (also commonly referred to as a  [rank-size plot](https://en.wikipedia.org/wiki/Rank%E2%80%93size_distribution)).
- Further testing - Wikipedia has a paradigm for the html structure of their atricle's, however some authors do not follow these rules to the finest details. Further, there may be more "hidden content" within the html which I have no yet discovered.
- Further improvement of the regular expressions to handle some of the limitations and biases of the WikiTextExtractor (see *Limitations*).
