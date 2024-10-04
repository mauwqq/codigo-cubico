import re
import json
from typing import List, Dict
from tabulate import tabulate


def cargar_data(ruta_archivo: str) -> List[Dict]:
    """Carga datos desde un archivo JSON o CSV.

    Pre: Recibe una cadena "ruta_archivo" que representa la ruta de un archivo
         válido con extensión .json o .csv.

    Post: Devuelve una lista de diccionarios con los datos del archivo. Si ocurre
          un error, devuelve una lista vacía.

    """
    match ruta_archivo.split(".")[1]:
        case "json":
            try:
                with open(ruta_archivo, encoding="utf-8") as archivo:
                    return json.load(archivo)
            except json.JSONDecodeError:
                return []
            except FileNotFoundError:
                print(f"Error: no se encontro: {ruta_archivo}.")
                return []
        case "csv":
            try:
                with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                    lineas = archivo.readlines()
                headers = lineas[0].strip().split(',')
                data = []
                for linea in lineas[1:]:
                    valores = linea.strip().split(',')
                    elementos = {headers[i]: valores[i].strip('"') for i in range(len(headers))}
                    data.append(elementos)
                return data
            except FileNotFoundError:
                print(f"No se encontro: {ruta_archivo}")
        case _:
            print("La extension del archivo es desconocida.")


def imprimir_tabla(ruta_archivo: str) -> None:
    """Imprime la tabla especificada.

    Pre: Recibe la ruta del archivo como string.

    Post: Usando tabulate, imprime la tabla generada a partir del archivo JSON
          o CSV. Si no hay registros, informa al usuario.

    """
    data = cargar_data(ruta_archivo)
    if not data:
        print(f"No hay registros de {re.split("[/.]",ruta_archivo)[1]}.")
    print(tabulate(data, headers="keys", tablefmt="rounded_grid"))


def escribir_cambios(data: List[Dict], ruta: str) -> None:
    pass