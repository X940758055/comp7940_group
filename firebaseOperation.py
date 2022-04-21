import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

TVcol = "TV"
HRcol = "hiking_routine"
HPcol = "hiking_photo"
COcol = "cookary"

def init(path):
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def write_TV_review(db, t_name, comment_name, comment_description, comment_time):
    TV_ref = db.collection(TVcol).document(str(uuid.uuid4()))
    TV_ref.set({
        't_name': t_name,
        'comment_name': comment_name,
        'comment_description': comment_description,
        'comment_time': comment_time
    })


def show_TV_review(db, t_name):
    results = db.collection(TVcol).where("t_name", "==", t_name).stream()

    res = []
    for row in results:
        res.append(row.to_dict())
    return res


def write_hiking_routine(db, hr_name, comment_name, comment_description, comment_time):
    HR_ref = db.collection(HRcol).document(str(uuid.uuid4()))
    HR_ref.set({
        't_name': hr_name,
        'comment_name': comment_name,
        'comment_description': comment_description,
        'comment_time': comment_time
    })

def show_hiking_routine(db, hr_name):
    results = db.collection(HRcol).where("t_name", "==", hr_name).stream()

    res = []
    for row in results:
        res.append(row.to_dict())
    return res



def write_hiking_photo(db, hp_name, path, username):
    HP_ref = db.collection(HPcol).document(str(uuid.uuid4()))
    HP_ref.set({
        'hp_name':hp_name,
        'photo_path':path,
        'user_name':username
    })

def show_hiking_photo(db, hp_name):
    results = db.collection(HPcol).where("hp_name", "==", hp_name).stream()
    res = []
    for row in results:
        res.append(row.to_dict())
    return res

def write_cookary(db, c_name, path, username):
    HP_ref = db.collection(COcol).document(str(uuid.uuid4()))
    HP_ref.set({
        'c_name':c_name,
        'video_path':path,
        'user_name':username
    })

def show_cookary(db, c_name):
    results = db.collection(COcol).where("c_name", "==", c_name).stream()
    res = []
    for row in results:
        res.append(row.to_dict())
    return res