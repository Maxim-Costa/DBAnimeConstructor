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
sql = "INSERT INTO Anime (id_anime, nom_anime, url_img_anime, vue_anime, format_id_format, statue_id_statue, nbepisode_anime, alternative_titles_en_anime, alternative_titles_ja_anime, alternative_titles_synonyms_anime, desc_anime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
val = []
for i in Dico.values():
    id_anime = int(i['id'])
    nom_anime = i['title']
    if "main_picture" in i.keys():
        url_img_anime = i['main_picture']['large']
    else:
        url_img_anime = "https://ibb.co/3YQMYh4"
    vue_anime = "Non"
    format_id_format = formatID[i['media_type']]
    statue_id_statue = statueID[i['status']]
    nbepisode_anime = int(i['num_episodes'])
    alternative_titles_en_anime = i['alternative_titles']['en']
    alternative_titles_ja_anime = i['alternative_titles']['ja']
    alternative_titles_synonyms_anime = ';'.join(
        i['alternative_titles']['synonyms'])
    desc_anime = i['synopsis']

    val.append((id_anime, nom_anime, url_img_anime, vue_anime, format_id_format, statue_id_statue, nbepisode_anime,
                alternative_titles_en_anime, alternative_titles_ja_anime, alternative_titles_synonyms_anime, desc_anime))

mycursor.executemany(sql, val)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
