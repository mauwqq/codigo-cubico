# Proyecto hotel

from os import system, name


def clear() -> None:
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")
    return None


def pedir_numero(cant_op: int) -> int:
    while True:
        try:
            n = int(input("Seleccione una opción: "))
            if (n > -1) and (n <= cant_op):
                break
            print("El número ingresado no corresponde a ninguna opción.")
        except ValueError:
            print("Debe ingresar un número.")
    return n


def menu_principal() -> None:
    clear()
    print(
        "##### Menú principal #####\n",
        "1- Tablero.\n",
        "2- Reservas.\n",
        "3- Consumos del frigobar.\n",
        "4- Facturación.\n",
        "5- Tablas del sistema.\n",
        "0- Salir del sistema.\n",
    )
    op = pedir_numero(5)
    match op:
        case 1:
            menu_tablero()
        case 2:
            menu_reservas()
        case 3:
            menu_consumo_frigobar()
        case 4:
            menu_facturacion()
        case 5:
            menu_tablas_del_sistema()
        case 0:
            print("Saliendo...")
    return None


def menu_tablero() -> None:
    clear()
    print(
        "##### Tablero #####\n",
        "1- Visualizar reservas.\n",
        "0- Menú principal.\n",
    )
    op = pedir_numero(1)
    match op:
        case 1:
            pass
        case 0:
            menu_principal()
    return None


def menu_reservas() -> None:
    clear()
    print(
        # Ver lo del check in y check out como un print para recordar al operario del sistema.
        "##### Reservas #####\n",
        "1- Registrar reserva.\n",
        "2- Datos de las reservas.\n",
        "3- Anular reserva.\n",
        "0- Menú principal.\n",
    )
    op = pedir_numero(3)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 0:
            menu_principal()
    return None


def menu_consumo_frigobar() -> None:
    clear()
    print(
        "##### Consumos frigobar #####\n",
        "1- Registrar consumo.\n",
        "2- Anular consumo.\n",
        "0- Menú principal.\n",
    )
    op = pedir_numero(2)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 0:
            menu_principal()
    return None


def menu_facturacion() -> None:
    clear()
    print(
        "##### Facturación #####\n",
        "1- Emitir facturas.\n",
        "2- Emitir notas de crédito.\n",
        "3- Consultar comprobantes.\n",
        "0- Menú principal.\n",
    )
    op = pedir_numero(3)
    match op:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 0:
            menu_principal()
    return None


def menu_tablas_del_sistema() -> None:
    clear()
    print(
        "##### Tablas #####\n",
        "1- Clientes.\n",
        "2- Habitaciones.\n",
        "3- Productos frigobar.\n",
        "4- Medios de pago.\n",
        "5- Comprobantes.\n",
        "0- Menú principal.\n",
    )
    op = pedir_numero(5)
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
            menu_principal()
    return None
