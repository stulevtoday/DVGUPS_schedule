import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(r'C:\Users\Danil\PycharmProjects\selenium\chromedriver_win32\chromedriver.exe'), options=options)  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/')

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element(By.NAME, 'q')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()