class Content:
    """
    Creates a reference to the attributes of a website, which is identified by its url.
    Users do not access this class so make it nonpublic.
        This ensures that _text and _article_links remain as lists
    """
    def __init__(self, url):
        self._url = url
        self._text = None
        self._frequency_list = None
        self._article_links = None
        # For Testing Purposes
        self._removed_text = None

    # two websites (or objects) are the same when their urls are the same
    def __eq__(self, other):
        return other._url is self._url

    def __ne__(self, other):
        return not (self == other)

    def getUrl(self):
        return self._url

    def getText(self):
        return self._text

    def getRemovedText(self):
        return self._removed_text

    def getLinks(self):
        return self._article_links

    def getLink(self, index):
        if index > len(self._article_links):
            raise IndexError(f"No Article at index {index}")
        return self._article_links[index]

    # Mutators _____________________
    def storeText(self, text):
        """
        Stores a list of the extracted text from the webpage that is used in the frequency list.
        """
        if text:
            self._text = text

    def storeRemovedText(self, removed_text):
        if removed_text:
            self._removed_text = removed_text

    def storeFrequencyList(self, frequency_list):
        """
        Stores a dict of {word : frequency} in the self.frequency_list attribute of the webpage's Content object.
        """
        # Can be None
        if isinstance(frequency_list, dict):
            self._frequency_list = frequency_list
        else:
            raise AttributeError(f"{frequency_list} is not a dictionary!")

    def storeLinks(self, article_links):
        """
        Stores a list of article links in the self._article_links attribute of the webpage's Content object.
        """
        # Can be none
        if isinstance(article_links, list):
            self._article_links = article_links
        else:
            raise AttributeError(f"{article_links} is not a list!")