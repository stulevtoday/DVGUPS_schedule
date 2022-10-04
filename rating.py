from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# todo: options
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(r'C:\Users\Danil\PycharmProjects\selenium\chromedriver_win32\chromedriver.exe'),
    options=options)  # Optional argument, if not specified will search path.

# todo: url
driver.get('https://www.dvgups.ru/studtopmenu/student-rating')
sleep(2)

def click_iframe():
    iframe = driver.find_element(By.NAME, 'iframe')
    driver.switch_to.frame(iframe)

try:
    # todo: auth
    click_iframe()
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_LinkButtonFind').click()

    sleep(2)

    # need group name
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TextBoxGroup').send_keys('БО211ПИН')
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Button1').click()

    sleep(3)

    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_GridView1_ctl02_LinkButton1').click()

    sleep(3)

    # need fullname
    driver.find_element(By.LINK_TEXT, 'Стулёв Данил Евгеньевич').click()

    sleep(5)

    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ASPxGridView1_DXMainTable').screenshot('person_rating.png')

    sleep(3)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()