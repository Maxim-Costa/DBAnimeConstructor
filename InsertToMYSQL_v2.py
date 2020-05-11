# -*- coding: utf-8 -*-
import mysql.connector
import json

with open("data_v2.json", "r", encoding="utf-8") as fp:
    Dico = json.load(fp)


def GetGenres():
    genre = {}
    for i in Dico.values():
        if "genres" in i.keys():
            for j in i["genres"]:
                genre[j["name"]] = int(j['id'])
    genre["unknow"] = 0
    return genre


def GetStudio():
    studio = {}
    for i in Dico.values():
        if "studios" in i.keys():
            for j in i["studios"]:
                studio[j["name"]] = int(j['id'])
    studio["unknow"] = 0
    return studio


def GetStatue():
    status = {}
    statusL = []
    for i in Dico.values():
        statusL.append(i["status"])

    for k, v in enumerate(sorted(list(set(statusL)))):
        status[v] = k
    return status


def GetMedia_type():
    Media_type = {}
    Media_typeL = []
    for i in Dico.values():
        Media_typeL.append(i["media_type"])

    for k, v in enumerate(sorted(list(set(Media_typeL)))):
        Media_type[v] = k
    return Media_type


mydb = mysql.connector.connect(
    host="YOUR-HOST",
    user="YOUR-USER",
    passwd="YOUR-PASWORD",
    database="YOUR-DATABASE"
)

formatID = GetMedia_type()
statueID = GetStatue()
stuioID = GetStudio()
genreID = GetGenres()

mycursor = mydb.cursor()
sql = "INSERT INTO relation_anime (id_anime_primary, id_anime_relation) VALUES (%s, %s)"
val = []

for i in Dico.values():
    id_anime_primary = i['id']

    if i['related_anime'] != []:
        for j in i['related_anime']:
            id_anime_relation = j['node']['id']
            val.append((id_anime_primary, id_anime_relation))

val = list(set(val))

mycursor.executemany(sql, val)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
