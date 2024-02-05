from urllib.parse import urlsplit
from bs4 import BeautifulSoup
# For regular expressions
import re
# HTTP
import requests
# Handling punctuation
import string
# Rate Limiting
import time
# Frequency list
from collections import Counter
# Removing punctuation from words
from string import punctuation

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
# FIXME: dont import unnecessary modules
# TODO: check for consistent use of '' and ""
from Content import Content


class Crawler:
    """
    Creates an instance of a WikiCrawler, starting from the root Wikipedia article and traversing through its
    displayed articles to extract displayed words.
    """
    def __init__(self, root):
        self.root = root
        self.base_url = self.split_url()
        self.visited = []

    def __iter__(self):
        for website in self.visited:
            yield website.getUrl()

    def split_url(self):
        """
        Returns the root url protocol and domain to later join to article paths.
        """
        components = urlsplit(self.root)
        base_url = f"{components.scheme}://{components.netloc}"
        return base_url

    @staticmethod
    def get_html(url):
        """
        Extracts the html and returns it as a BeautifulSoup object.
        """
        if not Crawler.is_wiki_url(url):
            print(f"The url {url} is not a wikipedia article link.")
            return None
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            print(f"REQUEST ERROR: status code {requests.get(url)}")
            return None
        return BeautifulSoup(req.text, 'html.parser')

    @staticmethod
    def is_wiki_url(url):
        try:
            components = urlsplit(url)
        except TypeError:
            print(f"TypeError splitting the url of {url}")
            return False
        netloc = components.netloc
        if netloc == "en.wikipedia.org" or netloc == "simple.wikipedia.org":
            return True
        else:
            return False

    def get_content(self, url):
        """
        Extracts the content from BeautifulSoup object and stores it as an instance of the Content class.
        Returns the created instance of the Content class.
        """
        # print(f"in getContent for: {url}")
        bs = self.get_html(url)
        if bs is None:
            print(f"The url {url} has no HTML content")
            return None
        webpage = Content(url)
        if webpage.get_url() in self.visited:
            print(f"Already visited {url} before")
            return None
        # --------------------------------------------------
        # Remove hidden elements from the Body Content div tag
        body_content = bs.find('div', {'id': 'bodyContent'})
        for element in body_content.find_all(True, {'style': True}):
            if 'display:none' in element['style']:
                element.decompose()
        for element in body_content.find_all('code'):
            element.decompose()
        hidden_cat = body_content.find('div', {'class': 'mw-hidden-catlinks mw-hidden-cats-hidden'})
        if hidden_cat is not None:
            hidden_cat.decompose()
        print_footer = body_content.find('div', {'class': 'printfooter'})
        if print_footer is not None:
            print_footer.decompose()
        # --------------------------------------------------
        # Get links
        article_links = []
        for link in bs.find('div', {'id': 'bodyContent'}).find_all(
                     'a', href=re.compile('^(/wiki/)((?!:).)*$')):
            article_links.append(f"{self.base_url}{link.attrs['href']}")
        # --------------------------------------------------
        # Get text
        title = bs.find('h1', {'id': 'firstHeading'}).get_text(separator=' ')
        raw_text = ' '.join([title, body_content.get_text(separator=' ')])
        clean_text_list, removed_text = self.clean_text(raw_text, return_removed=True)
        # --------------------------------------------------
        # Create object in Content class.
        webpage.store_text(clean_text_list)
        webpage.store_removed_text(removed_text)
        webpage.store_links(article_links)
        self.visited.append(webpage.get_url())
        return webpage

    @staticmethod
    def clean_text(raw_text, return_removed=False):
        """
        Uses regular expressions to return a list containing the displayed words.
        For testing, can return the removed text.
        """
        removed_text = False
        # TODO - test the second part of the re
        is_word_re = re.compile(r'^[\'\"(]?[a-zA-Z]+[a-zA-Z-\'.]*[a-zA-Z]+[\',!\")?:;.]*$'
                                r'|^[\'\"(]?[aAI][\',!\")?:;.]*$')
        # Horizontal bar, figure dash, em dash, en dash translation.
        translation_table = str.maketrans('―‒—–’/', "----\' ")
        raw_text = raw_text.translate(translation_table)
        if return_removed is True:
            removed_text = [text for text in raw_text.split() if not is_word_re.match(text)]
        clean_text_list = [text.strip(string.punctuation).lower()
                           for text in raw_text.split() if is_word_re.match(text)]
        return clean_text_list, removed_text

    def parse(self, url=None, depth=None, width=None, extract_excel=False, file_directory=None):
        """
        It's a method that creates a visible iterator using that paradigm.
        """
        frequency_list = Counter()
        for webpage in self.breadth_first_traversal(url, depth, width):
            frequency_list.update(webpage.get_text())
        return frequency_list.most_common()

    def breadth_first_traversal(self, url, depth, width=None):
        """
        Preforms a breath first traversal of the article links displayed on a Wikipedia article.
        """
        queue = [url]
        curr_depth, curr_width = 0, 0
        while queue:
            curr_url = queue.pop(0)
            # Decrease the speed of the webscraper for friendliness.
            time.sleep(1)
            webpage = self.get_content(curr_url)  # creates a webpage object from the url
            if webpage is not None:
                yield webpage
                if curr_depth < depth:
                    for link in webpage.get_links():
                        if width is None or curr_width <= width:
                            queue.append(link)
                            curr_width += 1
                    curr_depth += 1
                    curr_width = 0
            else:
                # raise error - url returned none from get content
                # But ultimately nothing will happen - None - no links extracted - no links to traverse - traversal stop
                # Do we want to return where the scraper stopped unexpectedly?
                pass

    @staticmethod
    def create_excel(name, file_directory, frequency_list):
        """
        Creates an Excel workbook which displays the gathered data and creates a log(Rank) vs log(Frequency) plot to
         analyse Zipf's Law in the data.
        """
        wb = Workbook()
        ws = wb.active
        ws.append(["Word", "Frequency"])
        for word, frequency in frequency_list.items():
            ws.append([word, frequency])
        table = Table(displayName="Frequency_List", ref=f"A1:B{len(frequency_list)+1}")
        # Applying a style to the table
        style = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=True
        )
        table.tableStyleInfo = style
        ws.add_table(table)
        if file_directory:
            wb.save(f"{file_directory}/{name}.xlsx")
        else:
            wb.save(f"{name}.xlsx")
