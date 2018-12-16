import sqlite3

from ..model.Area import Area
from ..model.Chat import Chat
from ..model.Group import Group
from ..model.User import User

import os

DB_PATH = 'db/mreza.db'  # can do abs path too!
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

INIT_SCRIPT = """
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `Chat` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`idGrupe`	INTEGER,
	`idKorisnika`	INTEGER,
	`tekst`	TEXT,
	`kategorija`	TEXT,
	FOREIGN KEY(`idGrupe`) REFERENCES `Grupa`(`id`),
	FOREIGN KEY(`idKorisnika`) REFERENCES `Korisnik`(`id`)
);

CREATE TABLE IF NOT EXISTS `Grupa` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`idOblasti`	INTEGER,
	`aktivnost`	INTEGER,
	FOREIGN KEY(`idOblasti`) REFERENCES `Oblast`(`id`)
);

CREATE TABLE IF NOT EXISTS `Korisnik` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ime`	TEXT,
	`prezime`	TEXT,
	`godinaRodjenja`	TEXT,
	`sifra`	TEXT,
	`deskripcija`	TEXT,
	`idGrupe`	INTEGER,
	FOREIGN KEY(`idGrupe`) REFERENCES `idGrupe`(`id`)
);

CREATE TABLE IF NOT EXISTS `Oblast` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ime`	TEXT
);

COMMIT;
"""


def _connect():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return conn


conn = _connect()
c = conn.cursor()
c.executescript(INIT_SCRIPT)
conn.commit()
conn.close()

def create_user(data):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    user_query = """INSERT INTO Korisnik (ime, prezime, godinaRodjenja, sifra, deskripcija) VALUES (?,?,?,?,?)"""
    c.execute(user_query, (data['name'], data['lastName'], data['year'], data['password'], data['deskripcija']))
    user_id = c.lastrowid

    new_user = User(user_id, data['name'], data['lastName'], data['year'], data['deskripcija'], -1)

    conn.commit()
    c.close()
    conn.close()
    return new_user


def auth_user(data):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, ime, prezime, godinaRodjenja, deskripcija, idGrupe FROM Korisnik WHERE ime=? AND sifra=? AND prezime=?"""
    c.execute(query, (data['name'], data['password'], data['lastName']))
    t = c.fetchone()

    if t is None:
        return -1

    user = User(id=t[0], name=t[1], lastName=t[2], year=t[3], link=t[4], idGroup=t[5])

    if user.idGroup is None:
        user.idGroup = -1

    conn.commit()
    c.close()
    conn.close()

    return user


def get_all_areas():
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, ime FROM Oblast"""
    c.execute(query)
    result_set = c.fetchall()

    areas = []

    for t in result_set:
        created_area = Area(id=t[0], areaName=t[1])
        areas.append(created_area)

    conn.commit()
    c.close()
    conn.close()

    return areas


