import requests
import json


def animeRequestAPI(id):
    url = f"https://api.myanimelist.net/v2/anime/{id}"
    querystring = {"fields": [
        "alternative_titles,media_type,num_episodes,status,genres,synopsis,authors{first_name,last_name},studios,serialization,related_anime,related_manga%27="]}
    headers = {
        'Host': "api.myanimelist.net",
        'authorization': "Bearer MY-TOKEN-MYANIMELIST",
        'user-agent': "okhttp/4.3.1",
        'cache-control': "no-cache",
        'Postman-Token': "f8c59809-2fe3-4084-934d-629b2d7d3d81"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return json.loads(response.text.encode('utf8'))
    else:
        return None


for j in range(0, 50000):
    if not j % 100:
        print(j, end=" ")
    anime = animeRequestAPI(j)
    if anime != None:
        with open('./data.json', 'a', encoding="utf-8") as outfile:
            json.dump(anime, outfile, sort_keys=True, indent=4)
            outfile.write(',')
