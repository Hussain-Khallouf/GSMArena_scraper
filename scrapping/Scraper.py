from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, home_url):
        self.home_url = home_url
        page_file = requests.get(home_url).text
        self.home_bs = BeautifulSoup(page_file, "html5lib")

    def bs_object_from_url(self, url):
        page_file = requests.get(url).text
        page = BeautifulSoup(page_file, "html5lib")
        return page

    def start_scraping(self):
        pass
