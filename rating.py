from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from settings import chromedriver_path

from search import group_parse

from datetime import datetime

from time import sleep
from selenium.webdriver.common.by import By

import os.path
# options | required settings
options = Options()
# used for ease of writing code | in future this func will be disabled
options.add_argument("headless")
# path to chromedriver
driver = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=options)  # Optional argument, if not specified will search path.

rating_url = 'https://www.dvgups.ru/studtopmenu/student-rating'

def rating(*, groupname: str, username: str):
    time_now = str(datetime.now()).split()[0].split("-")
    filename = username + str(group_parse(groupname)[0]) + "_" + time_now[2] + '.' + time_now[1] + ".png"
    if os.path.exists(filename):
        return filename

    try:
        driver.get(rating_url)

        driver.switch_to.frame(driver.find_element(By.NAME, 'iframe'))
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_LinkButtonFind').click()

        sleep(2)

        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TextBoxGroup').send_keys(groupname)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Button1').click()

        sleep(3)

        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_GridView1_ctl02_LinkButton1').click()

        sleep(3)

        driver.find_element(By.LINK_TEXT, username).click()

        sleep(5)

        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ASPxGridView1_DXMainTable').screenshot(
            filename)

        sleep(3)

        driver.refresh()

    except Exception as ex:
        print(ex)
        driver.refresh()

    return filename
def main():
    rating(username='Стулёв Данил Евгеньевич', groupname='БО211ПИН')

if __name__ == "__main__":
    main()