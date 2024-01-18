from urllib.parse import urlsplit
from bs4 import BeautifulSoup
# For regular expressions
import re
# HTTP
import requests
# Handling punctuation
import string
# Rate Liminting
import time
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
# FIXME: dont import unnecessary modules
from Content import Content

class Crawler:
    """
    Contains a list which maintains a reference to the visited websites.
    """
    def __init__(self, root):
        self.root = root
        self.base_url, self.path = self.splitURL()
        self.visited = []

    def __iter__(self):
        for website in self.visited:
            yield website.getUrl()

    def splitURL(self):
        """
        Splits the root Wikipedia url into its base_url and path
        """
        components = urlsplit(self.root)
        base_url = f"{components.scheme}://{components.netloc}"
        # TODO: raise warning if base url is not Wiki
        path = f"{components.path}"
        return base_url, path

    def getHTML(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def getContent(self, url, depth, width):
        """
        Extracts the content from BeautifulSoup object and stores it as an instance of the Website class, returns the
        reference to this instance.
        """
        print(f"in getContent for: {url}")
        bs = self.getHTML(url)
        # Invalid url content.
        if bs is None:
            print(f"The url {url} has no HTML content")
            return None
        # Create object in Content class.
        webpage = Content(url)
        if webpage.getUrl() in self.visited:
            print(f"already visited {url} before")
            return None
        # --------------------------------------------------
        # Remove hidden elements from Body Content
        body_content = bs.find('div', {'id': 'bodyContent'})
        for element in body_content.find_all(True, {'style': True}):
            if 'display:none' in element['style']:
                element.decompose()
        for element in body_content.find_all('code'):
            element.decompose()
        hidden_cat = body_content.find('div', {'id': 'mw-hidden-catlinks'})
        if hidden_cat is not None:
            hidden_cat.decompose()
        printfooter = body_content.find('div', {'class': 'printfooter'})
        if printfooter is not None:
            printfooter.decompose()
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
        clean_text_list, removed_text = self.cleanText(raw_text, return_removed=True)
        # --------------------------------------------------
        # Create object in Content class.
        # TODO: make sure these are in correct order
        webpage.storeText(clean_text_list)
        webpage.storeRemovedText(removed_text)
        webpage.storeLinks(article_links)
        self.visited.append(webpage.getUrl())
        return webpage

    def cleanText(self, raw_text, return_removed=False):
        removed_text = False
        # TODO maybe include . in middle of a word for abbreviations
        is_word_re = re.compile(r'^[\'\"(]?[a-zA-Z]+[a-zA-Z-\'.]*[a-zA-Z]+[\',!\")?:;.]*$|^[a-zA-Z]$')
        # horizontal bar, figure dash, em dash, en dash
        translation_table = str.maketrans('―‒—–’/', "----\' ")
        raw_text = raw_text.translate(translation_table)
        raw_text_list = raw_text.split()
        if return_removed is True:
            removed_text = [text for text in raw_text.split() if not is_word_re.match(text)]
        clean_text_list = [text for text in raw_text.split() if is_word_re.match(text)]
        return clean_text_list, removed_text

    def parse(self, url=None, depth=None, width=None, extract_excel=False, file_directory=None):
        """
        """
        # TODO maybe add a method of returning them in order of rank?
        frequency_list = {}
        if url is None:
            url = self.root
        for webpage_content in self.breadthFirstSearch(url, depth, width):
            frequency_list = self.createFrequncyList(webpage_content, frequency_list)
        # --------------------------------------------------
        # Extract to Excel
        if extract_excel is True:
            file_name = input("What would you like to name your Excel file? ")
            self.createExcel(file_name, file_directory, frequency_list)
        # --------------------------------------------------
        else:
            for word, frequency in frequency_list.items():
                print(f"{word} : {frequency}")
        return "DONE!"

    def breadthFirstSearch(self, url, depth=None, width=None):
        """
        """
        queue = [url]
        curr_depth = 0
        curr_width = 0
        while queue:
            curr_url = queue.pop(0)
            time.sleep(1)
            webpage = self.getContent(curr_url, curr_depth, curr_width)
            if webpage is not None:
                yield webpage
                if depth is None or curr_depth <= depth:
                    for link in webpage.getLinks():
                        if width is None or curr_width < width:
                            queue.append(link)
                            curr_width += 1
                    curr_depth += 1
                    curr_width = 0

    def createFrequncyList(self, webpage, frequency_list):
        """
        {word : frequency}
        :param webpage:
        :param frequency_list:
        :return:
        """
        text = webpage.getText()
        for word in text:
            clean_word = word.strip(string.punctuation)
            if len(clean_word) > 1 or (clean_word.lower() == "a" or clean_word.lower() == "i"):
                if clean_word.lower() in frequency_list:
                    frequency_list[clean_word.lower()] += 1
                else:
                    frequency_list[clean_word.lower()] = 1
        return frequency_list

    def createExcel(self, name, file_directory, frequency_list):
        wb = Workbook()
        ws = wb.active
        ws.append(["Word", "Frequency"])
        for word, frequency in frequency_list.items():
            ws.append([word, frequency])
        table = Table(displayName="Freqeuncy_List", ref=f"A1:B{len(frequency_list)+1}")
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