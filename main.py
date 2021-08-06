import requests
from bs4 import BeautifulSoup
import json

product_categories = []
products = []
URL = "https://www.ikea.com/us/en/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(name="nav")
cat0_elements = results.find_all("li")
categories0 = []
categories1 = []

for cat0_element in cat0_elements:
    categories0.append({"name": cat0_element.find("a", class_="hnf-link").text.strip(),
                        "url": cat0_element.find("a", {"class": "hnf-link"}).attrs['href']})

for cat1_element in categories0:
    page1 = requests.get("https://www.ikea.com/us/en/cat/products-products/")
    soup1 = BeautifulSoup(page1.content, "html.parser")
    ul_main_cat = soup1.find(class_="vn-nav vn-p-grid vn-accordion")
    ul_main_cat_list = ul_main_cat.find_all("div", class_="vn-p-grid-gap vn-accordion__item")
    for cat2_element in ul_main_cat_list:
        sub_categories = []
        sub_cat = cat2_element.find(class_="vn-list--plain vn-list vn-accordion__content")
        sub_cat_list = sub_cat.find_all("li")
        for sub_cat_element in sub_cat_list:
            product_categories.append({"name": sub_cat_element.find("a", class_="vn-link vn-nav__link").text.strip(),
                                       "url": sub_cat_element.find("a", {"class": "vn-link vn-nav__link"})
                                      .attrs['href']})
            sub_categories.append({"name": sub_cat_element.find("a", class_="vn-link vn-nav__link").text.strip(),
                                   "url": sub_cat_element.find("a", {"class": "vn-link vn-nav__link"})
                                  .attrs['href']})

        categories1.append({"name": cat2_element.find("span", class_="vn-accordion__title h4").text.strip(),
                            "url": cat2_element.find("a", {"class": "vn-link vn-nav__link vn-accordion__image"})
                           .attrs['href'], "children": sub_categories})

    break

jsonStr = json.dumps({"name": "products", "url": "https://www.ikea.com/us/en/cat/products-products/",
                      "children": categories1})
jsonFile = open("categories.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()

for product_element in product_categories:

    if product_element["name"] != "Shop all":
        page2 = requests.get(product_element["url"])
        soup2 = BeautifulSoup(page2.content, "html.parser")
        product_data = soup2.find(class_="plp-product-list__products")
        product_data_list = product_data.find_all("div", class_="range-revamp-product-compact")
        for product_data_element in product_data_list:
            page3 = requests.get(product_data_element.find("a").attrs['href'])
            soup3 = BeautifulSoup(page3.content, "html.parser")
            description_section = soup3.find(class_="range-revamp-product__left-bottom range-revamp-product__grid-gap")
            description_area = description_section.find(class_="range-revamp-product-summary")
            description = description_area.find("p", {"class": "range-revamp-product-summary__description"})
            if description != None:
                description_value = description.text
            image_grid = soup3.find(class_="range-revamp-media-grid__grid")
            image_grid_items = image_grid.find_all(class_="range-revamp-media-grid__media-container")
            image_list = []
            for image_item in image_grid_items:
                image_list.append(product_data_element.find("img").attrs['src'])
            products.append({"name": product_data_element["data-product-name"], "category": product_element["name"],
                             "price": product_data_element["data-price"],
                             "currency": product_data_element["data-currency"],
                             "productType": product_data_element["data-product-type"],
                             "url": product_data_element.find("a").attrs['href'],
                             "description": description_value,
                             "sku": product_data_element["data-product-number"],
                             "images": image_list})

productStr = json.dumps(products)
jsonFile = open("products.json", "w")
jsonFile.write(productStr)
jsonFile.close()
