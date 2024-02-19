from Wiki_Crawler import Crawler
from urllib.parse import urlsplit
from openpyxl import Workbook
from openpyxl.worksheet.table import Table


def get_user_root():
    while True:
        user_root = str(input("Enter the root Wikipedia URL:")).strip()
        print(user_root)
        if user_root and Crawler.is_wiki_url(user_root) and good_bot(user_root):
            return user_root
        else:
            print("\nThis not a valid Wikipedia URL.\n")


def good_bot(url):
    """is_wiki_url is True"""
    components = urlsplit(url)
    path = components.path
    # if path is not in Wiki_robots_txt
    # TODO - implement a check to see if user URL is not in the wikirobots.txt
    return True


def get_user_journey():
    """
    Need to document rules:
    depth = 0 means only scrape from the root.
    width = 0 means only scrape from the first link on each page for the given depth.
    Note: this is seen in the different if conditions in line 154 and 158 of Wiki_Crawler.
    """
    user_depth = get_positive_int("Enter the crawler's depth:")
    if user_depth == 0:
        return user_depth, 0
    user_width = get_positive_int("Enter the crawler's width:")
    if user_depth * user_width < 1000:
        return user_depth, user_width
    else:
        print("\nERROR: The dimensions you have inputted construct too large of a path!\n"
              "This crawler is designed to construct small to medium datasets.\n"
              "Please enter smaller values.\n")
        return get_user_journey()


def get_positive_int(prompt_message):
    while True:
        user_input = input(prompt_message)
        try:
            user_int = int(user_input)
            if user_int < 0:
                raise ValueError
            return user_int
        except ValueError:
            print("\nPlease enter a valid non-negative integer value.\n")


def get_user_output():
    while True:
        user_input = input("How would you like to return your created Frequency List: EXCEL/CSV? ")
        if user_input.lower() == "csv" or user_input.lower() == "excel":
            return user_input.lower()
        else:
            print(f"Your input is invalid. Please choose one of the following options: CSV/EXCEL")
            continue


def create_excel(fl, rt=None):
    """
       Creates an Excel workbook which displays the gathered data and creates a log(Rank) vs log(Frequency) plot to
        analyse Zipf's Law in the data.
       """
    wb = Workbook()
    ws1 = wb.active
    ws1.append(["Rank", "Word", "Frequency"])
    rank = 0
    last_frequency = None
    for word, frequency in fl:
        if frequency != last_frequency:
            rank += 1
        ws1.append([rank, word, frequency])
        last_frequency = frequency
    table = Table(displayName="Frequency_List", ref=f"A1:C{len(fl) + 1}")
    ws1.add_table(table)
    desktop_path = r"C:\Users\lconn\Desktop"
    wb.save(f"{desktop_path}\\Test_output.xlsx")
    print(f"Your file is saved under the name in the directory")


def create_csv(fl):
    pass
# ---------------------------------------------------------------------------------------------------------------------


def main():
    user_root = get_user_root()
    user_depth, user_width = get_user_journey()

    crawler = Crawler(root=user_root)
    fl, rt = crawler.parse(url=user_root, depth=user_depth, width=user_width)
    if rt:
        print("--- Printing Removed Text ---")
        for lst in rt:
            print(lst)
    if fl:
        user_output = get_user_output()
        if user_output == "csv":
            create_csv(fl)
        elif user_output == "excel":
            create_excel(fl)
    else:
        return f"The chosen root {user_root} returned nothing to output."


if __name__ == "__main__":
    main()
