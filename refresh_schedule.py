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

schedule_url = 'https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable'


def run():
    from time import sleep
    from datetime import date, timedelta
    from selenium.webdriver.common.by import By

    def schedule(*, time: str, facultet: str, group: str, dates: list):
        global date_id
        from selenium.webdriver.support.select import Select

        try:
            # select timeline
            select_element = driver.find_element(By.NAME, 'time')
            Select(select_element).select_by_value(time)

            # select facultet
            select_element = driver.find_element(By.NAME, 'facultet')
            Select(select_element).select_by_value(facultet)

            sleep(2)

            # select group
            select_element = driver.find_element(By.NAME, 'group')
            Select(select_element).select_by_value(group)

            sleep(2)

            # screenshot schedule / by day optional
            select_element = driver.find_element(By.ID, 'curGroup')
            sleep(2)
            header_elements = select_element.find_elements(By.TAG_NAME, 'h3')
            headers = []
            for header in header_elements:
                h = header.text.split('.')[:2]
                headers.append('.'.join(h))
            schedule_elements = select_element.find_elements(By.TAG_NAME, 'tbody')
            print(headers)
            date_request = input('Input date: ')
            for id in range(len(headers)):
                if headers[id].find(date_request):
                    date_id = id + 1
                else:
                    break
            for date in dates:
                pass

            schedule_elements[date_id].screenshot(headers[date_id] + '.png')

        except Exception as ex:
            print(ex)

    try:
        # open schedule URL
        driver.get(schedule_url)

        # today and tomorrow dates
        dates = [str(date.today()).split('-')[1] + '.' + str(date.today()).split('-')[2],
                 str(date.today() + timedelta(days=1)).split('-')[1] + '.' + str(date.today() + timedelta(days=1)).split('-')[2]]



    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

run()