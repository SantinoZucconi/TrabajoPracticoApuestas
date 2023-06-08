import requests
import json
import csv
from passlib.hash import pbkdf2_sha256 as plib
import os
import random
import colored
from colored import stylize

def respuesta_api(endpoint) -> dict:
    url    = "https://v3.football.api-sports.io/"
    header = {"x-rapidapi-host": "v3.football.api-sports.io",
              "x-rapidapi-key": "f0c007a556a4cabc316ce1a8afa0d95a"}
    respuesta = requests.request("GET",url = (url + endpoint), headers = header)
    respuesta = respuesta.text
    respuesta = json.loads(respuesta)
    return respuesta

def leer_archivo_respuesta_api(archivo_respuesta) -> dict:
    with open(archivo_respuesta, "r") as archivo:
        datos = ""
        for linea in archivo:
            linea = linea.rstrip("\n")
            datos += linea
    datos = json.loads(datos)
    return datos

def validar_mail(mail) -> bool:
    mail = mail.split("@")
    if (len(mail) == 2 and mail[1] != ""):
        return True
    else:
        return False

def leer_usuarios(archivo_usuarios):
    usuarios = []
    with open(archivo_usuarios, "r", newline = "", encoding = "utf-8-sig") as archivo:
        reader = csv.reader(archivo, delimiter = ",")
        next(reader)
        for row in reader:
            if row != []:
                usuarios.append({"id": row[0], "nombre": row[1], "contraseña": row[2], "cantidad apostada": float(row[3]), "fecha ultima apuesta": row[4], "dinero disponible": float(row[5])})
    return usuarios

