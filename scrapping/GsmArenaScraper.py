from Scraper import Scraper

import os, json


url = "https://www.gsmarena.com/"


class GsmArenaScraper(Scraper):
    def __init__(self, home_url):

        super().__init__(home_url)

    def __extract_feature_value(self, feature_row, feture_name):

        for tr in feature_row.find_all("tr"):

            if tr.td.a.text.lower() == feture_name:

                value = tr.find_all("td")[1].text

                return value

    def __extract_mobile_features(self, features_table):

        feature_dic = {}

        for feature in features_table:

            head = feature.tbody.tr

            if head.th.text.lower() == "misc":

                feature_dic["price"] = self.__extract_feature_value(
                    feature.tbody, "price"
                )

            if head.th.text.lower() == "launch":

                feature_dic["announcment_year"] = self.__extract_feature_value(
                    feature.tbody, "announced"
                ).split(",")[0]

            if head.th.text.lower() == "memory":

                feature_dic["memory"] = self.__extract_feature_value(
                    feature.tbody, "internal"
                )

            if head.th.text.lower() == "display":

                feature_dic["display_size"] = self.__extract_feature_value(
                    feature.tbody, "size"
                ).split(",")[0]

            if head.th.text.lower() == "platform":

                feature_dic["os"] = self.__extract_feature_value(
                    feature.tbody, "os"
                ).split(",")[0]
        return feature_dic

    def __get_mobile_object(self, brand, mobile_item):

        mobile_name = mobile_item.a.strong.span.text

        item_href = mobile_item.a["href"]

        mobile_page = self.bs_object_from_url(self.home_url + item_href)

        features_table = mobile_page.find("div", {"id": "specs-list"}).find_all("table")

        features = self.__extract_mobile_features(features_table)

        mobile_object = {"brand": brand, "name": mobile_name, **features}

        return mobile_object

    def __extract_mobiles_item(self, brand):

        hrefs = []

        mobiles = []

        first_brand_page_href = brand.a["href"]

        hrefs.append(first_brand_page_href)

        home_brand_page = self.bs_object_from_url(self.home_url + first_brand_page_href)

        nav_pages = (
            home_brand_page.find("div", class_="main")
            .find("div", class_="review-nav")
            .find("div", class_="nav-pages")
        )

        if nav_pages:

            all_brand_pages = nav_pages.find_all("a")

            for a in all_brand_pages:

                hrefs.append(a["href"])

        for href in hrefs:

            brand_page = self.bs_object_from_url(self.home_url + href)

            makers_list = brand_page.find("div", class_="makers").ul
            mobiles.extend(makers_list.find_all("li"))
        return mobiles

    def __get_all_brands(self, brand_table):

        brands = []

        for row in brand_table:

            brand_row = row.find_all("td")

            for brand in brand_row:
                brands.append(brand)
        return brands

    def __get_last_mobile_index(self, path):

        with open(path, "r") as recovory_file:

            obj = json.load(recovory_file)

        return obj["brand"], obj["mobile"]

    def __save_last_mobile_index(self, path, brand_ix, mobile_ix):

        with open(path, "w") as file:

            dic = {"brand": brand_ix, "mobile": mobile_ix}

            json.dump(dic, file)

    def start_scraping(self):

        mobile_objects = []

        try:

            current_brand_index, current_mobile_index = self.__get_last_mobile_index(
                f"{os.path.dirname(__file__)}/recovery.json"
            )

            print("start")

            brands_page = self.bs_object_from_url(f"{self.home_url}makers.php3")

            all_brand = brands_page.find("div", class_="st-text")

            brand_table = all_brand.table.tbody.find_all("tr")

            brands = self.__get_all_brands(brand_table)

            for brand in brands[current_brand_index:]:

                brand_name = brand.a.contents[0]

                mobiles = self.__extract_mobiles_item(brand)

                print(brand_name, " has ", len(mobiles), "mobiles")

                for mobil in mobiles[current_mobile_index:]:

                    mobile_object = self.__get_mobile_object(brand_name, mobil)

                    print("get one")

                    mobile_objects.append(mobile_object)

                    current_mobile_index += 1

                current_brand_index += 1

                current_mobile_index = 0

        # except ConnectionError as ex:

        #     print(ex)

        except AttributeError as ex:

            print(ex)

            self.__save_last_mobile_index(
                f"{os.path.dirname(__file__)}/recovery.json",
                current_brand_index,
                current_mobile_index,
            )

        finally:

            return mobile_objects
