import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
provinces = {1: "Вінницька", 13: "Миколаївська", 2: "Волинська", 14: "Одеська", 3: "Дніпропетровська", 15: "Полтавська",
             4: "Донецька", 16: "Рівенська", 5: "Житомирська", 17: 'Сумська', 6: "Закарпатська", 18: "Тернопільська",
             7: "Запорізька", 19: "Харківська",
             8: "Івано-Франківська", 20: "Херсонська", 9: "Київська", 21: "Хмельницька", 10: "Кіровоградська",
             22: "Черкаська", 11: "Луганська", 23: "Чернівецька",
             12: "Львівська", 24: "Чернігівська", 25: "Республіка Крим"}


get_url = lambda url : str(BeautifulSoup(requests.get(url).content.decode("utf8"),'html.parser').find('pre').contents[0])

def datafile(oblast, when):
    parse_from,parse_to = when
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1={}&year2={}&type=Mean".format(
            oblast, parse_from, parse_to)

    resp = get_url(url)

    filename = oblast + "_" + 'Mean' + "_" + parse_from + "-" + parse_to + '.txt'
    open(filename, 'wb').write(str.encode(resp))
    print(filename, " created.")
    return filename


def choose_province():
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])
    oblast = input("Какую область ищем?: ")
    from_to = input('С какого по какой год ищем?: ').split()
    print("Качаем")
    return datafile(oblast, from_to)


def prepare_df(file):
    raw = open(file, 'r')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()
    replace = lambda dat: str(re.sub(r',\s\s|\s\s|\s|,\s', ',', dat)[:-1]).split(',')
    data = list(map(replace,data))
    df = pd.DataFrame(data, columns=headers)

    return df

filename = choose_province()
df = prepare_df(filename)

print(df)
print(df.VHI.min())
print(df.VHI.max())



