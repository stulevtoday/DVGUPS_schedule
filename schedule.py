
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# options
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(r'C:\Users\Danil\PycharmProjects\selenium\chromedriver_win32\chromedriver.exe'),
    options=options)  # Optional argument, if not specified will search path.

schedule_url = 'https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable'

# function
def schedule(*, url: str):
    from time import sleep
    from selenium.webdriver.support.select import Select

    # request to FESTU's schedule
    driver.get(url)

    try:
        # select timeline
        select_element = driver.find_element(By.NAME, 'time')
        Select(select_element).select_by_value('12.09.2022')

        # select facultet
        select_element = driver.find_element(By.NAME, 'facultet')
        Select(select_element).select_by_value('2')

        sleep(2)

        # select group
        select_element = driver.find_element(By.NAME, 'group')
        Select(select_element).select_by_value('52752')

        sleep(2)

        # screenshot schedule / by day ll including later
        select_element = driver.find_element(By.ID, 'curGroup')
        header_elements = select_element.find_elements(By.TAG_NAME, 'h3')
        headers = []
        for header in header_elements:
            headers.append(header.text)
        schedule_elements = select_element.find_elements(By.TAG_NAME, 'tbody')
        for id in range(len(schedule_elements)):
            schedule_elements[id].screenshot(headers[id] + '.png')

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

schedule(url = schedule_url)