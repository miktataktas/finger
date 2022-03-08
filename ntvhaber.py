
import pyvirtualdisplay
import selenium
from selenium import  webdriver
import csv
import requests
import sys
from selenium.webdriver.chrome.options import Options
import re, datetime
from bs4 import BeautifulSoup
import time
from datetime import datetime,timedelta
import os
import shutil
import base64
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
def adpass(css):
    while True:
        try:
            button = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
            button.click()
            print
            
        except:
            break

def csvwriter( text1,text2,text3):
    with open('ntv_haberler.csv', 'a', encoding='utf-16') as news:
                        writer = csv.writer(news, delimiter=',')
                        writer.writerow([text1,text2,text3])
                        news.close()


# method to get the downloaded file name
if __name__ == '__main__':
    URL = 'https://www.ntv.com.tr/turkiye/'
    driver = webdriver.Chrome(executable_path=r'C:\Python\Python37\Lib\chromedriver.exe')
    driver.get(URL)
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    adpass("div.adm-close-btn-01")
    adpass("span.icon--1x4EzqLa5P")
    j=0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.infinite-link")))
                button.click()
            except:
                break
            last_height = new_height

        
        j=j+1
    page = BeautifulSoup(driver.page_source, "html.parser")
    veri = page.find_all("p", {"class": "card-text"})
    for div in veri:
        final_URL=''
        last_url=div.find('a')['href']
        if last_url!='':
            final_URL=URL.replace('''turkiye/''','')+last_url
            sayfa=requests.get(final_URL)
            page_news = BeautifulSoup(sayfa.content, "html.parser")
            haber_Baslik = page_news.find_all("h1", {"class": "category-detail-title"})
            haber_ozeti=page_news.find_all("h2",{"class":"category-detail-sub-title"})
            haber_tarih = page_news.find_all("p", {"class": "news-info-text"})
            match = re.search('\d{2}.\d{2}.\d{4}', haber_tarih[0].text)
            if match:
                with open('ntv_haberler.csv', 'a', encoding='utf-8') as news:
                    writer = csv.writer(news, delimiter=',')
                    writer.writerow([haber_Baslik[0].text,haber_ozeti[0].text,match.group()])
                    news.close()

    driver.quit()
