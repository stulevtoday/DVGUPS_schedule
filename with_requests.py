import requests
from bs4 import BeautifulSoup
import os.path
from datetime import date, timedelta
import search

def parse_date(date_of):
	this_day = str(date_of).split("-")
	this_day = ".".join([this_day[-1], this_day[1], this_day[0]])
	return this_day

def collect_timetable(time="24.10.2022", 
	group="52752", date_of="28.10"):
	#пока что мы будем использовать свои выходные данные
	url = "https://www.dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable"
	# отправим post запрос
	
	data = {
		#"Time":time,
		'GroupID': group
	}

	r = requests.post(url=url, data=data)
	filename = group + "_" + date_of + ".html"
	with open(filename, "w") as file:
		file.write(r.text)
	return filename

def for_timetable(filename, today):
	with open(filename) as file:
		soup = BeautifulSoup(file.read(), "lxml")
	# под h3 с нашей датой находится наша таблица
	timetable = soup.find_all("h3")

	info = {}
	important_time = ""
	for time in timetable:
		if today in time.next_element:
			important_time = time
			break
	if not(important_time):
		return info
		
	tb_for_today = important_time.next_sibling

	trs = tb_for_today.find_all("tr")

	info = {}
	for tr in trs:
		tds = tr.find_all("td")
		subj_info = []
		for td_i in range(1, 3):
			subj_info.append((tds[td_i].next_element))
		info[tds[0].next_element.next_element] = subj_info

	return info

def process(group="52752", agreement="С"):
	if agreement == "С":
		date_of = parse_date(date.today())
	else:
		date_of = parse_date(date.today() + timedelta(days=1))

	filename = group + "_" + date_of + ".html"
	if os.path.exists(filename):
		return for_timetable(filename, date_of)
	else:
		filename = collect_timetable(group=group, date_of=date_of)
		if agreement == "С":
			search.schedule_today_ch(int(group), filename)
		else:
			search.schedule_tomorrow_ch(int(group), filename)
		return for_timetable(filename, date_of)

def main():
	print(process())

if __name__ == "__main__":
	main()