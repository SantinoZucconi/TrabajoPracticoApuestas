import requests
import json
import csv

def respuesta_api(url , header, endpoint) -> dict:
    respuesta = requests.request("GET",url = (url + endpoint), headers = header)
    respuesta = respuesta.text
    with open("respuesta.txt", "w") as archivo:
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

def main():
    url = "https://v3.football.api-sports.io/"
    header = {"x-rapidapi-host": "v3.football.api-sports.io",
              "x-rapidapi-key": "f0c007a556a4cabc316ce1a8afa0d95a"}
    endpoint = "leagues"
    
    respuesta = leer_archivo_respuesta_api(archivo_respuesta = "respuesta.txt")

main()

