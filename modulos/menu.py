"""Modulo para imprimir el menu del gestor."""

from typing import Dict
import os
import time
from modulos import tablas_del_sistema
from modulos import reservas
from modulos import facturacion


def clear() -> None:
    """Limpia la consola (pantalla) del terminal.

    Pre: No recibe nada.

    Post: Devuelve None.

    """
    os.system("cls" if os.name == "nt" else "clear")
    return None


def pedir_numero(opciones: Dict[str, str]) -> int:
    """Solicita al usuario seleccionar un número de opción.

    Pre: Recibe un diccionario "opciones" que contiene las opciones válidas como
         claves.

    Post: Devuelve un número entero correspondiente a una opción válida
          seleccionada por el usuario.

    """
    while True:
        try:
            n = int(input("Seleccione una opción: "))
            if str(n) in opciones:
                break
            print("El número ingresado no corresponde a ninguna opción.")
        except ValueError:
            print("Debe ingresar un número.")
    return n


def mostrar_menu_y_pedir_numero(
    nombre_menu: str, config: Dict[str, Dict[str, str]]
) -> int:
    """Muestra el menú correspondiente y solicita una opción al usuario.

    Pre: "nombre_menu" es una cadena que representa el nombre de un menú
         existente en "config", que es un diccionario que contiene
         configuraciones de menús.

    Post: Devuelve un número entero correspondiente a una opción válida
          seleccionada en el menú.

    """
    clear()
    opciones = config[nombre_menu]
    for clave, valor in opciones.items():
        print(f"{clave}- {valor}.")
    op = pedir_numero(opciones)
    return op


def volver_al_menu() -> None:
    """Imprime un mensaje y devuelve al usuario al menu principal cuando este lo necesite.

    Pre: No recibe nada.

    Post: Devuelve None.

    """
    input("Presione 'Enter' para volver al menu.")
    menu_principal()
    return None


def no_implementado() -> None:
    """Informa al usuario que una opción no está implementada.

    Pre: No recibe nada.

    Post: Devuelve None.

    """
    print("Esta opción no está implementada aún.\nRegresando al menú...")
    time.sleep(2)
    menu_principal()
    return None


def menu_principal() -> None:
    """Muestra el menú principal y ejecuta la opción seleccionada.

    Pre: No recibe nada.

    Post: Muestra el menú principal y llama a la función correspondiente según la
          opción seleccionada por el usuario.

    """
    config = tablas_del_sistema.cargar_data("data/menu.json")
    op = mostrar_menu_y_pedir_numero("menu_principal", config)
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
            menu_principal()
    return None


def menu_tablero(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú del tablero y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene en un diccionario el menú del
         tablero.

    Post: Muestra el menú del tablero y llama a la función correspondiente según
          la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_tablero", config)
    match op:
        case 1:
            no_implementado()
        case 0:
            menu_principal()
    return None


def menu_reservas(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú de reservas y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene el menú de reservas.

    Post: Muestra el menú de reservas y llama a la función correspondiente según
          la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_reservas", config)
    config = tablas_del_sistema.cargar_data("data/reservas.json")
    match op:
        case 1:
            reservas.registrar_reserva(config)
            volver_al_menu()
        case 2:
            reservas.datos_reserva()
            volver_al_menu()
        case 3:
            reservas.anular_reserva(config)
            volver_al_menu()
        case 4:
            reservas.registrar_check_in(config)
            volver_al_menu()
        case 5:
            reservas.registrar_check_out(config)
            volver_al_menu()
        case 0:
            menu_principal()
    return None


def menu_consumo_frigobar(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú de consumo de frigobar y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene el menú de consumo

    Post: Muestra el menú de consumo de frigobar y llama a la función
          correspondiente según la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_consumo_frigobar", config)
    match op:
        case 1:
            no_implementado()
        case 2:
            no_implementado()
        case 0:
            menu_principal()
    return None


def menu_facturacion(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú de facturación y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene el menú de facturación.

    Post: Muestra el menú de facturación y llama a la función correspondiente
          según la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_facturacion", config)
    match op:
        case 1:
            facturacion.emitir_factura(
                tablas_del_sistema.cargar_data("data/reservas.json")
            )
            volver_al_menu()
        case 2:
            facturacion.emitir_nota_de_credito(
                tablas_del_sistema.cargar_data("data/reservas.json")
            )
            volver_al_menu()
        case 3:
            no_implementado()
        case 0:
            menu_principal()
    return None


def menu_tablas_del_sistema(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú de tablas del sistema y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene el menú de tablas del sistema.

    Post: Muestra el menú de tablas del sistema y llama a la función
          correspondiente según la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_tablas_del_sistema", config)
    match op:
        case 1:
            tablas_del_sistema.imprimir_tabla("data/clientes.csv")
            volver_al_menu()
        case 2:
            tablas_del_sistema.imprimir_tabla("data/habitaciones.csv")
            volver_al_menu()
        case 3:
            tablas_del_sistema.imprimir_tabla("data/productos.csv")
            volver_al_menu()
        case 4:
            no_implementado()
        case 5:
            no_implementado()
        case 0:
            menu_principal()
    return None


if __name__ == "__main__":
    menu_principal()
