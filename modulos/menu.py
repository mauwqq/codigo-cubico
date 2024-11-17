from typing import Dict
import os
import time
from modulos import tablas_del_sistema
from modulos import reservas
from modulos import facturacion
from modulos import consumos


RUTA_RESERVAS = "data/reservas.json"
RUTA_MENU = "data/menu.json"
RUTA_CLIENTES = "data/clientes.csv"
RUTA_HABITACIONES = "data/habitaciones.csv"
RUTA_PRODUCTOS = "data/productos.csv"


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

    Raises: ValueError: si no se ingresa un numero entero.

    """
    while True:
        try:
            n = input("Seleccione una opción: ")
            if not n.isdigit():
                raise ValueError("Debe ingresar un numero.")
        except ValueError as e:
            print(e)
        else:
            if n in opciones:
                break
            print("El número ingresado no corresponde a ninguna opción.")
    return int(n)


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
    if not config:
        return 0
    opciones = config[nombre_menu]
    print("=" * 27)
    for clave, valor in opciones.items():
        print(f"{clave}- {valor}.")
    print("=" * 27)
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
    data = tablas_del_sistema.cargar_data(RUTA_MENU)
    op = mostrar_menu_y_pedir_numero("menu_principal", data)
    match op:
        case 1:
            menu_reservas(data)
        case 2:
            menu_consumo_frigobar(data)
        case 3:
            menu_facturacion(data)
        case 4:
            menu_tablas_del_sistema(data)
        case 0:
            print("Saliendo...")
        case _:
            print("Opción inválida. Regresando al menú principal.")
            menu_principal()
    return None


def menu_reservas(config: Dict[str, Dict[str, str]]) -> None:
    """Muestra el menú de reservas y ejecuta la opción seleccionada.

    Pre: "config" es un diccionario que contiene el menú de reservas.

    Post: Muestra el menú de reservas y llama a la función correspondiente según
          la opción seleccionada por el usuario.

    """
    op = mostrar_menu_y_pedir_numero("menu_reservas", config)
    data = tablas_del_sistema.cargar_data(RUTA_RESERVAS)
    match op:
        case 1:
            reservas.registrar_reserva(data)
            volver_al_menu()
        case 2:
            reservas.datos_reserva()
            volver_al_menu()
        case 3:
            reservas.anular_reserva(data)
            volver_al_menu()
        case 4:
            reservas.registrar_check_in(data)
            volver_al_menu()
        case 5:
            reservas.registrar_check_out(data)
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
            consumos.registrar_consumos(tablas_del_sistema.cargar_data(RUTA_RESERVAS))
            volver_al_menu()
        case 2:
            consumos.anular_consumos(tablas_del_sistema.cargar_data(RUTA_RESERVAS))
            volver_al_menu()
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
            facturacion.emitir_factura(tablas_del_sistema.cargar_data(RUTA_RESERVAS))
            volver_al_menu()
        case 2:
            facturacion.emitir_nota_de_credito(
                tablas_del_sistema.cargar_data(RUTA_RESERVAS)
            )
            volver_al_menu()
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
            tablas_del_sistema.imprimir_tabla(RUTA_CLIENTES)
            volver_al_menu()
        case 2:
            tablas_del_sistema.imprimir_tabla(RUTA_HABITACIONES)
            volver_al_menu()
        case 3:
            tablas_del_sistema.imprimir_tabla(RUTA_PRODUCTOS)
            volver_al_menu()
        case 4:
            tablas_del_sistema.medios_de_pago()
            volver_al_menu()
        case 0:
            menu_principal()
    return None


if __name__ == "__main__":
    menu_principal()
