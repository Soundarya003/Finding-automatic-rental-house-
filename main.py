from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

# The links for the forms stored in constant variable
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSd_xsdzYjudeTu2EDqS-3T1gn_ZCe4-0O7a6rFJ_ATc50ZoXQ/viewform?usp=sf_link"
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

# we're providing our system headers for the response
headers  ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
"Accept-Language":"en-US,en;q=0.5"
}
response = requests.get(url=URL,headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# adding all the needed elements into respective lists which we
# obtained from scrapping
# rpartition() method partitions the given string based on the last occurrence of the delimiter
price_list = [price.getText().rpartition('+')[0] for price in soup.find_all(class_="list-card-price")]
address_list = [address.getText() for address in soup.find_all(class_ = "list-card-addr")]

# Here the first property has a different class so we obtain it
first_link = soup.find(name="a",class_="list-card-link list-card-link-top-margin list-card-img",href=True)
# we create list for links and add the first property
link_list = [first_link['href']]

# then we append rest of property's link
for links in soup.find_all(name="a",class_="list-card-link list-card-img",href=True):
            link_list.append(f"https://www.zillow.com{links['href']}")

# installing the web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# creating the loop to open website and enter all the values of the all lists
for i in range(len(link_list)):
    # opening the website
    driver.get(url=FORM_LINK)
    # letting it stay for 2 secs
    time.sleep(2)

    # finding the class of 3 blank spaces to fill in form
    address_text = driver.find_element(By.XPATH,
                                       "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_text = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_text = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    # entering the values automatically using selenium
    address_text.send_keys(address_list[i])
    price_text.send_keys(price_list[i])
    link_text.send_keys(link_list[i])
    # submitting after entering
    submit.click()

