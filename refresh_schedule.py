from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import date, timedelta
from selenium.webdriver.common.by import By

from settings import chromedriver_path
import datetime

# options | required settings
options = Options()
# used for ease of writing code | in future this func will be disabled
options.add_argument("start-maximized")
# path to chromedriver
driver = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=options)  # Optional argument, if not specified will search path.

schedule_url = 'https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable'

gr_ids = [52804, 52816, 47150, 52729, 52718, 52725, 52719, 52728, 52727, 52720, 52135, 52110, 52122, 52116, 52132,
          52129, 52113, 50124, 50110, 49963, 49798, 50120, 50114, 49795, 47177, 47146, 47137, 47169, 47160, 47133,
          47164, 52730, 52722, 52724, 52887, 52721, 52810, 52138, 52683, 52121, 52119, 52139, 52726, 52125, 49958,
          47154, 44931, 52804, 52816, 47150, 52729, 52718, 52725, 52719, 52728, 52727, 52720, 52135, 52110, 52122,
          52116, 52132, 52129, 52113, 50124, 50110, 49963, 49798, 50120, 50114, 49795, 47177, 47146, 47137, 47169,
          47160, 47133, 47164, 52730, 52722, 52724, 52887, 52721, 52810, 52138, 52683, 52121, 52119, 52139, 52726,
          52125, 49958, 47154, 44931, 50381, 50302, 50341, 50403, 50306, 50322, 50310, 50466, 50367, 50371, 50624,
          50510, 50515, 50673, 50565, 50570, 50575, 50580, 50520, 50476, 50483, 50683, 50635, 50688, 50640, 50505,
          50649, 50535, 50540, 50694, 52528, 50595, 50600, 50605, 50615, 50545, 50488, 50494, 50708, 50726, 50659,
          50713, 50664, 50720, 50555, 48475, 47767, 50076, 47772, 48192, 47908, 51427, 50047, 47852, 47747, 48197,
          48480, 48202, 48470, 47787, 32983, 32953, 32948, 45536, 32973, 32993, 53449, 53454, 45252, 32963, 45526,
          45542, 32988, 45531, 45825, 32942, 32746, 32958, 52736, 52808, 52809, 52171, 52174, 52177, 52862, 49819,
          52861, 54100, 52705, 52706, 48145, 52700, 52701, 54152, 54153, 52692, 52689, 52690, 52691, 52184, 52181,
          52182, 52183, 52739, 52737, 52742, 52743, 52738, 52740, 52193, 52185, 52201, 52206, 52189, 52864, 52197,
          50028, 50016, 50011, 50007, 50020, 51062, 50024, 48283, 48271, 48150, 48137, 48275, 48287, 48279, 45165,
          45150, 45137, 45142, 45155, 44867, 51069, 45160, 44872, 33344, 52735, 52167, 49870, 49889, 46838, 46833,
          52764, 52765, 52734, 52731, 52732, 52733, 52163, 52155, 52147, 52159, 52151, 52912, 52911, 49877, 49873,
          49885, 52909, 52910, 46859, 46847, 46864, 46852, 45240, 45230, 45184, 45236, 52908, 52535, 52750, 52752,
          52756, 52214, 52533, 52224, 52231, 52228, 52536, 49976, 54151, 49981, 52537, 46904, 52234, 46925, 52747,
          52751, 52744, 52811, 52217, 52227, 52210, 52748, 52757, 52753, 52749, 52758, 52755, 51211, 52218, 52235,
          51215, 52868, 52222, 52239, 52869, 52243, 49986, 50128, 52867, 50132, 49990, 52870, 51206, 50136, 46912,
          46896, 51224, 46933, 46917, 46938, 45069, 45053, 50850, 45090, 45079, 45075, 48564, 52768, 52767, 52693,
          52694, 52760, 52766, 52761, 52850, 52244, 52254, 52247, 52851, 52250, 49934, 54146, 52545, 46963, 54145,
          52853, 51007, 48561, 52763, 54147, 52769, 52253, 54169, 52856, 52772, 52697, 52770, 52771, 52257, 52261,
          52854, 50140, 51011, 46982, 46987, 45204, 45208, 45212, 52685, 51872, 52895, 52684, 53000, 52781, 52793,
          52708, 52715, 51257, 50262, 47040, 52714, 52779, 52806, 52807, 52791, 52792, 52268, 52295, 52298, 50239,
          50144, 47035, 52140, 52143, 49801, 49804, 47057, 47065, 52782, 52711, 51318, 52790, 52794, 52146, 52301,
          52713, 52785, 52780, 52783, 52784, 52786, 52788, 52789, 52279, 52271, 52275, 52283, 52287, 52291, 52849,
          51230, 50243, 52272, 49996, 51234, 51238, 47011, 47016, 47026, 45003, 45011, 45019, 45023, 52796, 52795,
          52305, 52302, 49811, 49808, 47003, 46998, 52800, 52802, 52803, 52313, 52317, 52877, 52879, 49945, 52878,
          47518, 52875, 52886, 52884, 52885, 52799, 52801, 52312, 52316, 52797, 52798, 51930, 52308, 50151, 50155,
          47503, 47508, 45097, 45101]
