from bs4 import BeautifulSoup
import urllib.request, re
from tkinter import *
from tkinter import messagebox
import sqlite3


fichero = urllib.request.urlopen("https://www.amazon.es/gp/bestsellers/electronics/ref=zg_bs_electronics_home_all")
documento = BeautifulSoup(fichero, 'lxml')
l = documento.find_all("li", class_=["zg-item-immersion"])

'''
#extraer titulo
for e in l:
    if e != None:
        print(e.span.div.find_all('span')[3].a.find_all('div')[1].contents[0])
    else:
        print("No se ha encontrado nada")


#extraer enlace
for e in l:
    if e != None:
        print(e.span.div.find_all('span')[3].a['href'])
    else:
        print("No se ha encontrado nada")
'''
#extraer puntuacion
for e in l:
    if e != None:
        try:
            if(e.span.div.find_all('span')[3].find_all('div')[2].a.i != None):  
                print(e.span.div.find_all('span')[3].find_all('div')[2].a.i.span.contents[0])
        except IndexError:
            print("No tiene precio")
    else:
        print("No se ha encontrado nada")
'''
#extraer precio
for e in l:
    if e != None:
        try:
            print(e.span.div.find_all('span')[3].find_all('div')[3].a.span.span.contents[0])
        except IndexError:
            print("No tiene precio")
    else:
        print("No se ha encontrado nada")
'''