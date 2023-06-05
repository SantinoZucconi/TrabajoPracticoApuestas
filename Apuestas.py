import requests
import json
import csv
from passlib.hash import pbkdf2_sha256 as plib

def respuesta_api(url , header, endpoint, *nombre) -> dict:
    respuesta = requests.request("GET",url = (url + endpoint), headers = header)
    respuesta = respuesta.text
    with open(f"respuesta_{nombre[0]}.txt", "w") as archivo:
        archivo.write(respuesta)
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

def pedir_usuario() -> dict:
    mail = input("Ingrese su mail: ")

    if (validar_mail(mail) == False):
        print("Mail invalido")
        pedir_usuario()
        return 
     
    nombre     = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    usuario = ingreso_de_usuario(mail,nombre,contraseña, archivo_usuarios = "usuarios.csv")

    return usuario

def validar_mail(mail) -> bool:
    mail = mail.split("@")
    if (len(mail) == 2 and mail[1] != ""):
        return True
    else:
        return False

def ingreso_de_usuario(mail, nombre_de_usuario, contraseña, archivo_usuarios) -> dict:

    usuarios = []
    usuario_coincidente = "no encontrado"

    with open(archivo_usuarios, "r", newline = "", encoding = "utf-8-sig") as archivo:
        reader = csv.reader(archivo, delimiter = ",")
        next(reader)
        for row in reader:
            if row != []:
                usuarios.append({"id": row[0], "nombre": row[1], "contraseña": row[2], "cantidad apostada": row[3], "fecha ultima apuesta": row[4], "dinero disponible": row[5]})
    
    for i in range(len(usuarios)):
        if (usuarios[i]['id'] == mail):
            if(verificar_contraseña(contraseña, usuarios[i]['contraseña']) == True and usuarios[i]['nombre'] == nombre_de_usuario):
                usuario_coincidente = usuarios[i]
                return usuario_coincidente
            else:
                print("El usuario o la contraseña es incorrecta")
                pedir_usuario()
                return
                           
    if (usuario_coincidente == "no encontrado"):
        contraseña = plib.hash(contraseña)
        with open(archivo_usuarios, "a", newline = "", encoding = "utf-8-sig") as archivo:
            writer = csv.writer(archivo, delimiter=",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
            writer.writerow((mail,nombre_de_usuario,contraseña,0,"",0))  
        usuario_coincidente = {"id": mail, "nombre": nombre_de_usuario, "contraseña": contraseña, "cantidad apostada": 0, "fecha ultima apuesta": "", "dinero disponible": 0}

    return usuario_coincidente

def verificar_contraseña(contraseña, hash) -> bool:
    if (plib.verify(contraseña, hash) == True):
        return True
    else:
        return False


def main():

    url = "https://v3.football.api-sports.io/"
    header = {"x-rapidapi-host": "v3.football.api-sports.io",
              "x-rapidapi-key": "f0c007a556a4cabc316ce1a8afa0d95a"}
    endpoint = "standings?league=128&season=2023"
    
    respuesta = leer_archivo_respuesta_api(archivo_respuesta = "respuesta_liga_argentina.txt") #esta funcion se usa una vez hecho la request a la api, asi evitamos gastar los usos que nos da la pagina
    
    liga = respuesta['response'][0]['league']['standings'][1] #lista, cada indice es un equipo

    usuario = pedir_usuario()


    
    

                

main()