def get_group(user_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    group_query = """SELECT idGrupe FROM Korisnik WHERE id = ?"""
    c.execute(group_query, (user_id,))
    g = c.fetchone()

    query = """SELECT idOblasti FROM Grupa WHERE id = ?"""
    c.execute(query, (g[0],))
    t = c.fetchone()

    area_query = """SELECT ime FROM Oblast WHERE id=?"""
    c.execute(area_query, (t[0],))
    a = c.fetchone()

    group = Group(id=g[0], areaName=a[0], areaId=t[0])

    user_query = """SELECT id, ime, prezime, godinaRodjenja, deskripcija FROM Korisnik
        WHERE idGrupe = ?"""
    c.execute(user_query, (g[0],))
    users = c.fetchall()

    for u in users:
        user = User(id=u[0], name=u[1], lastName=u[2], year=u[3], description=u[4], idGroup=g[0])
        group.add_user(user)

    conn.commit()
    c.close()
    conn.close()

    return group

def create_group(area_id, user_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    user_query = """INSERT INTO Grupa (idOblasti, aktivnost) VALUES (?,?)"""
    c.execute(user_query, (area_id, 100))
    group_id = c.lastrowid

    user_query = """UPDATE Korisnik SET IdGrupe = ? WHERE id=?"""
    c.execute(user_query, (group_id, user_id,))

    conn.commit()
    c.close()
    conn.close()
    return get_group(user_id)


def join_group(group_id, user_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    user_query = """UPDATE Korisnik SET IdGrupe = ? WHERE id=?"""
    c.execute(user_query, (group_id, user_id,))

    conn.commit()
    c.close()
    conn.close()
    return get_group(user_id)

def create_area(data):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    query = """INSERT INTO Oblast (ime) VALUES (?)"""
    c.execute(query, (data['name'],))
    area_id = c.lastrowid

    new_area = Area(area_id, data['name'])

    conn.commit()
    c.close()
    conn.close()
    return new_area

def create_chat(user_id, data):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    group_query = """SELECT idGrupe FROM Korisnik WHERE id = ?"""
    c.execute(group_query, (user_id,))
    g = c.fetchone()

    chat_query = """INSERT INTO Chat (tekst, kategorija, idGrupe, idKorisnika) VALUES (?, ?, ?, ?)"""
    c.execute(chat_query, (data['text'], data['category'], g[0], user_id))

    new_chat = Chat(textC=data['text'], category=data['category'], idGroup=g[0], idUser=user_id)

    conn.commit()
    c.close()
    conn.close()
    return new_chat

def get_all_chat():
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    all_chat_query = """SELECT id, idGrupe, idKorisnika, tekst, kategorija FROM Chat"""
    c.execute(all_chat_query)
    result_set = c.fetchall()

    chats = []

    for t in result_set:
        created_chat = Chat(idGroup=t[1], idUser=t[2], textC=t[3], category=t[4])
        chats.append(created_chat)

    conn.commit()
    c.close()
    conn.close()

    return chats


# def get_team(team_uuid):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#     query = """SELECT id, name, description, photo_url, team_uuid FROM team WHERE team_uuid=?"""
#     c.execute(query, (team_uuid,))
#     t = c.fetchone()
#
#     if t is None:
#         return None
#
#     created_team = Team(id=t[0], name=t[1], description=t[2], photo_url=t[3], team_uuid=t[4])
#
#     member_query = """SELECT id, first_name, last_name, email, phone_number, school, city FROM
#     team_member WHERE team_id=?"""
#     c.execute(member_query, (created_team.id,))
#     members = c.fetchall()
#
#     for m in members:
#         created_member = TeamMember(id=m[0], first_name=m[1], last_name=m[2], email=m[3], phone_number=m[4],
#                                     school=m[5], city=m[6], team=created_team)
#         created_team.add_member(created_member)
#
#     conn.commit()
#     c.close()
#     conn.close()
#
#     return created_team
#
#
# def create_team(data):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#
#     error_check = check_team(data)
#     if error_check != 4:
#         return error_check
#
#     team_query = """INSERT INTO team (name, description, photo_url, team_uuid) VALUES (?,?,?,?)"""
#     team_uuid = uuid.uuid4()
#     c.execute(team_query, (data['name'], data['description'], data['photo_url'], str(team_uuid)))
#     team_id = c.lastrowid
#     data['id'] = team_id
#     data['team_uuid'] = team_uuid
#
#     for m in data['team_members']:
#         member_query = """INSERT INTO team_member (first_name, last_name, email, phone_number, school, city, team_id)
#         VALUES (?,?,?,?,?,?,?)"""
#         c.execute(member_query,
#                   (m['first_name'], m['last_name'], m['email'], m['phone_number'], m['school'], m['city'], team_id))
#         m['id'] = c.lastrowid
#
#     conn.commit()
#     c.close()
#     conn.close()
#     return data
#
#
# def update_team(data, team_uuid):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#
#     query = """SELECT id FROM team WHERE team_uuid=?"""
#     c.execute(query, (team_uuid,))
#     t = c.fetchone()
#
#     if t is None:
#         return None
#
#     team_id = t[0]
#
#     error_check = check_team(data)
#     if error_check != 4:
#         return error_check
#
#     delete_all_team_members(team_id)
#
#     team_query = """UPDATE team SET name=?, description=?, photo_url=? WHERE team_uuid=?"""
#
#     c.execute(team_query, (data['name'], data['description'], data['photo_url'], team_uuid))
#
#     for m in data['team_members']:
#         member_query = """INSERT INTO team_member (first_name, last_name, email, phone_number, school, city, team_id)
#         VALUES (?,?,?,?,?,?,?)"""
#         c.execute(member_query,
#                   (m['first_name'], m['last_name'], m['email'], m['phone_number'], m['school'], m['city'], team_id))
#         m['id'] = c.lastrowid
#
#     conn.commit()
#     c.close()
#     conn.close()
#     return data
#
#
# def delete_team(team_uuid):
#     conn = _connect()
#
#     with conn:
#         team_query = """DELETE FROM team WHERE team_uuid=?"""
#         status = conn.execute(team_query, (team_uuid,))
#         success = False
#         if status.rowcount == 1:
#             success = True
#
#     return success
#
#
# def delete_all_team_members(team_id):
#     conn = _connect()
#     try:
#         with conn:
#             team_query = """DELETE FROM team_member WHERE team_id=?"""
#             status = conn.execute(team_query, (team_id,))
#             success = False
#             if status.rowcount > 0:
#                 success = True
#
#             return success
#     except sqlite3.Error:
#         return False
#
#
# def check_team(data):
#     if 'name' not in data or 'description' not in data or 'photo_url' not in data:
#         return -1  # error no field
#
#     if data["name"] == '' or data["description"] == '' or data["photo_url"] == '':
#         return -1  # error field empty
#
#     member_count = 0
#     for m in data['team_members']:
#         member_count += 1
#         member_faulty = check_team_member(m)
#         if member_faulty:
#             return 2, member_count  # member error
#
#     if member_count < 3 or member_count > 4:
#         return 3, member_count  # error wrong member count
#     return 4  # no error
#
#
# def check_team_member(m):
#     if 'first_name' not in m or 'last_name' not in m or 'email' not in m or \
#             'phone_number' not in m or 'school' not in m or 'city' not in m:
#         return True  # error no member field
#
#     if m['first_name'] == '' or m['last_name'] == '' or m['email'] == '' or \
#             m['phone_number'] == '' or m['school'] == '' or m['city'] == '':
#         return True  # error member field empty
#     return False
#
#
# def get_team_member(team_member_id):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#
#     member_query = """SELECT id, first_name, last_name, email, phone_number, school, city, team_id FROM
#     team_member WHERE id=?"""
#     c.execute(member_query, (team_member_id,))
#     m = c.fetchone()
#
#     if m is None:
#         return None
#
#     dummy_team = Team(id=m[7], name="dummy", description="dummy", photo_url="dummy", team_uuid="dummy")
#     created_member = TeamMember(id=m[0], first_name=m[1], last_name=m[2], email=m[3], phone_number=m[4],
#                                 school=m[5], city=m[6], team=dummy_team)
#
#     conn.commit()
#     c.close()
#     conn.close()
#
#     return created_member
#
#
# def update_team_member(m, team_member_id):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#
#     member_faulty = check_team_member(m)
#     if member_faulty:
#         return 2  # member error
#
#     member_update = """UPDATE team_member SET first_name = ?, last_name = ?, email = ?,
#         phone_number = ?, school = ?, city= ? WHERE id = ?"""
#     c.execute(member_update, (m['first_name'], m['last_name'], m['email'],
#                               m['phone_number'], m['school'], m['city'], team_member_id))
#     if c.rowcount < 1:
#         return None
#
#     conn.commit()
#     c.close()
#     conn.close()
#     return m
#
#
# def delete_team_member(team_member_id):
#     conn = _connect()  # todo use connection as context manager
#     c = conn.cursor()
#
#     member_query = """SELECT team_id FROM team_member WHERE id=?"""
#     c.execute(member_query, (team_member_id,))
#     team = c.fetchone()
#
#     if team is None:
#         return None
#
#     team_id = team[0]
#
#     count_members = """SELECT count(*) FROM team_member WHERE team_id = ?;"""
#     c.execute(count_members, (team_id,))
#     team_length = c.fetchone()
#
#     if team_length[0] < 4:
#         return 2  # too little members
#
#     with conn:
#         team_query = """DELETE FROM team_member WHERE id=?"""
#         status = conn.execute(team_query, (team_member_id,))
#         success = False
#         if status.rowcount == 1:
#             success = True
#
#     return success
