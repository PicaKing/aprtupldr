import time

import certifi
from pytube import YouTube

certifi.where()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

config = open('config.txt', mode='r').readlines()
username_text = config[0].strip()
password_text = config[1].strip()

while True:
    sheet = client.open('AparatUploaderURL').sheet1
    data = sheet.get_all_records()
    if data[-1]['status'] == '':
        print('I found some new URL!')
        i = 0
        for item in data:
            i += 1
            if item['status'] != 1:
                # print()
                # link = input("Enter the link: ")
                try:
                    yt = YouTube(item['URL'])
                    ys = yt.streams.get_highest_resolution()
                    address = ys.download()
                except:
                    sheet.update_cell(i + 1, 2, '-1')
                    continue
                # ys.download('location')

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

                time.sleep(4)

                driver.get("https://www.aparat.com/upload")
                # driver.find_element_by_id('browseButton').click()

                time.sleep(4)

                driver.find_element_by_id('browseButton').find_element_by_tag_name('input').send_keys(address)

                time.sleep(1)

                driver.find_element_by_name('title').send_keys(str(yt.title))

                driver.find_elements_by_class_name('ss-add')[0].click()
                time.sleep(2)

                tags = ['ویدیو', 'video', 'دانلود ویدیو']
                for tag in tags:
                    driver.find_elements_by_class_name('ss-main')[1].find_element_by_tag_name('input').send_keys(tag)
                    time.sleep(2)
                    driver.find_elements_by_class_name('ss-main')[1].find_element_by_tag_name('input').send_keys(Keys.ENTER)
                    time.sleep(1)

                # driver.find_element_by_name('video_pass').click()

                while True:
                    try:
                        if driver.find_element_by_class_name('status').find_element_by_tag_name('span').text == 'ویدیوی شما با موفقیت بارگذاری شد':
                            driver.find_element_by_class_name('form-buttons').find_element_by_name('video_pass').click()
                            sheet.update_cell(i + 1, 2, '1')
                            time.sleep(2)
                            driver.close()
                            break
                        else:
                            time.sleep(5)
                    except:
                        time.sleep(5)
    else:
        time.sleep(120)
