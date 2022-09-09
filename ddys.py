import requests
from bs4 import BeautifulSoup

def film_list():
    r = requests.get('https://ddys.tv/')
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())
    list = (soup.find_all('h2'))
    filmlist = []
    for i in list:
        try:
            a = i.text +' ' + i.a['href']
            filmlist.append(a)
        except:
            pass
    print(filmlist)
    return filmlist
