import sqlite3

db = sqlite3.connect('main_DB')
cursor = db.cursor()

print('Введите сокращённое название своей группы(пример - БО211ПИН)')
user_group = input()

id_group, id_fac = cursor.execute("""select id, id_fac from group_to_facs where name = ?""", (user_group, )).fetchall()[0]
print('Номер группы ->', id_group)
print('Номер института ->', id_fac)
db.commit()
db.close()