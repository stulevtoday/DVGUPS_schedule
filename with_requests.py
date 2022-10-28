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
		'GroupID': '52752'
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
	for dat in timetable:
		if today in dat.text:
			k = dat.next_sibling
			pairs = k.find_all("b")
			for pair in pairs:
				row_line = pair.find_next().text.split()
				print(row_line)
				row_line = row_line[:-1]
				row_line[-1] = row_line[-1].split("FreeConferenceCall")[0]
				row_line[-1] = row_line[-1].split("Контакты")[0]
				info[pair.text] = " ".join(row_line)
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