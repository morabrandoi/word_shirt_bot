from bs4 import BeautifulSoup as soup
import requests

DICTIONARY_URL = "https://www.dictionary.com/browse/"
PHONETIC_CLASS = "css-uis96j e1rg2mtf2"
HEADER_CLASS1 = "luna-pos"  # I believe pos stands for part of speach
HEADER_CLASS2 = "pos"
SECTION_CLASS = "css-171jvig e1hk9ate0"
DEFINITION_MASTER_CLASS = "one-click-content css-1e3ziqc e1q3nk1v4"
DEFINITION_WORDS_CLASS = "one-click"
EXAMPLE_CLASS = "luna-example italic"


# takes in a string, word,
# returns the web page in a soup object
def get_word_page(word):
    vocab_html = soup(requests.get(DICTIONARY_URL + word).content, "lxml")
    return vocab_html


# takes in soup object
# returns 2D list of definition segments
def parse_dictionary_entries(page_soup):
    master = []
    all_sections = page_soup.find_all("section", class_=SECTION_CLASS)
    for section in all_sections:
        section_list = []
        # gets the header e.g noun or verb or verb (used with object)
        header = section.find("span", class_=HEADER_CLASS1)

        # check if maybe it is the other kind of header
        if header is None:
            header = section.find("span", class_=HEADER_CLASS2)


        # add that header to the section list
        section_list.append(header.get_text())

        all_def_in_sec = section.find_all("span", class_=DEFINITION_MASTER_CLASS)
        # iterate through all super definition spans in section
        for definition in all_def_in_sec:
            if definition.find("span", class_=EXAMPLE_CLASS) is not None:


                # Need to remove the example span from the definition text

                pass






            print(definition.get_text())
            break
        break


# takes in a string, word
# returns a dictionary of contents like {phonics: "ahhpull, word: "apple", first_seg: [header, item, item]}
def parse_word_page(word):
    # bringing in web page as soup object
    page_soup = get_word_page(word)
    # initializiing dictionary output
    res = dict()
    # assigning the phonetic spelling based on the first instance of text with that css class
    res["phonics"] = page_soup.find("span", class_=PHONETIC_CLASS).get_text()

    parse_dictionary_entries(page_soup)

parse_word_page("ball")
