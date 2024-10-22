from typing import List, Dict
from modulos import reservas
from modulos import tablas_del_sistema

'''ANÁLISIS

DOS FUNCIONES MÍNIMO:
UNA ES REGISTRAR CONSUMO
LA OTRA ES ANULAR CONSUMO

EN REGISTRAR CONSUMO SE BUSCA LA RESERVA (VER SI USO CONSULTAR RESERVAS COMO EN FACTURACION)
LA RESERVA TIENE QUE ESTAR OCUPADA
SI ESTÁ OCUPADA, SE PIDE QUE INGRESE EL CÓDIGO DEL PRODUCTO Y LUEGO LA CANTIDAD
MUESTRA LO ELEGIDO Y PIDE CONFIRMACION
SI CONFIRMA ES AGREGADO EL CONSUMO A LA RESERVA

'''

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
        reserva for reserva in listado_reservas if reserva["id_"] == str(id_)
    )[0]
    if reserva_encontrada and reserva_encontrada["estado"] != "ocupada":
        print(f"La reserva N° {id_} no se encuentra ocupada actualmente")
        return None
    

    for i, producto in enumerate(listado_productos):
            id_producto = producto.get("COD", 0)
            nombre_producto = producto.get("NOMBRE",0)
            print(f"Código: {id_producto} | Descripción: {nombre_producto}")
    
    consumos = reserva_encontrada.get("consumos", [0]*5)
    while True:
        try:
            codigo_producto = int(input("Ingrese el código del producto a registrar: "))
            if codigo_producto not in [0,1,2,3,4]:
                raise ValueError("Ingrese un número de producto válido")
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                print("Ingrese un número válido.")
            else:
                print(e)

        else:
            try:
                cantidad_consumida = int(input(f"Ingrese la cantidad consumida del producto {codigo_producto}: "))
            except ValueError:
                print("Ingrese un número entero válido")
            else:
                consumos[codigo_producto] += cantidad_consumida
                print(f"Se registró el consumo de {cantidad_consumida} unidades del producto {codigo_producto} ")
    
            reserva_encontrada["consumos"] = consumos
            tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
            return None
   

def anular_consumos(listado_reservas: List[Dict]) -> None:
    """Busca una reserva por su ID. Si el estado es "ocupada" pide que indique el producto
    y la cantidad a anular. Modifica la cantidad consumida en la reserva.

    Pre: el listado de reservas proviene de reservas.json. La lista de productos viene de
    productos.json, que ya tiene cargados los precios.

    Post: no tiene un return sino que muestra en pantalla lo que se consumió y elimina
    el listado de consumos a la reserva.

    """
    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    if id_ == 0:
        print("No se encontro la reserva.")
        return None

    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    reserva_encontrada = list(
        reserva for reserva in listado_reservas if reserva["id_"] == str(id_)
    )[0]
    if reserva_encontrada and reserva_encontrada["estado"] != "ocupada":
        print(f"La reserva N° {id_} no se encuentra ocupada actualmente")
        return None
    

    for i, producto in enumerate(listado_productos):
            id_producto = producto.get("COD", 0)
            nombre_producto = producto.get("NOMBRE",0)
            print(f"Código: {id_producto} | Descripción: {nombre_producto}")
    
    consumos = reserva_encontrada.get("consumos", [])
    while True:
        try:
            codigo_producto = int(input("Ingrese el código del producto a anular: "))
            if codigo_producto not in [0,1,2,3,4]:
                raise ValueError("Ingrese un número de producto válido")
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                print("Ingrese un número válido.")
            else:
                print(e)

        else:
            try:
                cantidad_anulada = int(input(f"Ingrese la cantidad a anular del producto {codigo_producto}: "))
            except ValueError:
                print("Ingrese un número entero válido")
            else:
                consumos[codigo_producto] -= cantidad_anulada
                print(f"Se registró la anulación de {cantidad_anulada} unidades del producto {codigo_producto} ")
    
            reserva_encontrada["consumos"] = consumos
            tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
            return None
