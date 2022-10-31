import requests
from bs4 import BeautifulSoup
import os.path
from datetime import date, timedelta
import search
import json

def parse_date(date_of):
	this_day = str(date_of).split("-")
	this_day = ".".join([this_day[-1], this_day[1], this_day[0]])
	return this_day

def collect_timetable(group="52752", date_of="28.10.2022"):

	first_streak = date(2022, 10, 10)
	row_data = list(map(int, date_of.split('.')))
	some_day = date(row_data[-1], row_data[1], row_data[0])
	while not(first_streak <= some_day < first_streak + timedelta(days=14)):
		# пока не в нужном диапазоне
		first_streak += timedelta(days=14)
	#пока что мы будем использовать свои выходные данные
	url = "https://www.dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable"
	# отправим post запрос
	filename = group + "_" + date_of + "_" +"schedule" + ".json"
	data = {
		"Time":parse_date(first_streak),
		'GroupID': group
	}

	r = requests.post(url=url, data=data)
	
	soup = BeautifulSoup(r.text, "lxml")
	# под h3 с нашей датой находится наша таблица
	timetable = soup.find_all("h3")

	info = {}
	important_time = ""
	for time in timetable:
		if date_of in time.next_element:
			important_time = time
	if not(important_time):
		with open(filename, "w") as file:
			json.dump({}, file)
		return filename
	tb_for_today = important_time.next_sibling

	trs = tb_for_today.find_all("tr")

	info = {}
	for tr in trs:
		tds = tr.find_all("td")
		subj_info = []
		for td_i in range(1, 3):
			subj_info.append((tds[td_i].next_element))
		info[tds[0].next_element.next_element] = subj_info
	with open(filename, "w") as file:
		json.dump(info, file)
	return filename

def for_timetable(filename):
	with open(filename) as file:
		info = json.load(file)
	return info

def for_update(group):
	date_of = parse_date(date.today())
	filename = group + "_" + date_of + "_" +"schedule" + ".json"
	collect_timetable(group=group, date_of=date_of)

	date_of = parse_date(date.today() + timedelta(days=1))
	filename = group + "_" + date_of + "_" +"schedule" + ".json"
	collect_timetable(group=group, date_of=date_of)


def process(group="52749", agreement="З"):
	if agreement == "С":
		date_of = parse_date(date.today())
	else:
		date_of = parse_date(date.today() + timedelta(days=1))
	filename = group + "_" + date_of + "_" +"schedule" + ".json"
	if os.path.exists(filename):
		return for_timetable(filename)
	else:
		filename = collect_timetable(group=group, date_of=date_of)
		return for_timetable(filename)

def main():
	print(process())

if __name__ == "__main__":
	main()