from typing import List, Dict
from modulos import reservas
from modulos import tablas_del_sistema


def pedir_num(msj: str, tipo):
    """Pide un numero y lo devuelve.

    Pre: msj es un string.
         tipo es el tipo de valor que va a pedir, puede ser un entero o un flotante.

    Post: Devuelve el numero ingresado si no es negativo.

    Raises: TypeError: si el dato ingresado no se puede castear al tipo pedido al
            llamar la funcion.
            ValueError: si el valor ingresado no es un numero, o no es un numero
            positivo.

    """
    while True:
        try:
            n = input(msj).strip()
            if tipo == int and not n.isdigit():
                raise ValueError("Ingrese un numero valido.")
            if tipo(n):
                break
            raise ValueError("El valor ingresado debe ser positivo.")
        except TypeError:
            print("Error: No se pudo convertir el dato. Verifique el tipo.")
        except ValueError as e:
            print(e)
    return n


def imprimir_detalles_iva(etiqueta: str, importe: float, discriminar: bool) -> None:
    """Imprime los detalles del IVA para el importe dado.

    Pre: etiqueta indica si es 'Hospedaje' o 'Consumos frigobar', importe es el monto a procesar,
         y discriminar indica si debe discriminar IVA o no.

    Post: Muestra el neto, el IVA y el total en caso de que deba discriminar IVA,
          o solo el total en caso contrario.

    """
    if discriminar:
        neto = round(importe / 1.21, 2)
        iva = round(importe * 0.21, 2)
        print(f"{etiqueta}: neto $ {neto} - IVA $ {iva} - Total $ {importe}")
    else:
        print(f"{etiqueta}: Total $ {importe:.2f}")
    return None


def discriminar_iva() -> bool:
    """Consulta la condición frente al IVA del cliente y retorna discriminar.

    Pre: El importe del hospedaje y el de los consumos del frigobar.

    Post: Devuelve discriminar, un booleano.

    Raises: ValueError: si el valor ingreado no esta dentro de las opciones.

    """
    while True:
        try:
            condicion_iva = pedir_num(
                "Indique la condición frente al IVA (1-Monotributo o RI, 2-Consumidor final): ",
                int,
            )
            print(condicion_iva)
            if condicion_iva not in ("1", "2"):
                raise ValueError(
                    "Ingrese 1 para monotributo o RI y 2 para consumidor final."
                )
            break
        except ValueError as e:
            print(e)
    return bool(condicion_iva)


def emitir_factura(listado_reservas: List[Dict]) -> None:
    """Busca una reserva por su ID. Si el estado es "check-out" pide el importe de la estadía.
    Lo muestra. También muestra el total detallado de los consumos del frigobar, tomando
    los precios de los productos desde productos.json y multiplicando por lo consumido que
    está registrando en reservas.json.
    Pregunta la condición frente al IVA. En caso de que el cliente sea monotributista o
    Responsable Inscripto se discrimina el IVA. Luego muestra el importe total a facturar
    con los datos.

    Pre: el listado de reservas proviene de reservas.json. La lista de productos viene de
    productos.json, que ya tiene cargados los precios.

    Post: no tiene un return sino que muestra en pantalla lo que se debe facturar
    luego en AFIP.

    """
    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    if not id_:
        print("No se encontro la reserva.")
        return None

    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    if not listado_productos:
        return None

    reserva_encontrada = list(
        reserva for reserva in listado_reservas if reserva["ID"] == str(id_)
    )[0]
    if reserva_encontrada and reserva_encontrada["estado"] != "desocupada":
        print(f"Aún no se produjo el check-out para la reserva N° {id_}")
        return None

    importe_a_facturar = pedir_num(
        "Ingrese el importe total de la estadía a pagar: ", float
    )
    consumos = reserva_encontrada.get("consumos", [])
    consumo_total = calcular_consumo_total(consumos, listado_productos)
    print(f"El importe ingresado es: {importe_a_facturar}")
    if not sum(consumos):
        print(f"La reserva {id_} no posee consumos del frigobar.")
    else:
        for i, producto in enumerate(listado_productos):
            precio_producto = producto.get("PRECIO_U", 0)
            cantidad_consumo = consumos[i]
            total_consumo = float(precio_producto) * cantidad_consumo
            if total_consumo:
                print(
                    f"{producto['NOMBRE']} - Precio unitario: {precio_producto} - Cantidad: {cantidad_consumo} - Total: {total_consumo}"
                )
    print(f"El importe de consumos del frigobar es de {consumo_total}")
    importe_total = float(importe_a_facturar) + consumo_total
    print(f"El importe total a facturar es de $ {importe_total}")
    tablas_del_sistema.medios_de_pago()
    medio_de_pago = pedir_num("Ingrese el medio de pago: ", int)
    discriminar = discriminar_iva()
    imprimir_factura(importe_a_facturar, consumo_total, discriminar)
    reserva_encontrada["importe_pagado"] = str(float(importe_a_facturar) + float(consumo_total))
    reserva_encontrada["medio_de_pago"] = medio_de_pago
    tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
    return None


