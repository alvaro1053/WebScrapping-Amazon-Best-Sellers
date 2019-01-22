'''
Created on 22 oct. 2018

@author: alvar
'''

import urllib.request, re
import sqlite3
import os
import urllib
import PIL.Image 
import PIL.ImageTk
import tkinter as tk
from tkinter.constants import TOP
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox

def seleccionar_paginas():
    conjunto = set()
    for i in range (1,2):#coge las 2 paginas (top 100 articulos)
        p = 'https://www.amazon.es/gp/bestsellers/electronics/ref=zg_bs_electronics_home_all&pg='+str(i)
        conjunto.add(p)
    return conjunto

def procesar_pagina(d:str):
    f = urllib.request.urlopen(d)
    s = BeautifulSoup(f,"lxml")
    
    l = s.find_all("li", class_=["zg-item-immersion"])
    return l

def cargar_db():
    conn = sqlite3.connect('amazon_db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS AMAZON")
    conn.execute('''CREATE TABLE AMAZON
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       TITULO       TEXT NOT NULL,
       ENLACE          TEXT    NOT NULL,
       PUNTUACION       TEXT    ,
       PRECIO       DOUBLE,
       FOTO         TEXT NOT NULL);''')
    paginas = seleccionar_paginas()
    for pagina in paginas:
        documento = procesar_pagina(pagina)
        for e in documento:
            foto = extraer_foto(e)
            titulo = extraer_titulo(e)
            enlace = extraer_enlace(e)
            puntuacion = extraer_puntuacion(e)
            precio = extraer_precio(e)

            insertar_tupla_bd(conn, titulo, enlace, puntuacion, precio, foto)
   
    cursor = conn.execute("SELECT COUNT(*) FROM AMAZON")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " artículos")
    cerrar_bd(conn)

def insertar_tupla_bd(conn, titulo, enlace, puntuacion, precio, foto):
    conn.execute("""INSERT INTO AMAZON (TITULO, ENLACE, PUNTUACION, PRECIO, FOTO) VALUES (?,?,?,?,?)""",(titulo, enlace, puntuacion, precio, foto))
    conn.commit()

def extraer_foto(e):
    if e != None:
        return e.span.div.find_all('span')[3].a.span.div.img['src']
    else:
        return ""


def extraer_titulo(e):
    if e != None:
        return e.span.div.find_all('span')[3].a.find_all('div')[1].contents[0]
    else:
        return ""


def extraer_enlace(e):
    if e != None:
        return e.span.div.find_all('span')[3].a['href']
    else:
        return ""
   
def extraer_puntuacion(e):
    if e != None:
        try:
            if(e.span.div.find_all('span')[3].find_all('div')[2].a.i != None):  
                return e.span.div.find_all('span')[3].find_all('div')[2].a.i.span.contents[0]
        except IndexError:
            return ""
    else:
        return ""


def extraer_precio(e):
    if e != None:
        try:
            aux = e.span.div.find_all('span')[3].find_all('div')[3].a.span.span.contents[0]
            return aux.string.replace(',','.').replace('EUR ', '').strip()
        except IndexError:
            return ""
    else:
        return ""

                      
def cerrar_bd(conn):
    conn.close()
   
def mostrar_db():
    conn = sqlite3.connect('amazon_db')
    cursor = conn.execute("""SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON""")
    mostrar_cursor(cursor)
    cerrar_bd(conn)
    
def mostrar_cursor(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
        lb.insert(END, row[4])
        '''
        urllib.request.urlretrieve(row[4], 'image.jpg')
        image = PIL.Image.open('image.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(v, image = photo)
        label.image = photo
        label.pack()
        '''
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)

'''
    root = tk.Tk()
    for idx, row in enumerate(cursor):
        lb = tk.Listbox(root, width=100)
        lb.insert(END, row[0])
        lb.grid(row=idx, column = 0)


        urllib.request.urlretrieve(row[4], 'image.jpg')
        image = PIL.Image.open('image.jpg')
        photo = PIL.ImageTk.PhotoImage(image, master=root)
        #print(row[4])
        print(photo)

        label = tk.Label(root, image = photo ) 
        #label = Label(v, image = photo)
        label.image = photo
        label.grid(row = idx, column = 1)
    root.mainloop()
'''


