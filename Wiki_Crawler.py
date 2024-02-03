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
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
# FIXME: dont import unnecessary modules
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
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            print(f"REQUEST ERROR: status code {requests.get(url)}")
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def get_content(self, url):
        """
        Extracts the content from BeautifulSoup object and stores it as an instance of the Content class.
        Returns the created instance of the Content class.
        """
        print(f"in getContent for: {url}")
        # FIXME: check if wiki link here
        bs = self.get_html(url)
        if bs is None:
            print(f"The url {url} has no HTML content")
            return None
        # FIXME check the url BEFORE creating an object --> less memory allocation
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
        hidden_cat = body_content.find('div', {'id': 'mw-hidden-catlinks'})
        # FIXME: some hidden categories are shown sometimes.
        # hidden: class="mw-hidden-catlinks mw-hidden-cats-hidden">
        # shown: class="mw-hidden-catlinks mw-hidden-cats-ns-shown">
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
        # TODO maybe include . in middle of a word for abbreviations
        is_word_re = re.compile(r'^[\'\"(]?[a-zA-Z]+[a-zA-Z-\'.]*[a-zA-Z]+[\',!\")?:;.]*$|^[a-zA-Z]$')
        # Horizontal bar, figure dash, em dash, en dash translation.
        translation_table = str.maketrans('―‒—–’/', "----\' ")
        raw_text = raw_text.translate(translation_table)
        if return_removed is True:
            removed_text = [text for text in raw_text.split() if not is_word_re.match(text)]
        clean_text_list = [text for text in raw_text.split() if is_word_re.match(text)]
        return clean_text_list, removed_text

    def parse(self, url=None, depth=None, width=None, extract_excel=False, file_directory=None):
        """
        It's a method that creates a visible iterator using that paradigm.
        """
        # TODO maybe add a method of returning them in order of rank?
        # FIXME create the frequency list as the crawler crawls.
        frequency_list = {}
        for webpage in self.breadth_first_traversal(url, depth, width):
            frequency_list = self.create_frequency_list(webpage, frequency_list)
        # --------------------------------------------------
        # Extract to Excel
        if extract_excel is True:
            file_name = input("What would you like to name your Excel file? ")
            self.create_excel(file_name, file_directory, frequency_list)
        # --------------------------------------------------
        # Printing the Frequency List
        else:
            for word, frequency in frequency_list.items():
                print(f"{word} : {frequency}")
        return "DONE!"

    def breadth_first_traversal(self, url, depth, width=None):
        """
        Preforms a breath first traversal of the article links displayed on a Wikipedia article.
        """
        queue = [url]
        curr_depth, curr_width = 0, 0
        while queue:
            curr_url = queue.pop(0)
            time.sleep(1)
            webpage = self.get_content(curr_url)  # creates a webpage object from the url
            if webpage is not None:
                yield webpage
                if curr_depth < depth:
                    for link in webpage.get_links():
                        # TODO may return None
                        # TODO if it does, this for loop above will not be entered
                        if width is None or curr_width <= width:
                            queue.append(link)
                            curr_width += 1
                    curr_depth += 1
                    curr_width = 0
            else:
                # raise error - url returned none from get content
                pass

    @staticmethod
    def create_frequency_list(webpage, frequency_list):
        """
        Creates and returns the frequency list of the entire dataset gathered by the WikiCrawler.
        """
        text = webpage.get_text()
        for word in text:
            clean_word = word.strip(string.punctuation)
            if len(clean_word) > 1 or (clean_word.lower() == "a" or clean_word.lower() == "i"):
                if clean_word.lower() in frequency_list:
                    frequency_list[clean_word.lower()] += 1
                else:
                    frequency_list[clean_word.lower()] = 1
        return frequency_list

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
