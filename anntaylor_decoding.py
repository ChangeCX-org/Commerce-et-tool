import urllib

import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# AWS Start Here

import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse

# dotenv_path = Path(r'E:\PRASAD\Dasha\chocolate\.env')
# load_dotenv(dotenv_path=dotenv_path)

# load .env from project location
load_dotenv()

# Load from .env file
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_S3_ENDPOINT = os.getenv('AWS_S3_ENDPOINT')


# AWS Upload Image Function
def upload_file_to_aws_s3(url, imagecount, file_type='image'):
    file_url = ''
    # get the connection of AWS S3 Bucket
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    global sku_count
    isku = "A0E2000000021S" + str(sku_count)
    # print(imagecount,'imagecount')
    response = requests.get(url)
    if response.status_code == 200:
        raw_data = response.content
        url_parser = urlparse(url)
        # print(url_parser,'url_parser')
        file_name = os.path.basename(url_parser.path)
        # print(file_name, 'file_name')
        key = isku + "_" + str(imagecount) + ".png"
        # print(key, 'key')

        try:
            # Write the raw data as byte in new file_name in the server
            with open(file_name, 'wb') as new_file:
                new_file.write(raw_data)

            # Open the server file as read mode and upload in AWS S3 Bucket.
            data = open(file_name, 'rb')
            s3.Bucket(AWS_BUCKET_NAME).put_object(Key=key, Body=data)
            data.close()

            # Format the return URL of upload file in S3 Bucjet
            file_url = 'https://%s.%s/%s' % (AWS_BUCKET_NAME, AWS_S3_ENDPOINT, key)
        except Exception as e:
            print("Error in file upload %s." % (str(e)))

        finally:
            # Close and remove file from Server
            new_file.close()
            os.remove(file_name)
            print("Attachment Successfully save in S3 Bucket url %s " % (file_url))
    else:
        print("Cannot parse url")
    return file_url


# END AWS


product_categories = []
products = []
x = 0
p = 0
dollar_value = 74.47
sku_count = 0
baseId_count = 0
# imagesku_count = 0

# INITIATING THE PROCESS
URL = "https://www.anntaylor.com/"
page = requests.get(URL).text
soup = BeautifulSoup(page, "lxml")
results = soup.find(name="nav")

# Top_elements = results.findAll("div", class_="sub-nav-wrapper")

cat0_elements = results.find_all("div", class_="sub-nav-wrapper")

categories0 = []
categories1 = []
products0 = []
for cat0_element in cat0_elements:
    x = x + 1
    categories0.append({"name": cat0_element.find("a").text.strip(), "url": cat0_element.find("a").attrs['href']})
    product_categories.append({"key": "c" + str(x), "externalId": x, "name.de": cat0_element.find("a").text.strip(),
                               "slug.de": cat0_element.find("a").text.strip().lower(),
                               "name.en": cat0_element.find("a").text.strip(),
                               "slug.en": cat0_element.find("a").text.strip().lower(),
                               "name.it": cat0_element.find("a").text.strip(),
                               "slug.it": cat0_element.find("a").text.strip().lower(), "parentId": "",
                               "webImageUrl": "",
                               "iosImageUrl": ""})

