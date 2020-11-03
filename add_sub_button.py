import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ids = open("ID.txt", mode='r').readlines()

config = open('config.txt', mode='r').readlines()
username_text = config[0].strip()
password_text = config[1].strip()

driver = webdriver.Firefox()

driver.get("https://www.aparat.com/login?redirect_url=https://www.aparat.com/dashboard")

time.sleep(2)

username = driver.find_element_by_id('username')
username.send_keys(username_text)
username.send_keys(Keys.ENTER)

time.sleep(3)

password = driver.find_element_by_id('password')
password.send_keys(password_text)
password.send_keys(Keys.ENTER)

for id in ids:
    try:
        time.sleep(1)

        driver.get("https://www.aparat.com/video/video/edit/videohash/" + str(id).strip())
        driver.find_element_by_id('tab_featured').click()
        time.sleep(1)
        driver.find_element_by_class_name('featured-edit').find_element_by_class_name('dropdown-toggle').click()
        time.sleep(1)
        driver.find_element_by_class_name('request-link').click()
        time.sleep(1)
        driver.find_element_by_id('featureAnnotationContent').find_element_by_class_name('form-buttons').find_element_by_tag_name('button').click()
        time.sleep(1)
    except:
        continue
