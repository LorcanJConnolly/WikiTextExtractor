# The WikiTextExtractor
WikiTextExtractor.py is a Python script for a web scraper which extracts and cleans visible English text from Wikipedia Articles to create a frequency list, in order to study Zipf’s Law in Wikipedia articles. This script is designed for the creation of small to medium datasets.

## Necessary Libraries
-
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
