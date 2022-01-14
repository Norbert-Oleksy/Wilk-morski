import discord
import os
import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse

client = discord.Client()


@client.event
async def on_ready():
    print('Zalogowano jako {0.user}'.format(client))


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
    if len(wiadomosc) == 1:
        miasto = "gdansk"
    elif len(wiadomosc) == 2:
        miasto = wiadomosc[1]
        miasto = miastoDostosowanie(miasto)
        print(miasto)
    else:
        listamiasto = wiadomosc[1::1]
        miasto = ""
        for elem in listamiasto:
            miasto = miasto + elem
        miasto = miastoDostosowanie(miasto)
        print(miasto)

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
    if len(wiadomosc) == 1:
        return "Podaj kogo szukasz."
    elif len(wiadomosc) == 2:
        kto = wiadomosc[1]
    else:
        ktodane = wiadomosc[1::1]
        kto = ' '.join(ktodane)

    kto = urllib.parse.quote(kto)

    url = "https://umg.edu.pl/node/160?p=" + kto

    return url


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$Witam'):
        await message.channel.send('Ahoj!')

    if message.content.startswith('$Bot-Info'):
        with open("README.txt", encoding='utf8') as inf:
            await message.channel.send(inf.read().rstrip())
        inf.close()

    if message.content.startswith('$Bot-Opcje'):
        with open("BotOptions.txt", encoding='utf8') as opt:
            await message.channel.send(opt.read().rstrip())
        opt.close()

    if message.content.startswith('$Pogoda'):
        if message.content.startswith('$PogodaMiasta'):
            await message.channel.send(listaMiast())
        else:
            SplitMSG = message.content.split()
            await message.channel.send(pogoda(SplitMSG))

    if message.content.startswith('$Kontakt'):
        SplitMSG = message.content.split()
        await message.channel.send(teleAdresat(SplitMSG))


client.run(os.environ['TOKEN'])
