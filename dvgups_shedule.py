from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

db_time = {
    'names': [],
    'values': [],
}

db_facultet = {
    'names': [],
    'values': [],
}

db_group = {
    'names': [],
    'values': [],
}


def cut(n: list, v: list):
    return n[1:], v[1:]


# todo: options
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(r'C:\Users\Danil\PycharmProjects\selenium\chromedriver_win32\chromedriver.exe'),
    options=options)  # Optional argument, if not specified will search path.

# todo: url
driver.get('https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable')

sleep(1)

from selenium.webdriver.support.select import Select

# todo: time
select_element = driver.find_element(By.NAME, 'time')
time_elements = select_element.find_elements(By.TAG_NAME, 'option')
for time in time_elements:
    db_time['names'].append(time.text)
    db_time['values'].append(time.get_attribute('value'))
select_object = Select(select_element)
select_object.select_by_value('12.09.2022')

sleep(1)

# todo: facultet
select_element = driver.find_element(By.NAME, 'facultet')
facultet_elements = select_element.find_elements(By.TAG_NAME, 'option')
for facultet in facultet_elements:
    db_facultet['names'].append(facultet.text)
    db_facultet['values'].append(facultet.get_attribute('value'))
db_facultet['names'], db_facultet['values'] = cut(n=db_facultet['names'], v=db_facultet['values'])
select_object = Select(select_element)
select_object.select_by_value('6')

sleep(1)

# todo: group
select_element = driver.find_element(By.NAME, 'group')
group_elements = select_element.find_elements(By.TAG_NAME, 'option')
for group in group_elements:
    db_group['names'].append(group.text)
    db_group['values'].append(group.get_attribute('value'))
db_group['names'], db_group['values'] = cut(n=db_group['names'], v=db_group['values'])
select_object = Select(select_element)
select_object.select_by_value('52800')

sleep(5)

# todo: schedule
select_element = driver.find_element(By.ID, 'curGroup')
header_elements = select_element.find_elements(By.TAG_NAME, 'h3')
headers = []
for header in header_elements:
    headers.append(header.text)
schedule_elements = select_element.find_elements(By.TAG_NAME, 'tbody')
for id in range(len(schedule_elements)):
    schedule_elements[id].screenshot(headers[id] + '.png')


# print(db_time['names'])
# print(db_time['values'])
# print(db_facultet['names'])
# print(db_facultet['values'])
# print(db_group['names']) # id, v_facultet, v_group
# print(db_group['values'])

driver.quit()
