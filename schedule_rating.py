from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from settings import chromedriver_path
# options | required settings
options = Options()
# used for ease of writing code | in future this func will be disabled
options.add_argument("start-maximized")
# path to chromedriver
driver = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=options)  # Optional argument, if not specified will search path.

schedule_url = 'https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable'
rating_url = 'https://www.dvgups.ru/studtopmenu/student-rating'


def main():
    from time import sleep
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    def schedule(*, url: str, time: str, facultet: str, group: str):
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
            schedule_elements[date_id].screenshot(headers[date_id] + '.png')

        except Exception as ex:
            print(ex)

    def rating(*, url: str, username: str, groupname: str):
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

        except Exception as ex:
            print(ex)

    def process(*, rating_window: str, schedule_window: str, request_window: str):
        # get ID of current window
        current_window = driver.current_window_handle

        if request_window == 'у':
            if current_window != rating_window:
                driver.switch_to.window(rating_window)
            rating(url=rating_url, username='Стулёв Данил Евгеньевич', groupname='БО211ПИН')
            driver.refresh()

        elif request_window == 'р':
            if current_window != schedule_window:
                driver.switch_to.window(schedule_window)
            schedule(url=schedule_url, time='26.09.2022', facultet='2', group='52752')
            driver.refresh()

        else:
            print('Попробуйте снова. . .')
            return False

        return True

    try:
        # open schedule URL
        driver.get(schedule_url)

        # setup wait for later
        wait = WebDriverWait(driver, 10)

        # store the ID of the schedule window
        schedule_window = driver.current_window_handle

        # check we don't have other windows open already
        assert len(driver.window_handles) == 1

        # open a new window
        driver.switch_to.new_window('tab')

        # wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))

        # open rating URL
        driver.get(rating_url)

        # store the ID of the rating window
        rating_window = driver.current_window_handle

        # infinity cycle
        while True:
            request_window = input('Успеваемость / рейтинг: ')

            process(rating_window=rating_window, schedule_window=schedule_window,
                                     request_window=request_window)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()
    return rating

if __name__ == "__main__":
    main()