def actualizar_tabla_usuarios(datos_actualizados):
    with open("usuarios.csv","w", newline="",encoding="utf-8-sig") as archivo:
        writer = csv.writer(archivo, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(("ID","Nombre de usuario","Contraseña","Cantidad apostada","Fecha de la ultima apuesta","Cantidad de dinero disponible"))
        for dato in datos_actualizados:
            writer.writerow((dato['id'],dato['nombre'],dato['contraseña'],dato['cantidad apostada'],dato['fecha ultima apuesta'],dato['dinero disponible']))

def ingreso_de_usuario() -> dict:

    mail = input("Ingrese su mail: ")
    if (validar_mail(mail) == False):
        print("Mail invalido")
        ingreso_de_usuario()
        return  
    nombre_de_usuario   = input("Ingrese su nombre de usuario: ")
    contraseña          = input("Ingrese su contraseña: ")
    usuarios            = leer_usuarios(archivo_usuarios = "usuarios.csv")
    
    for i in range(len(usuarios)):
        if (usuarios[i]['id'] == mail):
            if(verificar_contraseña(contraseña, usuarios[i]['contraseña']) == True and usuarios[i]['nombre'] == nombre_de_usuario):
                usuario_coincidente = usuarios[i]
                return usuario_coincidente
            elif (verificar_contraseña(contraseña, usuarios[i]['contraseña']) != True or usuarios[i]['nombre'] != nombre_de_usuario):
                print("El usuario o la contraseña es incorrecta")
                return 
                           
    contraseña = plib.hash(contraseña)
    with open("usuarios.csv", "a", newline = "", encoding = "utf-8-sig") as archivo:
        writer = csv.writer(archivo, delimiter=",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        writer.writerow((mail,nombre_de_usuario,contraseña,0,"",0))  
    usuario_coincidente = {"id": mail, "nombre": nombre_de_usuario, "contraseña": contraseña, "cantidad apostada": 0, "fecha ultima apuesta": "", "dinero disponible": 0}

    return usuario_coincidente

def verificar_contraseña(contraseña, hash) -> bool:
    if (plib.verify(contraseña, hash) == True):
        return True
    else:
        return False

def imprimir_menu():
    os.system("cls")
    print(f"Bienvenido a {stylize('Jugársela', (colored.fg('green') + colored.attr('underlined')))}!\n")
    print("a. Mostrar plantel de un equipo")
    print("b. Mostrar tabla de posiciones")
    print("c. Mostrar informacion del escudo y estadio de un equipo")
    print("d. Mostrar gráfico de goles por minuto de un equipo")
    print("e. Cargar dinero")
    print("f. Mostrar usuario que más dinero apostó")
    print("g. Mostrar usuario que más veces ganó")
    print("h. Apostar\n")
    return

def verificar_opciones(input) -> bool:
    opciones = ['a','b','c','d','e','f','g','h']
    if input not in opciones:
        return False
    else:
        return True

def mostrar_plantel():
    preguntar     = input("Ingrese el nombre del equipo: ").lower()
    api           = respuesta_api("standings?league=128&season=2023")
    liga          = api['response'][0]['league']['standings'][1]
    equipo_mas_id = []
    jugadores     = []
    for i in range(len(liga)):
        equipo_mas_id.append({"nombre": api['response'][0]['league']['standings'][1][i]['team']['name'].lower(), "id": api['response'][0]['league']['standings'][1][i]['team']['id']})
    
    for i in range(len(equipo_mas_id)):
        if (preguntar in equipo_mas_id[i]["nombre"]):
            api_equipo = respuesta_api(f"/players/squads?team={equipo_mas_id[i]['id']}")
            jugadores = api_equipo['response'][0]['players']
    
    if(jugadores != []):
        for i in range(len(jugadores)):
            print(f"{i+1}. {jugadores[i]['name']}")
    else:
        print("Nombre de equipo inválido")
        mostrar_plantel()
    return

def mostrar_tabla_posiciones():
    temporadas = [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    preguntar  = int(input("Ingrese la temporada: "))
    while (preguntar not in temporadas):
        print("Temporada no disponible")
        preguntar = int(input(f"Ingrese la temporada: \n"))
    respuesta = respuesta_api(f"standings?league=128&season={preguntar}",f"temporada_{preguntar}")
    temporada = respuesta['response'][0]['league']['standings'][1]
    for i in range(len(temporada)):
        print(f"{i+1}. {temporada[i]['team']['name']}")
    print("")
    return

def mostar_info_equipo():
    preguntar     = input("Ingrese el nombre del equipo: ").lower()
    api           = respuesta_api("standings?league=128&season=2023")
    liga          = api['response'][0]['league']['standings'][1]
    equipo_mas_id = []
    jugadores     = []
    for i in range(len(liga)):
        equipo_mas_id.append({"nombre": api['response'][0]['league']['standings'][1][i]['team']['name'].lower(), "id": api['response'][0]['league']['standings'][1][i]['team']['id']})
    
    for i in range(len(equipo_mas_id)):
        if (preguntar in equipo_mas_id[i]["nombre"]):
            api_equipo = respuesta_api(f"/teams?id={equipo_mas_id[i]['id']}")
            equipo = api_equipo['response'][0]['team']
            estadio = api_equipo['response'][0]['venue']
   
    print("Equipo: ")
    for i in equipo.items():
        print(i)
    print("")
    print("Estadio: ")
    for i in estadio.items():
        print(i)    
    return

def mostrar_grafico():
    return

def ingresar_dinero(usuario):
    bd_usuarios = leer_usuarios(archivo_usuarios = "usuarios.csv")
    monto       = float(input("Ingrese el monto a depositar: "))   

    bd_usuarios.remove(usuario)
    usuario['dinero disponible'] += monto
    bd_usuarios.append(usuario)

    actualizar_tabla_usuarios(bd_usuarios)
    return

def mostrar_usuario_mas_dinero_aposto():
    usuarios = leer_usuarios(archivo_usuarios = "usuarios.csv")
    max_apostador = [usuarios[0]]
    for i in range(len(usuarios)):
        if (usuarios[i]['cantidad apostada'] > max_apostador[0]['cantidad apostada']):
            max_apostador = [usuarios[i]]
        elif (usuarios[i]['cantidad apostada'] == max_apostador[0]['cantidad apostada']):
            max_apostador.append(usuarios[i])
    
    if (len(max_apostador) == 1):
        print(f"El usuario que más dinero apostó fue {max_apostador[0]['nombre']}")
    else:
        print(f"Los usuarios que más dinero apostaron fueron:")
        for i in range(len(max_apostador)):
            print(max_apostador[i]['nombre'])

    return

def mostar_usuario_mas_veces_gano():
    return

def apostar(usuario):
    fixtures = respuesta_api("/fixtures?league=128&season=2023")['response']
    fixtures_equipo = []
    pregunta = input("Ingrese un equipo: ").capitalize()
    
    for i in range(len(fixtures)):
        local = fixtures[i]['teams']['home']['name']
        visitante = fixtures[i]['teams']['away']['name']
        fecha = fixtures[i]['fixture']['date'].split("T")[0].replace("-","/")
        if(pregunta in local or pregunta in visitante):
            print(f"{local}(L) vs. {visitante}(V) - fecha: {fecha}")
            fixtures_equipo.append({"local": local,"visitante": visitante,"fecha": fecha})
    pregunta_fecha = input("Ingrese la fecha deseada (YYYY/MM/DD): ")

    for i in range(len(fixtures_equipo)):
        if(pregunta_fecha == fixtures_equipo[i]['fecha']):
            print(fixtures_equipo[i])
            apuesta = input("Ingrese su apuesta (L/E/V): ").upper()
            while apuesta not in ["L","E","V"]:
                apuesta = input("Ingrese su apuesta (L/E/V): ").upper()
            monto = float(input("Ingrese su monto: "))
            while (monto > usuario['dinero disponible']):
                print(f"Saldo insuficiente.(Saldo: {usuario['dinero disponible']}$)")
                monto = float(input("Ingrese su monto: "))
            resultado = random.randrange(1,4)
            if resultado == 1:
                resultado = "L"
            if resultado == 2:
                resultado = "E"
            if resultado == 3:
                resultado = "V"
            if (resultado == apuesta):
                multiplicador = random.randrange(2,5)
                monto = monto*multiplicador
            else:
                multiplicador = random.randrange(2,5)/10
                monto = monto*multiplicador
 
    return

def main():
    usuario = ingreso_de_usuario()
    while (usuario == None):
        usuario = ingreso_de_usuario()
    
    imprimir_menu()

    seleccionar_opcion = input("Seleccionar una opcion: ")
    while (verificar_opciones(seleccionar_opcion) == False):
        seleccionar_opcion = input("Seleccionar una opcion: ")
    if(seleccionar_opcion == 'a'):
        mostrar_plantel()
    if(seleccionar_opcion == 'b'):
        mostrar_tabla_posiciones()
    if(seleccionar_opcion == 'c'):
        mostar_info_equipo()
    if(seleccionar_opcion == 'd'):
        mostrar_grafico()
    if(seleccionar_opcion == 'e'):
        ingresar_dinero(usuario)
    if(seleccionar_opcion == 'f'):
        mostrar_usuario_mas_dinero_aposto()
    if(seleccionar_opcion == 'g'):
        mostar_usuario_mas_veces_gano()
    if(seleccionar_opcion == 'h'):
        apostar(usuario)
             
main()

