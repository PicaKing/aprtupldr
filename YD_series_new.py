import time

import certifi
from pytube import YouTube

certifi.where()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

config = open('config.txt', mode='r').readlines()
username_text = config[0].strip()
password_text = config[1].strip()

keywords_sheet = client.open('AparatUploaderURL').worksheet('keywords').get_all_records()
details_sheet = client.open('AparatUploaderURL').worksheet('details').get_all_records()

while True:
    sheet = client.open('AparatUploaderURL').worksheet('NewSeries')
    data = sheet.get_all_records()
    if data[-1]['status'] == '':
        print('I found some new URL!')
        i = 0
        for item in data:
            keyword_key = item['keyword']
            detail_key = item['detail']

            yt = False
            i += 1
            if item['status'] != 1:
                # print()
                # link = input("Enter the link: ")
                flag = True
                j = 0
                while flag == True:
                    try:
                        yt = YouTube(item['URL'])
                        if item['quality'] != '':
                            ys = yt.streams.get_by_resolution(item['quality'])
                        else:
                            ys = yt.streams.get_highest_resolution()
                        address = ys.download()
                        flag = False
                    except:
                        if j < 5:
                            j += 1
                            time.sleep(1)
                        else:
                            flag = False
                            sheet.update_cell(i + 1, 2, '-1')
                        continue
                # ys.download('location')

                # title = open('title.txt', mode='r', encoding="UTF8").read()
                # desc = open('description.txt', mode='r', encoding="UTF8").read()
                # tags = open('tags.txt', mode='r', encoding="UTF8").readlines()

                tags = pd.DataFrame(keywords_sheet).set_index('key').query('key == "' + keyword_key + '"').values[0]
                desc = pd.DataFrame(details_sheet).set_index('key').query('key == "' + detail_key + '"')[['desc']].values[0][0]
                title = pd.DataFrame(details_sheet).set_index('key').query('key == "' + detail_key + '"')[['title']].values[0][0]

                if title == '':
                    title = yt.title[:80]
                    desc = ''
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

                time.sleep(3)

                driver.get("https://www.aparat.com/upload")
                # driver.find_element_by_id('browseButton').click()

                time.sleep(3)

                driver.find_element_by_id('browseButton').find_element_by_tag_name('input').send_keys(address)

                time.sleep(1)
                if item['row'] != '':
                    driver.find_element_by_name('title').send_keys(str(title).replace('xxxx', str(item['row'])))
                    driver.find_element_by_tag_name('textarea').send_keys(str(desc).replace('xxxx', str(item['row'])))
                else:
                    driver.find_element_by_name('title').send_keys(str(title))
                    driver.find_element_by_tag_name('textarea').send_keys(str(desc))

                driver.find_elements_by_class_name('ss-add')[0].click()
                time.sleep(2)

                for tag in tags:
                    driver.find_elements_by_class_name('ss-main')[1].find_element_by_tag_name('input').send_keys(tag)
                    time.sleep(3)
                    driver.find_elements_by_class_name('ss-main')[1].find_element_by_tag_name('input').send_keys(Keys.ENTER)
                    time.sleep(2)
                while True:
                    try:
                        if driver.find_element_by_class_name('status').find_element_by_tag_name('span').text == 'ویدیوی شما با موفقیت بارگذاری شد':
                            driver.find_element_by_class_name('form-buttons').find_element_by_name('video_pass').click()
                            sheet.update_cell(i + 1, 2, '1')
                            time.sleep(3)
                            driver.close()
                            break
                        else:
                            time.sleep(5)
                    except:
                        time.sleep(5)
    else:
        time.sleep(120)