def calcular_consumo_total(consumos: List[int], listado_productos: List[Dict]) -> float:
    """Calcula el consumo total basado en los consumos y los precios de los productos.

    Pre: consumos es una lista de numeros enteros.
         listado_productos es una lista de diccionarios.

    Post: devuelve la suma del consumo del frigobar, en flotante.

    """
    return sum(
        float(producto.get("PRECIO_U", 0)) * consumo
        for producto, consumo in zip(listado_productos, consumos)
    )


def emitir_nota_de_credito(listado_reservas: List[Dict]) -> None:
    """Busca una reserva por su ID. Si el estado es "check-out" pide el importe a
    anular, ya que una nota de crédito implica la disminución del importe
    original. Pregunta el importe a anular. Pregunta la condición frente al IVA. En caso
    de que el cliente sea monotributista o Responsable Inscripto se discrimina el IVA.
    Luego muestra el importe total a facturar con los datos.

    Pre: el listado de reservas proviene de reservas.json. El importe a anular
    y la condición frente al IVA se preguntan.

    Post: no tiene un return sino que muestra en pantalla el importe que
    debe cargar en la nota de crédito luego en AFIP.

    """
    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    if not id_:
        print("No se encontro la reserva.")
        return None

    reserva_encontrada = list(
        reserva for reserva in listado_reservas if reserva["ID"] == str(id_)
    )[0]
    if reserva_encontrada["estado"] == "desocupada":
        importe_pagado = reserva_encontrada.get("importe_pagado", 0)
        importe_a_anular = pedir_num(
            "Ingrese el importe total a anular en nota de crédito: ", float
        )
        print(f"El importe ingresado es: {importe_a_anular}")
        importe_final = float(importe_pagado) - float(importe_a_anular)
        if importe_final < 0:
            importe_final = 0.0
        reserva_encontrada["importe_pagado"] = importe_final
        discriminar = discriminar_iva()
        consumos = reserva_encontrada.get("consumos", [])
        consumo_total = calcular_consumo_total(consumos, tablas_del_sistema.cargar_data("data/productos.csv"))
        tablas_del_sistema.guardar_data(listado_reservas, "data/reservas.json")
        imprimir_factura(importe_final, consumo_total, discriminar)
    else:
        print("No se encontro la reserva.")
    return None


def imprimir_factura(
    importe_a_facturar: float,
    consumo_total: float,
    discriminar: bool,
) -> None:
    """
    Imprime los detalles de la factura, incluyendo consumos, IVA, y medios de pago.

    Pre: importe_a_facturar es un flotante.
         consumo_total es un flotante.
         medio_de_pago es un string.
         discriminar es un booleano.

    Post: No devuelve nada.

    """
    imprimir_detalles_iva("Hospedaje", float(importe_a_facturar), discriminar)
    imprimir_detalles_iva("Frigobar", float(consumo_total), discriminar)
    return None
