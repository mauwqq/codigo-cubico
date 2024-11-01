from typing import List, Dict
from modulos import reservas
from modulos import tablas_del_sistema


def pedir_cod_producto(consumos: List[int]) -> int:
    """"""
    while True:
        try:
            cod = input("Ingrese el código del producto: ")
            if not cod.isdigit():
                raise ValueError("Debe ingresar un numero.")
            if cod not in tuple(str(i) for i in range(len(consumos))):
                raise ValueError("Ingrese un número de producto válido.")
            break
        except ValueError as e:
            print(e)
    return cod


def registrar_consumos(listado_reservas: List[Dict]) -> None:
    """Busca una reserva por su ID. Si el estado es "ocupada" pide que indique el producto
    y la cantidad consumida. Agrega los consumos a la reserva.

    Pre: el listado de reservas proviene de reservas.json. La lista de productos viene de
    productos.json, que ya tiene cargados los precios.

    Post: no tiene un return sino que muestra en pantalla lo que se consumió y agrega
    el listado de consumos a la reserva o lo modifica si ya existe.

    """
    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    if id_ == 0:
        print("No se encontro la reserva.")
        return None
    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    reserva_encontrada = list(
        reserva for reserva in listado_reservas if reserva["ID"] == str(id_)
    )[0]
    if reserva_encontrada and reserva_encontrada["estado"] != "ocupada":
        print(f"La reserva N° {id_} no se encuentra ocupada actualmente")
        return None
    for producto in listado_productos:
        id_producto = producto.get("ID", 0)
        nombre_producto = producto.get("NOMBRE", "Desconocido")
        print(f"Código: {id_producto} | Descripción: {nombre_producto}")
    consumos = reserva_encontrada.get("consumos", [0] * 5)
    codigo_producto = pedir_cod_producto(consumos)
    while True:
        try:
            cantidad_consumida = input(
                f"Ingrese la cantidad consumida del producto {codigo_producto}: "
            )
            if not cantidad_consumida.isdigit():
                raise ValueError("Debe ingresar un numero.")
            break
        except ValueError as e:
            print(e)
    consumos[int(codigo_producto)] += int(cantidad_consumida)
    print(
        f"Se registró el consumo de {cantidad_consumida} unidades del producto {codigo_producto}"
    )
    reserva_encontrada["consumos"] = consumos
    tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
    return None


def anular_consumos(listado_reservas: List[Dict]) -> None:
    """
    Busca una reserva por su ID. Si el estado es "ocupada" pide que indique el producto
    y la cantidad a anular. Modifica la cantidad consumida en la reserva.
    """
    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    if id_ == 0:
        print("No se encontró la reserva.")
        return None
    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    reserva_encontrada = list(
        reserva for reserva in listado_reservas if reserva["ID"] == str(id_)
    )[0]
    if reserva_encontrada and reserva_encontrada["estado"] != "ocupada":
        print(f"La reserva N° {id_} no se encuentra ocupada actualmente.")
        return None
    for producto in listado_productos:
        id_producto = producto.get("ID", 0)
        nombre_producto = producto.get("NOMBRE", "Desconocido")
        print(f"Código: {id_producto} | Descripción: {nombre_producto}")
    consumos = reserva_encontrada.get("consumos", [])
    codigo_producto = pedir_cod_producto(consumos)
    while True:
        try:
            cantidad_anulada = input(
                f"Ingrese la cantidad a anular del producto {codigo_producto}: "
            )
            if not cantidad_anulada.isdigit():
                raise ValueError("Debe ingresar un numero.")
            if int(cantidad_anulada) > consumos[int(codigo_producto)]:
                raise ValueError(
                    f"No se puede anular más de lo consumido. Consumo actual: {consumos[codigo_producto]}"
                )
            break
        except ValueError as e:
            print(e)
    consumos[int(codigo_producto)] -= int(cantidad_anulada)
    print(
        f"Se registró la anulación de {cantidad_anulada} unidades del producto {codigo_producto}."
    )
    reserva_encontrada["consumos"] = consumos
    tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
    return None
