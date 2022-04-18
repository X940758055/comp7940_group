import pymysql


def init(host, user, password, port, database):
    db = pymysql.connect(host=host, user=user, passwd=password, port=int(port), database=database)
    return db

def write_TV_review(db, t_name, comment_name, comment_description, comment_time):
    sql = "insert into tv(t_name, comment_name, comment_description, comment_time) value ('{}', '{}', '{}', '{}')"\
        .format(t_name, comment_name, comment_description, comment_time)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def show_TV_review(db, t_name):
    sql = "select * from tv where t_name = '{}' ".format(t_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    res = []
    for row in results:
        temp = {}
        temp["t_id"] = row[0]
        temp["t_name"] = row[1]
        temp["comment_name"] = row[2]
        temp["comment_description"] = row[3]
        temp["comment_time"] = row[4]
        res.append(temp)
    return res


def write_hiking_routine(db, hr_name, comment_name, comment_description, comment_time):
    sql = "insert into hiking_routine (hr_name, comment_name, comment_description, comment_time) value ('{}', '{}', '{}', '{}')"\
        .format(hr_name, comment_name, comment_description, comment_time)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


def show_hiking_routine(db, hr_name):
    sql = "select * from hiking_routine where hr_name = '{}' ".format(hr_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    res = []
    for row in results:
        temp = {}
        temp["hr_id"] = row[0]
        temp["hr_name"] = row[1]
        temp["comment_name"] = row[2]
        temp["comment_description"] = row[3]
        temp["comment_time"] = row[4]
        res.append(temp)
    return res

def write_hiking_photo(db, hp_name, path, username):
    sql = "insert into hiking_photo (hp_name, photo_path, user_name) value ('{}', '{}', '{}')"\
        .format(hp_name, path, username)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def show_hiking_photo(db, hp_name):
    sql = "select * from hiking_photo where hp_name = '{}' ".format(hp_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    res = []
    for row in results:
        temp = {}
        temp["hp_id"] = row[0]
        temp["hp_name"] = row[1]
        temp["photo_path"] = row[2]
        temp["user_name"] = row[3]
        res.append(temp)
    return res


def write_cookary(db, c_name, path, username):
    sql = "insert into cookary (c_name, video_path, user_name) value ('{}', '{}', '{}')"\
        .format(c_name, path, username)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def show_cookary(db, c_name):
    sql = "select * from cookary where c_name = '{}' ".format(c_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    res = []
    for row in results:
        temp = {}
        temp["c_id"] = row[0]
        temp["c_name"] = row[1]
        temp["video_path"] = row[2]
        temp["user_name"] = row[3]
        res.append(temp)
    return res