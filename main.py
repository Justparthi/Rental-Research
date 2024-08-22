import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


form_link = "https://docs.google.com/forms/d/e/1FAIpQLSfk5yDqHxCSfdzUtRv0irOKxohINXOzXVe5php38dPfrNmTgQ/viewform?usp=sf_link"

zillo = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(zillo)
data = response.text


soup = BeautifulSoup(data, 'html.parser')


links = []
all_list = soup.find_all(name='li', class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
for list in all_list:
    links.append(list.find(name="a").get('href'))


all_prices_el = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_prices_el if "$" in price.text]



address_list = []
address = soup.select(".StyledPropertyCardDataArea-anchor address")


for add in address:
    items = add.get_text().replace("|", "").split("\n",)
    cleaned_items = [item.strip() for item in items if item.strip()]

    address_list.append(cleaned_items)


loop_time = int(len(links))

# Auto part


for i in range(loop_time):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)


    driver = webdriver.Chrome(options=options)
    driver.get(form_link)

    driver.maximize_window()

    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_input.send_keys(f"{links[i]}")
    price_input.send_keys(f"{all_prices[i]}")
    property_input.send_keys(f"{address_list[i]}")

    submit.click()

    driver.close()

    sleep(2)

















