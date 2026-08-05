from bs4 import BeautifulSoup


def create_soup(html):

    return BeautifulSoup(html, "lxml")