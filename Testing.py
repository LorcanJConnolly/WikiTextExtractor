import unittest
from unittest.mock import patch
from main import get_user_root, get_user_journey, is_wiki_url, good_bot
from Wiki_Crawler import Crawler
"""
To do:
- downed url
- general inputs
    - root
        - wiki
        - not page not found
        - not down
    - any url
- robots.txt disallowed sites
- UI controls


- get_content is where the errors can occur.

- breath width traversal
    - if we somehow reach dead end articles (e.g. https://en.wikipedia.org/wiki/Andr%C3%A9_M._Levesque) before the
      requested user_depth has been satisfied, the crawler will just stop and return only what was possible to scrape.

User inputs

The will of the machine
    - wiki url that does not have a page
    - wiki article that is down (should be handled)
    - dead-end wiki article (should be handled)

    - creating a webpage object for the article
        - text is none
        - articles are none
        - (attributes are returned as None)
        - test when urls are equal and not equal

Later-Later
    - Excel naming
    - Excel returning
"""


class TestMain(unittest.TestCase):
    # When the input is called, input return_value instead of waiting.
    #
    @patch('builtins.input', return_value=r"https://en.wikipedia.org/wiki/Main_Page")
    def test_valid_user_root(self, mock_input):
        self.assertEqual(get_user_root(), r"https://en.wikipedia.org/wiki/Main_Page")

    @patch('builtins.input', side_effect=["", "https://www.wikihow.com/Main-Page", 7, False])
    def test_invalid_user_root(self, mock_input):
        expected_output = [
            "\nThis not a valid Wikipedia URL.\n",
            "\nThis not a valid Wikipedia URL.\n",
            "\nThis not a valid Wikipedia URL.\n",
            "\nThis not a valid Wikipedia URL.\n"
        ]
        for message in expected_output:
            with self.subTest(message=message):
                self.assertIn(message, "\nThis not a valid Wikipedia URL.\n")

    def test_is_not_wiki_url(self):
        invalid_urls = ["", "https://www.wikihow.com/Main-Page"]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_wiki_url(url))

    def test_is_wiki_url(self):
        valid_urls = [r"https://en.wikipedia.org/wiki/Main_Page"]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_wiki_url(url))


if __name__ == '__main__':
    unittest.main()
