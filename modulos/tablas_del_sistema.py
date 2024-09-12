import re
from tabulate import tabulate


def cargar_data(ruta_archivo: str) -> dict[str]:
    """Cargar informacion de un archivo JSON."""
    try:
        with open(ruta_archivo, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: no se encontro: {ruta_archivo}.")
        return []
    except json.JSONDecodeError as e:
        print("Error: {e}")
        return []


def imprimir_tabla(ruta_archivo: str) -> None:
    """ Imprime la tabla especificada
    Pre: Recibe la ruta del archivo como string.
    
    Post: Usando tabulate imprime la tabla generada a partir del archivo json.
    """
    data = cargar_data(ruta_archivo)
    if not data:
        print(f"No hay registros de {re.split("[/.]",ruta_archivo)[1]}")
    print(tabulate(data, headers="keys", tablefmt="rounded_grid"))