def buscar_bd():
    v = Toplevel()
    cargar = Button(v, text="Titulo", command = cargar_titulo_bd)
    cargar.pack(side = TOP)
    fecha = Button(v, text="Puntuacion", command = cargar_puntuacion_bd)
    fecha.pack(side = TOP)
    fecha = Button(v, text="Precio", command = cargar_precio_bd)
    fecha.pack(side = TOP)
    quitar = Button(v, text = "Quitar", command = v.destroy)
    quitar.pack(side = TOP)

def cargar_titulo_bd():
    def listar_busqueda_titulo(event):
        conn = sqlite3.connect('amazon_db')
        s = "%"+en.get()+"%"
        cursor = conn.execute("""SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON WHERE TITULO LIKE ?""", (s,))
        mostrar_cursor(cursor)
        cerrar_bd(conn)

    v = Toplevel()
    lb = Label(v, text="Introduzca el articulo a buscar: ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda_titulo)
    en.pack(side = LEFT)

def cargar_puntuacion_bd():
    def listar_busqueda_puntuacion(event):
        conn = sqlite3.connect('amazon_db')
        s = "%"+en.get()+"%"
        cursor = conn.execute("""SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON WHERE PUNTUACION LIKE ?""", (s,))
        mostrar_cursor(cursor)
        cerrar_bd(conn)

    v = Toplevel()
    lb = Label(v, text="Introduzca puntuacion a buscar (0,0-5,0): ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda_puntuacion)
    en.pack(side = LEFT)

def cargar_precio_bd():
    def listar_busqueda_precio(event):
        conn = sqlite3.connect('amazon_db')
        s = "%"+en.get()+"%"
        cursor = conn.execute("""SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON WHERE PRECIO LIKE ?""", (s,))
        mostrar_cursor(cursor)
        cerrar_bd(conn)

    v = Toplevel()
    lb = Label(v, text="Introduzca precio a buscar (ej: 59,99): ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda_precio)
    en.pack(side = LEFT)


def estadisticas_bd():
    v = Toplevel()
    mejores  = Button(v, text="Articulos mejor puntuados", command = estadisticas_mejores)
    mejores.pack(side = TOP)
    baratos  = Button(v, text="Articulos mas baratos", command = estadisticas_baratos)
    baratos.pack(side = TOP)
    caros  = Button(v, text="Articulos mas caros", command = estadisticas_caros)
    caros.pack(side = TOP)


def estadisticas_mejores():
    conn = sqlite3.connect('amazon_db')
    cursor = conn.execute('SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON ORDER BY PUNTUACION DESC LIMIT 20;')
    mostrar_estadisticas(cursor)
    cerrar_bd(conn)

def estadisticas_baratos(): 
    conn = sqlite3.connect('amazon_db')
    cursor = conn.execute('SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON ORDER BY PRECIO ASC LIMIT 20;')
    mostrar_estadisticas(cursor)
    cerrar_bd(conn)

def estadisticas_caros(): 
    conn = sqlite3.connect('amazon_db')
    cursor = conn.execute('SELECT TITULO, ENLACE, PUNTUACION, PRECIO, FOTO FROM AMAZON ORDER BY PRECIO DESC LIMIT 20;')
    mostrar_estadisticas(cursor)
    cerrar_bd(conn)

def mostrar_estadisticas(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
        lb.insert(END, row[4])
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)
  
    
def ventana_principal():
    top = Tk()
    cargar = Button(top, text="Cargar", command = cargar_db)
    cargar.pack(side = LEFT)
    mostrar = Button(top, text="Mostrar", command = mostrar_db)
    mostrar.pack(side = LEFT)
    buscar = Button(top, text="Buscar", command = buscar_bd)
    buscar.pack(side = LEFT)
    estadisticas = Button(top, text="Estadisticas", command = estadisticas_bd)
    estadisticas.pack(side = LEFT)
    quitar = Button(top, text="Quitar", command = top.destroy)
    quitar.pack(side=TOP)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()
