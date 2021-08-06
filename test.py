import requests
from bs4 import BeautifulSoup
import json

categories2 = []
categories3 = []
URL = "https://www.ikea.com/in/en/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(name="nav")
cat0_elements = results.find_all("li")
categories0 = []
categories1 = []
categories2 = []
for cat0_element in cat0_elements:
    categories0.append({"name": cat0_element.find("a", class_="hnf-link").text.strip(),
                        "url": cat0_element.find("a", {"class": "hnf-link"}).attrs['href']})

for cat1_element in categories0:
    page1 = requests.get("https://www.ikea.com/in/en/cat/products-products/")
    soup1 = BeautifulSoup(page1.content, "html.parser")
    ul_main_cat = soup1.find(class_="vn-nav vn-p-grid vn-accordion")
    ul_main_cat_list = ul_main_cat.find_all("div", class_="vn-p-grid-gap vn-accordion__item")
    for cat2_element in ul_main_cat_list:
        sub_categories = []
        sub_cat = cat2_element.find(class_="vn-list--plain vn-list vn-accordion__content")
        sub_cat_list = sub_cat.find_all("li")
        for sub_cat_element in sub_cat_list:
            sub_categories.append({"name": sub_cat_element.find("a", class_="vn-link vn-nav__link").text.strip(),
                                   "url": sub_cat_element.find("a", {"class": "vn-link vn-nav__link"})
                                  .attrs['href']})

        categories1.append({"name": cat2_element.find("span", class_="vn-accordion__title h4").text.strip(),
                            "url": cat2_element.find("a", {"class": "vn-link vn-nav__link vn-accordion__image"})
                           .attrs['href'], "children": sub_categories})

    break
jsonStr = json.dumps({"name": "products", "url": "", "children": categories1})
jsonFile = open("data.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()
