# Commerce-et-tool
This is a et tool extract data from website

- Download PyCharm (Community Edition)

#### Install the following Required Packages
- pip install requests
- pip install html5lib
- pip install bs4
- pip install beautifulsoup4
- pip install lxml
- pip install selenium
- pip install boto3
- pip install --upgrade pip (optional)
- pip install python-dotenv

#### Image copy process from anntaylor :

- Copy the "Chromedriver.exe"
- past in your local path "C:\Users\Username\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"

####If chrome not in the program file :
- use the following code
- options = Options()
- options.binary_location = "chrome path(chrome.exe)"

#### For AWS Image upload to s3 Bucket configuration :
- Create a file name ".env" in project root with following Details:
- AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
- AWS_SECRET_KEY = "AWS_SECRET_KEY"
- AWS_REGION = "AWS_REGION"
- AWS_BUCKET_NAME = "AWS_BUCKET_NAME"
- AWS_S3_ENDPOINT = "AWS_S3_ENDPOINT"

To Run the project
- anntaylor_decoding.py --> Run
