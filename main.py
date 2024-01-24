from Wiki_Crawler import Crawler
from Content import Content

from urllib.parse import urlsplit


def get_user_root():
    while True:
        user_root = str(input("Enter the root Wikipedia URL:")).strip()
        print(user_root)
        if user_root and is_wiki_url(user_root):
            return user_root
        else:
            print("\nThis not a valid Wikipedia URL.\n")


def is_wiki_url(url):
    try:
        components = urlsplit(url)
    except TypeError:
        return False
    netloc, path = components.netloc, components.path
    if netloc == "en.wikipedia.org" or netloc == "simple.wikipedia.org" and good_bot(path):
        return True
    else:
        return False


def good_bot(path):
    return True


def get_user_journey():
    """
    Need to document rules:
    depth = 0 means only scrape from the root.
    width = 0 means only scrape from the first link on each page for the given depth.
    Note: this is seen in the different if conditions in line 154 and 158 of Wiki_Crawler.
    """
    while True:
        # FIXME: if depth is 0 (only do the root url), width will also be 0.
        user_depth = input("Enter the crawler's depth:")
        # FIXME: Width can be None!
        user_width = input("Enter the crawler's width:")
        try:
            user_depth = int(user_depth)
            user_width = int(user_width)
            if user_depth < 0 or user_width < 0:
                raise ValueError
            if user_depth * user_width < 1000:
                return user_depth, user_width
            else:
                print("\nERROR: The dimensions you have inputted construct too large of a path!\n"
                      "This crawler is designed to construct small to medium datasets.\n"
                      "Please enter smaller values.\n")
                continue
        except ValueError:
            print("\nPlease enter valid non-negative integer values.\n")
            continue
# ---------------------------------------------------------------------------------------------------------------------


def main():
    user_root = get_user_root()
    user_depth, user_width = get_user_journey()
    print(user_root, user_width, user_depth)
    # crawler = Crawler(root=user_root)
    # crawler.parse(url=user_root, depth=user_depth, width=user_width, extract_excel=False, file_directory=None)


if __name__ == "__main__":
    main()
