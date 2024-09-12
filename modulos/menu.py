"""Modulo para imprimir el menu del gestor."""

import json
import os


def cargar_configuracion(ruta_archivo: str) -> dict[dict]:
    """Es mejor especificar el encoding porque usando el del sistema
    puede causar problemas de compatibilidad. UTF-8 es un standard.
    """
    with open(ruta_archivo, encoding="utf-8") as archivo:
        return json.load(archivo)


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pedir_numero(opciones: dict[dict]) -> int:
    while True:
        try:
            n = int(input("Seleccione una opción: "))
            if str(n) in opciones:
                return n
            print("El número ingresado no corresponde a ninguna opción.")
        except ValueError:
            print("Debe ingresar un número.")


def mostrar_menu(nombre_menu: str, config: dict[dict]) -> int:
    clear()
    opciones = config[nombre_menu]
    for clave, valor in opciones.items():
        print(f"{clave}- {valor}.")
    op = pedir_numero(opciones)
    return op


def menu_principal(config: dict[dict]) -> None:
    op = mostrar_menu("menu_principal", config)
    match op:
        case 1:
            menu_tablero(config)
        case 2:
            menu_reservas(config)
        case 3:
            menu_consumo_frigobar(config)
        case 4:
            menu_facturacion(config)
        case 5:
            menu_tablas_del_sistema(config)
        case 0:
            print("Saliendo...")
        case _:
            print("Opción inválida. Regresando al menú principal.")
            menu_principal(config)
    return None


def menu_tablero(config: dict[dict]) -> None:
    op = mostrar_menu("menu_tablero", config)
    match op:
        case 1:
            pass
        case 0:
            menu_principal(config)
        case _:
            print("Opción inválida. Regresando al menú de Tablero.")
            menu_tablero(config)
    return None


def menu_reservas(config: dict[dict]) -> None:
    op = mostrar_menu("menu_reservas", config)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 0:
            menu_principal(config)
        case _:
            print("Opción inválida. Regresando al menú de Reservas.")
            menu_reservas(config)
    return None


def menu_consumo_frigobar(config: dict[dict]) -> None:
    op = mostrar_menu("menu_consumo_frigobar", config)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 0:
            menu_principal(config)
        case _:
            print("Opción inválida. Regresando al menú de Consumo de Frigobar.")
            menu_consumo_frigobar(config)
    return None


def menu_facturacion(config: dict[dict]) -> None:
    op = mostrar_menu("menu_facturacion", config)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 0:
            menu_principal(config)
        case _:
            print("Opción inválida. Regresando al menú de Facturación.")
            menu_facturacion(config)
    return None


def menu_tablas_del_sistema(config: dict[dict]) -> None:
    op = mostrar_menu("menu_tablas_del_sistema", config)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 0:
            menu_principal(config)
        case _:
            print("Opción inválida. Regresando al menú de Tablas del Sistema.")
            menu_tablas_del_sistema(config)
    return None


if __name__ == "__main__":
    config = cargar_configuracion("menu.json")
    menu_principal(config)
