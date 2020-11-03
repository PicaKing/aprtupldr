import ssl
import time
from datetime import datetime

import certifi
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

certifi.where()

ssl._create_default_https_context = ssl._create_unverified_context
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

config = open('config.txt', mode='r').readlines()
username_text = config[0].strip()
password_text = config[1].strip()

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
print ("Headless Firefox Initialized")
#driver = webdriver.Firefox()

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

driver.get('https://www.aparat.com/user/video/videos/page/1/perpage/2000')

time.sleep(1)

videos = driver.find_elements_by_class_name('thumb-wrapper')
video_ids = []
for video in videos:
    try:
        video_id = video.find_element_by_tag_name('a').get_attribute('href').split('/')[7]
    except:
        video_id = video.find_element_by_tag_name('a').get_attribute('href').split('/')[4]
    video_ids.append(video_id)
print('video ids collected!')
i = 0
for video_id in video_ids:
    i += 1
    driver.get('https://www.aparat.com/user/dashboard/video_stat/videohash/' + video_id)
    likes = driver.find_elements_by_css_selector('.stat-box')[0].find_element_by_tag_name('span').text
    total_views = driver.find_elements_by_css_selector('.stat-box')[1].find_element_by_tag_name('span').text
    total_duration = driver.find_elements_by_css_selector('.stat-box')[2].find_elements_by_tag_name('span')[1].text
    today_views = driver.find_elements_by_css_selector('.stat-box')[3].find_element_by_tag_name('span').text
    date = str(datetime.now()).split('.')[0]
    sheet = client.open('AparatUploaderURL').worksheet('Statistics')
    title = driver.find_element_by_class_name('thumb-title').find_element_by_tag_name('a').find_element_by_tag_name('span').text
    data = [video_id, title, date, total_views, today_views, total_duration, likes]
    sheet.append_row(data)
    print(str(i) + '/' + str(len(video_ids)))

driver.quit()