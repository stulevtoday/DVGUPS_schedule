from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# options | required settings
options = Options()
# used for ease of writing code | in future this func will be disabled
options.add_argument("start-maximized")
# path to chromedriver
driver = webdriver.Chrome(
    service=Service(r'C:\Users\Danil\PycharmProjects\selenium\chromedriver_win32\chromedriver.exe'),
    options=options)  # Optional argument, if not specified will search path.

rating_url = 'https://www.dvgups.ru/studtopmenu/student-rating'

def rating(*, groupname: str, username: str):
    from time import sleep
    from selenium.webdriver.common.by import By

    try:
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
            'person_rating.png')

        sleep(3)

        driver.refresh()

    except Exception as ex:
        print(ex)
        driver.refresh()

    finally:
        driver.close()
        driver.quit()
