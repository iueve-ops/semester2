import random
from urllib.parse import unquote, quote

import requests
import matplotlib.pyplot as plt

headers = {"User-Agent": "hw2"}
target = "Россия"
ops = 10
max_iter = 40
rezultati = []
start = []

for i in range(ops):
    print("Опыт", i + 1)
    a = requests.get("https://ru.wikipedia.org/wiki/Special:Random", headers=headers, allow_redirects=True)
    nazvanie = unquote(a.url.split("/wiki/")[-1]).replace("_", " ")

    start.append(nazvanie)
    iters = 0

    while nazvanie != target and iters < max_iter:
        a = requests.get("https://ru.wikipedia.org/wiki/" + quote(nazvanie.replace(" ", "_"), safe=""), headers=headers)
        text = a.text
        kuski = text.split('href="/wiki/')[1:] + text.split('href="//ru.wikipedia.org/wiki/')[1:]
        ssilki = []

        for kusok in kuski:
            ssilka = kusok.split('"')[0]

            if ":" not in ssilka and "#" not in ssilka and len(ssilka) > 0:
                ssilka = unquote(ssilka).replace("_", " ")

                if ":" not in ssilka and "#" not in ssilka and "?" not in ssilka and ssilka not in ssilki:
                    ssilki.append(ssilka)

        if len(ssilki) == 0:
            break

        ran = random.choice(ssilki)

        for ssilka in ssilki:
            if ssilka == target:
                ran = target

        nazvanie = ran
        iters = iters + 1

    if nazvanie == target:
        rezultati.append(iters)
    else:
        rezultati.append(max_iter + 1)

f = open("result.txt", "w", encoding="utf-8")
f.write("Цель: " + target + "\n\n")

for i in range(len(rezultati)):
    f.write("Опыт " + str(i + 1) + "\n")
    f.write("Стартовая статья: " + start[i] + "\n")

    if rezultati[i] <= max_iter:
        f.write("Дошли за шагов: " + str(rezultati[i]) + "\n")
    else:
        f.write("Не дошли за " + str(max_iter) + " шагов\n")

    f.write("\n")

f.close()

znacheniya = []
podpisi = []

for i in range(max_iter + 2):
    kolvo = rezultati.count(i)

    if kolvo > 0:
        if i == max_iter + 1:
            podpis = "больше " + str(max_iter)
        else:
            podpis = str(i)

        podpisi.append(podpis)
        znacheniya.append(kolvo)

plt.bar(podpisi, znacheniya)
plt.title("Сколько шагов до статьи " + target)
plt.xlabel("Количество шагов")
plt.ylabel("Количество опытов")
plt.savefig("histogram.png")

print("Готово")
