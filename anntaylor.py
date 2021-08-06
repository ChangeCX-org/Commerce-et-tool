import requests
from bs4 import BeautifulSoup
import json

product_categories = []
products = []
URL = "https://www.anntaylor.com/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(name="nav")
Top_elements = results.findAll("div", class_="sub-nav-wrapper")

cat0_elements = results.find_all("div", class_="sub-nav-wrapper")

categories0 = []
categories1 = []
products0 = []
for cat0_element in cat0_elements:
    categories0.append({"name": cat0_element.find("a").text.strip(),
                        "url": cat0_element.find("a").attrs['href']})
    product_categories.append({"name": cat0_element.find("a").text.strip(),
                        "url": cat0_element.find("a").attrs['href']})

for cat1_element in categories0:
    page1 = requests.get(cat1_element.get("url"))
    soup1 = BeautifulSoup(page1.content, "html.parser")
    left_menu = soup1.find("div", class_="categories component")
    try:
            left1_menu = left_menu.find("nav")
            subleft_menu = left1_menu.find_all("a")
            for subleft1_menu in subleft_menu:
                product_categories.append({"name": subleft1_menu.text,
                        "url": subleft1_menu.get('href')})
                #print(product_categories)
                productpage = requests.get(subleft1_menu.get('href'))
                productsoup = BeautifulSoup(productpage.content, "html.parser")
                wproducts = productsoup.find_all("ul")
                for product in wproducts:
                    products01 = product.find_all("a")
                    for product1 in products01:
                        productname = product1.find("strong")
                        producturl = product1.get('href')
                        #product details get
                        productdetailpage = requests.get(product1.get('href'))
                        productdetailsoup = BeautifulSoup(productdetailpage.content, "html.parser")
                        detailproducts = productdetailsoup.find("div", "product-details component")
                        productprice=detailproducts.find("strong", class_="price")
                        #detailproducts1 = detailproducts.find_all("a")
                        detailproductssizetype = detailproducts.find_all("a", {"name": "sizeType"})
                        detailproductssize = detailproducts.find_all("fieldset", class_="sizes")
                        detailproductscolor = detailproducts.find_all("fieldset", class_="colors")
                        #print(detailproductssize)
                        producttypesize = []
                        productsize = []
                        productcolor=[]
                        #selectsizeonly = detailproductssize.find_all("a", {"name": "size"})
                        #print(selectsizeonly)
                        for pts in detailproductssizetype:
                            #print(pts.text)
                            producttypesize.append({pts.text})
                        for a in detailproductssize:
                            for sizea in a.find_all("a", {"name": "size"}):
                                #print(sizea.text)
                                #print("End")
                                productsize.append({sizea.text})
                                #allcolor = detailproductscolor.find_all("a")
                                #print(detailproductscolor)
                                for a in detailproductscolor:
                                    print(a.find_all("a"))
                                    print("1")

                                for pc in a.find_all("a"):
                                        print("2",pc.text)
                                        #print("2")
                                        productcolor.append({pc.text})
                        products.append({"name": detailproducts.find("h1").text, "price": detailproducts.find("strong", class_="price").text,
                                         "SizeType": producttypesize , "size": productsize , "color": productcolor })
                        #print(products)
                        #End Product details

    except:
        print("error")
    jsonStr = json.dumps({"name": "HomePageCategory", "url": "",
                              "children": product_categories})
    jsonFile = open("anntaylor-categories.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()
print("end categories string")
jsonStr = json.dumps({"name": "products", "url": "",
                                              "children": products})
jsonFile = open("anntaylor-products.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()
print("end product string")