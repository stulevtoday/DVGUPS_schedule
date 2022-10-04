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

try:
    iframe = driver.find_element(By.ID, 'blockrandom')
    driver.switch_to.frame(iframe)
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_LinkButtonFind').click()
    sleep(2)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()