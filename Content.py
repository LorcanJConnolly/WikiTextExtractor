class Content:
    """
    Creates a reference object for storage and retrival a Wikipedia article's visible attributes.
    A reference object for a Wikipedia article is identified by its url attribute.
    """
    def __init__(self, url):
        self.url = url
        self.text = None
        self.frequency_list = None
        self.article_links = None
        self.removed_text = None

    def __eq__(self, other):
        """Two Wikipedia articles (objects) are the same when their urls are the same."""
        return other.url is self.url

    def __ne__(self, other):
        return not (self == other)

    def get_url(self):
        return self.url

    def get_text(self):
        return self.text

    def get_removed_text(self):
        return self.removed_text

    def get_links(self):
        return self.article_links

    # Mutators _____________________
    def store_text(self, text):
        """
        Stores a list containing the extracted visible words from the Wikipedia article.
        """
        self.text = text

    def store_removed_text(self, removed_text):
        """
        Primarily for testing purposes.
        Stores a list containing the non-extracted (non-words) visible text from the Wikipedia article.
        """
        self.removed_text = removed_text

    def store_links(self, article_links):
        """
        Stores a list of the artile links displayed on the Wikipedia article.
        """
        self.article_links = article_links

    def store_frequency_list(self, frequency_list):
        """
        Stores the Wikipedia article's frequency list: a dictionary in the format {word : frequency}.
        """
        self.frequency_list = frequency_list


# TODO note for testing -  all of these may be returned as NONE
