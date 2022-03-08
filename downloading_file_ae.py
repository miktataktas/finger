
import pyvirtualdisplay
import selenium
from selenium import  webdriver
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


ae_PASSWORD = 'xxxxx'
ae_URL      = 'http://xxx.xxx.xxx.xxx/cgi-bin/download.cgi'
start_date=datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y')
end_date=datetime.strftime(datetime.now(),'%d.%m.%Y')


def ae_conversion(waitTime):
    Initial_path = 'C:\\Users\\R&D\\Downloads\\'
    final_path='D:\\Monitoring Raw Data\\04.08.2017-AE Conversion\\daily_downloads\\'
    driver = webdriver.Chrome(executable_path=r'C:\Python\Python37\Lib\chromedriver.exe')
    driver.set_page_load_timeout(5)
    driver.get(ae_URL)
    driver.find_element_by_name("start_day").clear()
    driver.find_element_by_name("start_day").send_keys(start_date)
    driver.find_element_by_name("end_day").clear()
    driver.find_element_by_name("end_day").send_keys(end_date)
    driver.find_element_by_css_selector("input[type='submit']").click()
    driver.implicitly_wait(100)
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    endTime = time.time() + waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
               filename= driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
               filename = Initial_path + filename
               shutil.move(filename, os.path.join(final_path, r"" + start_date + ".csv"))
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break


    driver.quit()




# method to get the downloaded file name


if __name__ == '__main__':
    ae_conversion(3)

