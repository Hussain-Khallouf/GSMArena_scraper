import sqlite3
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from GsmArenaScraper import GsmArenaScraper
from orm.PhoneOrm import PhoneOrm


url = "https://www.gsmarena.com/"


def scrap_and_save(orm):
    orm.create_table()
    scrapper = GsmArenaScraper(url)
    mobiles = scrapper.start_scraping()
    for mobile in mobiles:
        orm.insert(mobile)


def get_mobile_from_db(orm):
    for row in orm.select():
        print(row, end="\n\n")


if __name__ == "__main__":
    connection = sqlite3.connect("phony.db")
    orm = PhoneOrm(connection)
    get_mobile_from_db(orm)