# Product categories processed and stored as JSON file here...
jsonStr = json.dumps({"name": "Category", "url": "", "children": product_categories})
jsonFile = open("anntaylor-categories.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()
print("end categories string")


# product_loop starts here
def product_loop(subleft_menu):
    try:
        def get_images(producturl1):

            def render_page(url):
                # options = Options()
                # options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                # driver = webdriver.Chrome(r"C:\Users\Raghav\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
                driver = webdriver.Chrome(
                    r"C:\Users\ashok\AppData\Local\Programs\Python\Python310\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
                # driver = webdriver.Chrome(chrome_options=options, executable_path=r"E:\PRASAD\Dasha\chocolate\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
                # driver = webdriver.Chrome(chrome_options=options, executable_path=r"C:\Users\sulur\AppData\Local\Programs\Python\Python39\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
                driver.get(url)
                time.sleep(3)
                r = driver.page_source
                driver.quit()
                return r

            # product_images1 = []
            product_image = ""
            URL = producturl1
            render_content = render_page(URL)

            soup = BeautifulSoup(render_content, "html.parser")
            results = soup.find("main", class_='global-redirect')
            result1 = results.find("div", class_="product-details component")
            result2 = result1.find("div", class_="pagination-wrapper")
            result3 = result2.findAll("div", class_="pagination-slide")

            # icount = 1
            for result in result3:
                link_image = result.find('img').attrs["src"]
                if "?$" in link_image:
                    link_image = link_image.split("?")
                    # product_images1.append("https:"+link_image[0]+";")
                    product_image += "https:" + link_image[0] + ";"

                    # Save Image to local path
                    # filepath = "Product_Images/"
                    # filename = link_image[0].split("/")[-1]
                    # print(filename)
                    # urllib.request.urlretrieve("https:"+link_image[0], filepath + filename+".png")

                    ##Save to AWS
                    # upload_file_to_aws_s3("https:"+link_image[0], icount)
                else:
                    # product_images1.append(result.find('img').attrs["src"]+";")
                    product_image += result.find('img').attrs["src"] + ";"

                    # Save Image to local path
                    # filepath = "Product_Images/"
                    # filename = result.find('img').attrs["src"].split("/")[-1]
                    # print(filename)
                    # urllib.request.urlretrieve("https:"+result.find('img').attrs["src"], filepath + filename+".png")

                    ##Save to AWS
                    # upload_file_to_aws_s3(result.find('img').attrs["src"], icount)

                # icount += 1
            return product_image

        # for subleft1_menu in subleft_menu:
        # product_categories.append({"name": subleft1_menu.text,
        # "url": subleft1_menu.get('href')})
        productpage = requests.get(subleft_menu).text
        productsoup = BeautifulSoup(productpage, "lxml")
        wproducts = productsoup.find_all("div", class_="product-wrap")
        for wproducts_index, product in enumerate(wproducts):

            product01 = product.find("a")
            print(wproducts_index)
            # productname = product1.find("strong")
            producturl = product01.attrs['href']
            print(producturl)
            # product details get

            product_images = []
            product_images = get_images(producturl)
            product_images = product_images[:-1]
            print(product_images)
            productdetailpage = requests.get(producturl).text
            productdetailsoup = BeautifulSoup(productdetailpage, "lxml")
            category = productdetailsoup.find("div", class_="breadcrumb breadcrumb-plp component")
            category_list = category.findAll("span", itemprop="name")
            # print(category)
            category_breadcrumb = ""
            for category_list_item in category_list:
                if category_list_item == category_list[-2]:
                    category_breadcrumb += category_list_item.text
                elif category_list_item == category_list[0] or category_list_item == category_list[-1]:
                    continue
                else:
                    category_breadcrumb += category_list_item.text + ">"
            print(category_breadcrumb)

            # product thumbnail images

            detailproducts = productdetailsoup.find("div", class_="product-details component")
            product_name = detailproducts.find("h1").text  # Product name
            print(product_name)

            productprice_raw_text = detailproducts.find("strong", class_="price").text

            if "INR" in productprice_raw_text:
                product_price_split = productprice_raw_text.split()  # price spliting
                product_price_value = int(float(product_price_split[1])) // dollar_value  # price converting to dollars
                productprice = "USD " + str(int(product_price_value))  # Product Price
            else:
                productprice = productprice_raw_text.replace("$", "USD ")

            print(productprice)
            # detailproducts1 = detailproducts.find_all("a")
            detailproductssizetype = detailproducts.find_all("a", {"name": "sizeType"})
            detailproductssize = detailproducts.find_all("fieldset", class_="sizes")
            detailproductscolor = detailproducts.find_all("fieldset", class_="colors")
            # print(detailproductssize)
            producttypesize = []
            productsize = []
            productcolor = []
            # selectsizeonly = detailproductssize.find_all("a", {"name": "size"})
            # print(selectsizeonly)

            # product type
            for pts in detailproductssizetype:
                print(pts.text, end=" ")
                producttypesize.append(pts.text)

            print('')
            # product size
            for a in detailproductssize:
                # print(a.find_all("a", {"name": "size"}))
                for sizea in a.find_all("a", {"name": "size"}):
                    # print(sizea.text, end=" ")
                    productsize.append(sizea.text)
                    # allcolor = detailproductscolor.find_all("a")
                    # print(detailproductscolor)
            print('')
            # product color
            for index_dpc, a in enumerate(detailproductscolor):
                # print(a.find_all("a"))

                for index_a, pc in enumerate(a.find_all("a")):
                    pc_text = pc.text.replace(' - Online Exclusive', '')
                    # print(index_a + 1 + index_dpc, pc_text.strip())
                    # print("2")
                    productcolor.append(pc_text.strip())  # # # # #  #
            print('')

            productcategory = category_breadcrumb
            productslug = product_name.lower()
            productslug = productslug.replace(" ", "-")
            productslug = productslug.translate({ord('$'): None})
            productslug = productslug.translate({ord('&'): None})
            variant_count = 0

            # For Color Varient
            for color in productcolor:
                print(color)
                color_ed = color.replace(" ", "-")
                productslug = productslug + "-" + color_ed.lower()
                print(productslug)
                for size in productsize:
                    variant_count += 1
                    if variant_count == 1:
                        productType = "main"
                    else:
                        productType = ""

                    print(variant_count, size)

                    # sku and baseId
                    global baseId_count
                    global sku_count
                    # global imagesku_count
                    sku = "A0E2000000021S" + str(sku_count)
                    # isku = "A0E2000000021S" + str(imagesku_count)
                    baseId = baseId_count
                    print("sku:", sku)
                    print("baseId:", baseId)

                    # Send to aws
                    # icount = 1
                    # for image in product_images.split(";"):
                       # upload_file_to_aws_s3(image, icount)
                        # icount += 1
                    # End

                    products.append({"productType": productType, "variantId": variant_count, "sku": sku,
                                     "prices": productprice,
                                     "tax": "standard", "categories": productcategory,
                                     "images": product_images,
                                     "name.en": product_name, "description.en": "",
                                     "slug.en": productslug,
                                     "metaTitle.en": "", "metaDescription.en": "", "metaKeywords.en": "",
                                     "name.de": product_name,
                                     "description.de": "", "slug.de": productslug,
                                     "metaTitle.de": "",
                                     "metaDescription.de": "", "metaKeywords.de": "", "name.it": "",
                                     "description.it": "",
                                     "slug.it": productslug, "metaTitle.it": "", "metaDescription.it": "",
                                     "metaKeywords.it": "",
                                     "creationDate": "", "articleNumberManufacturer": "MT980 BB",
                                     "articleNumberMax": "",
                                     "matrixId": "", "baseId": baseId, "designer": "newbalance",
                                     "madeInItaly": "no", "completeTheLook": "", "commonSize": "", "size": size,
                                     "color": color, "colorFreeDefinition.en": "multi", "details.en": "",
                                     "colorFreeDefinition.de": "multi", "details.de": "", "colorFreeDefinition.it": "",
                                     "details.it": "", "style": "", "gender": "", "season": "",
                                     "isOnStock": "", "isLook": "", "lookProducts": "", "seasonNew": "",
                                     "name": product_name, "SizeType": producttypesize})
                    sku_count += 1
                    # imagesku_count += 1
                    baseId_count += 1

            print(products)

    except Exception as e:
        print(e)

    return None
    # product loop ends here


# Extraction of sub categories of categories0:
for categories0_index, cat1_element in enumerate(categories0):
    page1 = requests.get(cat1_element.get("url")).text
    soup1 = BeautifulSoup(page1, "lxml")
    left_menu = soup1.findAll("div", class_="categories component")
    print(categories0[categories0_index].get('name'))
    products = []
    for index, menu in enumerate(left_menu):
        menu1 = menu.findAll("a")
        for index, menu1_items in enumerate(menu1):
            try:
                if menu1_items["href"]:  # sub-category
                    print("    ", menu1_items.text.strip(), "- url :", menu1_items.attrs['href'])
                    product_categories.append({"name": menu1_items.text.strip(), "url": menu1_items.attrs['href']})
                    x = x + 1
                    slug = categories0[categories0_index].get('name').lower() + "-" + menu1_items.text.strip().lower()
                    slug = slug.replace(" ", "-")
                    slug = slug.translate({ord('$'): None})
                    slug = slug.translate({ord('&'): None})
                    product_categories.append(
                        {"key": "c" + str(x), "externalId": x, "name.de": menu1_items.text.strip(),
                         "slug.de": slug, "name.en": menu1_items.text.strip(),
                         "slug.en": slug, "name.it": menu1_items.text.strip(),
                         "slug.it": slug, "parentId": categories0_index + 1, "webImageUrl": "",
                         "iosImageUrl": ""})
                    # print(product_categories)

                    product_loop(menu1_items.attrs['href'])
                    # print("    ", menu1_items.text.strip(), "- url :", menu1_items.attrs['href'])
                    print("end of first AT ease")
                # break
            except KeyError:
                print("  ", menu1_items.text)  # prints sub-category-title
                # pass

    jsonStr = json.dumps({"name": "products", "url": "", "children": products})
    file_name = "anntaylor-products_" + str(categories0_index) + ".json"
    jsonFile = open(file_name, "w")
    jsonFile.write(jsonStr)
    jsonFile.close()
    print("end categories-product string")
    print("file saved")
    # break
    # break

# categories1.append({"name": cat1_element.get("name"), "sub_categories":[]})

# wproducts = soup1.find_all("ul")
