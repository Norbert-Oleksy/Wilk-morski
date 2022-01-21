import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse

def miastoDostosowanie(miasto):
    '''
      Ma na celu dostosowanie nazwy miasta.
      Zamienia wszystkie litery na małe.
      Zastępuje litery z znakiem diakrytycznym.
    '''
    miasto = miasto.lower()
    miasto = miasto.replace("ę", "e")
    miasto = miasto.replace("ó", "o")
    miasto = miasto.replace("ą", "a")
    miasto = miasto.replace("ś", "s")
    miasto = miasto.replace("ł", "l")
    miasto = miasto.replace("ż", "z")
    miasto = miasto.replace("ź", "z")
    miasto = miasto.replace("ć", "c")
    miasto = miasto.replace("ń", "n")
    return miasto


def pogoda(wiadomosc):
    '''
      Pobiera z danepubliczne.imgw.pl infromacje o pogodzie.

      Dostosowanie nazwy miasta do url
    '''
    if len(wiadomosc) == 0:
        miasto = "gdansk"
    elif len(wiadomosc) == 1:
        miasto = wiadomosc[0]
        miasto = miastoDostosowanie(miasto)
    else:
        listamiasto = wiadomosc[0::1]
        miasto = ""
        for elem in listamiasto:
            miasto = miasto + elem
        miasto = miastoDostosowanie(miasto)

    #Pobranie danych xml
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}/format/xml"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    dane = soup.find_all(True)
    dane = dane[4::1]

    #Przygotowanie odpowiedzi zwrotnej
    wynik = ""
    for dan in dane:
        wynik = wynik + dan.name.replace("_", " ") + ": " + dan.text + "\n"
    return wynik


def listaMiast():
    #Zwraca listę dostępnych miast z danepubliczne.imgw
    lista = ""
    url = "https://danepubliczne.imgw.pl/api/data/synop/format/xml"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    dane = soup.find_all("stacja")
    for dan in dane:
        lista = lista + dan.text + " / "
    return lista


def teleAdresat(wiadomosc):
    if len(wiadomosc) == 0:
        return "Podaj kogo szukasz."
    elif len(wiadomosc) == 1:
        kto = wiadomosc[0]
    else:
        ktodane = wiadomosc[0::1]
        kto = ' '.join(ktodane)

    kto = urllib.parse.quote(kto)

    url = "https://umg.edu.pl/node/160?p=" + kto

    return url