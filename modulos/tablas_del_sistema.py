import re
import json
from typing import List, Dict
from tabulate import tabulate


def cargar_data(ruta: str) -> List[Dict]:
    """Carga datos desde un archivo JSON o CSV.

    Pre: Recibe una cadena "ruta_archivo" que representa la ruta de un archivo
         válido con extensión .json o .csv.

    Post: Devuelve una lista de diccionarios con los datos del archivo. Si ocurre
          un error, devuelve una lista vacía.

    """
    match ruta.split(".")[1]:
        case "json":
            try:
                with open(ruta, encoding="utf-8") as archivo:
                    return json.load(archivo)
            except json.JSONDecodeError:
                return []
            except (FileNotFoundError, IsADirectoryError):
                print(f"No se encontro el archivo {ruta}")
                return []
            except Exception as e:
                print(f"Error al guardar los datos en JSON: {e}")
                return []
        case "csv":
            try:
                with open(ruta, mode="r", encoding="utf-8") as archivo:
                    lineas = archivo.readlines()
                headers = lineas[0].strip().split(",")
                data = []
                for linea in lineas[1:]:
                    valores = linea.strip().split(",")
                    elementos = {
                        headers[i]: valores[i].strip('"') for i in range(len(headers))
                    }
                    data.append(elementos)
                return data
            except ValueError as e:
                print(e)
            except (FileNotFoundError, IsADirectoryError):
                print(f"No se encontro el archivo {ruta}")
            except Exception as e:
                print(f"Error al guardar los datos en CSV: {e}")
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
        print(f"No hay registros en {re.split('[/.]', ruta_archivo)[1]}.")
    else:
        print(tabulate(data, headers="keys", tablefmt="rounded_grid"))
    return None


def guardar_data(data: List[Dict], ruta: str) -> None:
    """Guarda los datos en un archivo JSON o CSV.

    Pre: Recibe una lista de diccionarios 'data' y una cadena 'ruta' que representa
         la ruta del archivo donde se guardarán los datos. La extensión del archivo
         debe ser .json o .csv.

    Post: Guarda los datos en el archivo especificado. Si ocurre un error,
          informa al usuario.

    """
    extension = ruta.split(".")[1]
    match extension:
        case "json":
            try:
                with open(ruta, "w", encoding="utf-8") as archivo:
                    json.dump(data, archivo, indent=4, ensure_ascii=False)
                print("Datos guardados exitosamente.")
            except (FileNotFoundError, IsADirectoryError):
                print(f"No se encontro el archivo {ruta}")
            except json.JSONDecodeError:
                print(f"El archivo {ruta} no es un JSON valido.")
            except Exception as e:
                print(f"Error al guardar los datos en JSON: {e}")
        case "csv":
            try:
                if not data:
                    raise ValueError(
                        f"No hay datos para guardar en el archivo CSV: {ruta}."
                    )
                headers = data[0].keys()
                with open(ruta, mode="w", encoding="utf-8") as archivo:
                    archivo.write(",".join(headers) + "\n")
                    for linea in data:
                        archivo.write(
                            ",".join(f'"{linea[header]}"' for header in headers) + "\n"
                        )
                print("Datos guardados exitosamente.")
            except ValueError as e:
                print(e)
            except (FileNotFoundError, IsADirectoryError):
                print(f"No se encontro el archivo {ruta}")
            except Exception as e:
                print(f"Error al guardar los datos en CSV: {e}")
        case _:
            print(
                f"Extensión de archivo desconocida: {extension}. No se guardaron datos."
            )
    return None


def medios_de_pago() -> None:
    """Imprime los medios de pago aceptados por el sistema.

    Pre: No recibe nada.

    Post: Retorna None.

    """
    medios = "Efectivo - Transferencia - Tarjeta de débito - Tarjetas de crédito - Cuenta DNI - Modo"
    print("=" * len(medios))
    print(medios)
    print("=" * len(medios))
    return None
