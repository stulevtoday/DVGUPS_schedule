def group_parse(user_group):
    import sqlite3
    db = sqlite3.connect('main_DB')
    cursor = db.cursor()
    id_group, id_fac = \
        cursor.execute("""select id, id_fac from group_to_facs where name = ?""", (user_group,)).fetchall()[0]
    return id_group, id_fac
    db.commit()
    db.close()


def user_add(id, id_group, id_fac, fullname):
    import sqlite3
    db = sqlite3.connect('main_DB')
    cursor = db.cursor()
    cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?)""", (id, id_group, id_fac, fullname))
    db.commit()
    db.close()


def user_pull(id):
    import sqlite3
    db = sqlite3.connect('main_DB')
    cursor = db.cursor()
    negr = cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,)).fetchall()[0]
    return negr
    db.commit()
    db.close()


def user_name_ch(id, newname):
    import sqlite3
    db = sqlite3.connect('main_DB')
    cursor = db.cursor()
    cursor.execute("""UPDATE users SET fullname=? WHERE id=?""", (newname, id))
    db.commit()
    db.close()


def user_group_ch(id, newgroup_id):
    import sqlite3
    db = sqlite3.connect('main_DB')
    cursor = db.cursor()
    newfac_id = cursor.execute("""SELECT id_fac FROM group_to_facs WHERE id=?""", (newgroup_id,)).fetchall()[0]
    cursor.execute("""UPDATE users SET group_id=?, fac_id=? WHERE id=?""", (newgroup_id, newfac_id[0], id))
    db.commit()
    db.close()