fac_ids = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
           8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
           8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
           11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
           11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
           11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
           4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 34, 34,
           34, 34, 34, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
           7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 5,
           6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]


def schedule(*, time: str, facultet: str, group: str, dates):
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

        for id_i in range(len(headers)):
            if headers[id_i] == dates[0]:
                schedule_elements[id_i].screenshot(group + '_' + dates[0] + '.png')
            elif len(dates) > 1:
                if headers[id_i] == dates[1]:
                    schedule_elements[id_i].screenshot(group + '_' + dates[1] + '.png')

        driver.refresh()

    except Exception as ex:
        print(ex)

def to_standart_after(today, days_after: int):
    # добавляет к нынешнему времени
    # определённое количество дней
    # и возвращает дату
    raw_date = str(today + timedelta(days=days_after)).split('-')
    return raw_date[2] + '.' + raw_date[1]

def check_streak(today, first_streak, days):
    if (today + timedelta(days=days)) == (first_streak + timedelta(days=14)):
        return first_streak + timedelta(14)
    return first_streak


# стартовый поток
first_streak = datetime.date(2022, 10, 10)
today = date.today()
day_of_week = datetime.datetime.today().weekday()

while not(first_streak <= today < first_streak + timedelta(days=14)):
    # пока не в нужном диапазоне
    first_streak += timedelta(days=14)
second_streak = first_streak

if day_of_week < 4:
    # всё норм, всё на этой неделе
    date1 = to_standart_after(today=today, days_after=0)
    
    date2 = to_standart_after(today=today, days_after=1)
elif day_of_week == 4:
    # если сегодня пятница
    date1 = to_standart_after(today=today, days_after=0)
    # нужно проверить по селектору для следующего понедельника
    second_streak = check_streak(today, first_streak, 3)
    # следующий день отправляем понедельник
    date2 = to_standart_after(today=today, days_after=3)
elif day_of_week > 4:
    # если сегодня суббота или вообще воскресение
    # то мы отправим понедельник и вторник
    if day_of_week == 5:
        # если сегодня суббота
        days = 2
        first_streak = check_streak(today, first_streak, 2)
        second_streak = first_streak
    elif day_of_week == 6:
        # если сегодня воскресенье
        days = 1
        first_streak = check_streak(today, first_streak, 1)
        second_streak = first_streak
    date1 = to_standart_after(today=today, days_after=days)
    
    date2 = to_standart_after(today=today, days_after=(days+1))
# open schedule URL
driver.get(schedule_url)

# today and tomorrow dates
first_streak = str(first_streak).split('-')
first_streak = first_streak[2] + '.' + first_streak[1] + "." + first_streak[0]

second_streak = str(second_streak).split("-")
second_streak = second_streak[2] + "." + second_streak[1] +"." + second_streak[0]

dates = {date1: first_streak,
date2: second_streak}
if second_streak == first_streak:
    dates = list(dates.keys())
print(dates, first_streak)
if type(dates) == list:
    for i in range(len(gr_ids)):
        schedule(time=first_streak, facultet=str(fac_ids[i]), group=str(gr_ids[i]), dates=[dates])
else:
    for i in range(len(gr_ids)):
        for date in dates.keys():
            schedule(time=dates[date], facultet=str(fac_ids[i]), group=str(gr_ids[i]), dates=list(date))

driver.close()
driver.quit()
