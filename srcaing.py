
from bs4 import BeautifulSoup
import requests
import time
import json

base_url = 'https://www.gsmarena.com/'

def soup_page_object(url):
    page_file = requests.get(url).text
    page = BeautifulSoup(page_file, 'html5lib')
    return page


def extract_feature_value(feature_row,feture_name):
    for tr in feature_row.find_all('tr') :
        if tr.td.a.text.lower() == feture_name:
            value = tr.find_all('td')[1].text
            return value

def extract_mobile_features(features_table):
    feature_dic ={}
    for feature in features_table:
                head = feature.tbody.tr
                if head.th.text.lower() == 'misc':
                    feature_dic['price']= extract_feature_value(feature.tbody,'price')
                if head.th.text.lower() == 'launch':
                    feature_dic['announcment']= extract_feature_value(feature.tbody,'announced')
                if head.th.text.lower() == 'memory':
                    feature_dic['memory']= extract_feature_value(feature.tbody,'internal')  
                if head.th.text.lower() == 'display':
                    feature_dic['display_size']= extract_feature_value(feature.tbody,'size').split(',')[0]
                if head.th.text.lower() == 'platform':
                    feature_dic['os']= extract_feature_value(feature.tbody,'os').split(',')[0]     
    return feature_dic


def get_mobile_object(mobile_item):
    mobile_name = mobile_item.a.strong.span.text
    item_href = mobile.a['href']
    mobile_page = soup_page_object(base_url+item_href)
    features_table = mobile_page.find('div',{"id": "specs-list"}).find_all('table')
    features = extract_mobile_features(features_table)
    mobile_object = {'mobile_name':mobile_name,**features}
    return mobile_object

def extract_mobiles_item(brand_page):
    href = brand.a['href']
    brand_page_file = requests.get(base_url+href).text
    brand_page = BeautifulSoup(brand_page_file, 'html5lib')
    makers_list = brand_page.find('div',class_='makers').ul
    mobiles = makers_list.find_all('li')
    return mobiles


def get_all_brands(brand_table):
    brands = []
    for row in brand_table:
        brand_row = row.find_all('td')
        for brand in brand_row:
            brands.append(brand)
    return brands


def get_last_mobile_index(path):
    with open(path,'r') as recovory_file:
        obj = json.load(recovory_file)
    return obj['brand'],obj['mobile']


def save_last_mobile_index(path,brand_ix,mobile_ix):
    with open(path,'w') as file:
        dic = {"brand": brand_ix, "mobile": mobile_ix}
        json.dump(dic,file)
        

if __name__ == "__main__":
    current_brand_index,current_mobile_index = get_last_mobile_index('recovery.json' )
    try:
        brands_page = soup_page_object('https://www.gsmarena.com/makers.php3')
        all_brand = brands_page.find('div', class_='st-text')
        brand_table = all_brand.table.tbody.find_all('tr')
        brands = get_all_brands(brand_table)

        for brand in brands[current_brand_index:]:
            brand_name = brand.a.contents[0]
            mobiles = extract_mobiles_item(brand)
            print(brand_name,' has ',len(mobiles),'mobiles')

            for mobile in mobiles[current_mobile_index:]:
                mobile_object = get_mobile_object(mobile)
                print(mobile_object)
                current_mobile_index+=1
            current_brand_index+=1
            current_mobile_index=0

    except Exception as ex:
        print(ex)
        save_last_mobile_index('recovery.json',current_brand_index,current_mobile_index)
