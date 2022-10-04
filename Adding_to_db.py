import sqlite3

db = sqlite3.connect('main_DB')
cursor = db.cursor()
cursor.execute("""create table IF NOT EXISTS group_to_facs(id, name, fullname, id_fac, name_fac, fullname_fac)""")

group_names = []
group_ids = []
group_names_ids = []

with open('message (5).txt', 'r', encoding='utf-8') as eny:
    lines = eny.readline().split("', ")
    for l in range(len(lines)):
        line = lines[l].replace("'", '').replace('гр. ', '').split(' (')[0]
        group_names.append(line)

    lines = eny.readline().split("', ")
    for l in range(len(lines)):
        line = lines[l].replace("'", '').replace('гр. ', '').split(' (')[0]
        group_ids.append(line)

    for i in range(len(group_names)):
        group_names_ids.append([group_names[i], int(group_ids[i])])

a = 'ЭИ - Электроэнергетический институт - 6'.split(' - ')

id_fac = int(a[2])
name_fac = a[0]
fullname_fac = a[1]

for data in group_names_ids:
    cursor.execute("""insert into group_to_facs values(?, ?, ?, ?, ?, ?)""",
                   (data[1], data[0].split(' - ')[0], data[0].split(' - ')[1], id_fac, name_fac, fullname_fac))

db.commit()
db.close()
