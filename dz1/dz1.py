import random
from urllib.parse import quote
import requests

headers = {"User-Agent": 'zaichik'}
spisok = []

a = requests.get("https://ru.wikipedia.org/api/rest_v1/page/random/summary", headers=headers)
data = a.json()
nazvanie = data["title"]
adres = data["content_urls"]["desktop"]["page"]
spisok.append([nazvanie, adres])

while len(spisok) < 3:
    parametri = {"action": "query", "format": "json", "prop": "links", "titles": nazvanie}
    a = requests.get("https://ru.wikipedia.org/w/api.php", params=parametri, headers=headers)
    data = a.json()
    page = list(data["query"]["pages"].values())[0]
    ssilki = page.get("links", [])
    if len(ssilki) == 0:
        break

    ran = random.choice(ssilki)["title"]
    a = requests.get("https://ru.wikipedia.org/api/rest_v1/page/summary/" + quote(ran), headers=headers)

    data = a.json()
    if "content_urls" in data:
        nazvanie = data["title"]
        adres = data["content_urls"]["desktop"]["page"]
        spisok.append([nazvanie, adres])

f = open("result.txt", "w", encoding="utf-8")

for stranica in spisok:
    f.write(stranica[0] + "\n")
    f.write(stranica[1] + "\n")

f.close()
