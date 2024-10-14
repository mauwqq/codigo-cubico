from modulos import reservas
from modulos import tablas_del_sistema
from typing import List, Dict


def discriminar_iva(importe_hospedaje: float, importe_frigobar: float) -> None:
    """Consulta la condición frente al IVA del cliente. Si es Responsable Incripto (RI)
    o monotributista, discriminará el IVA de los importes totales, separando
    el hospedaje de los consumos del frigobar. Si es consumidor final o exento
    no discriminará el IVA.

    Pre: pasar como argumento el improte del hospedaje y el de los consumos del
    frigobar. Pedirá al usuario que indique la condición frente al IVA.

    Post: no devolverá nada sino que imrpmimirá el neto, IVA y total, separando
    hospedaje de consumos del frigobar.
    """

    while True:
        try:
            condicion_iva = int(
                input(
                    "Indique la condición frente al IVA del cliente, siendo 1 para monotributo o RI y 2 para consumidor final o exento: "
                )
            )
            assert (
                condicion_iva == 1 or condicion_iva == 2
            ), "Número erróneo, ingrese 1 para monotributo o RI y 2 para consumidor final o exento"
        except AssertionError as mensaje:
            print(mensaje)
        except ValueError:
            print("Ingrese un número válido")
        else:
            if condicion_iva == 1:
                print(
                    f"Hospedaje: neto $ {round(importe_hospedaje / 1.21,2)} - IVA $ {round(importe_hospedaje * 0.21,2)} - Total $ {importe_hospedaje}"
                )
                print(
                    f"Consumos frigobar: neto $ {round(importe_frigobar / 1.21,2)} - IVA $ {round(importe_frigobar * 0.21,2)} - Total $ {importe_frigobar}"
                )
            if condicion_iva == 2:
                print(f"Hospedaje: Total $ {importe_hospedaje}")
                print(f"Consumos frigobar: Total $ {importe_frigobar}")
            break


def emitir_facturas(listado_reservas: List[Dict]) -> None:
    """Busca una reserva por su ID. Si el estado es "check-out" pide el importe de la estadía.
    Lo muestra. También muestra el total detallado de los consumos del frigobar, tomando
    los precios de los productos desde productos.json y multiplicando por lo consumido que
    está registrando en reservas.json.
    Pregunta la condición frente al IVA. En caso
    de que el cliente sea monotributista o Responsable Inscripto se discrimina el IVA.
    Luego muestra el importe total a facturar con los datos.

    Pre: el listado de reservas proviene de reservas.json. La lista de productos viene de
    productos.json, que ya tiene cargados los precios.

    Post: no tiene un return sino que muestra en pantalla lo que se debe facturar
    luego en AFIP.
    """

    id_ = reservas.consultar_reserva(
        tablas_del_sistema.cargar_data("data/reservas.json")
    )
    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    try:
        reserva_encontrada = list(
            reserva for reserva in listado_reservas if reserva["id_"] == str(id_)
        )[0]
        if reserva_encontrada and reserva_encontrada["estado"] != "desocupada":
            print(f"{reserva_encontrada['estado']}")
            print(f"Aún no se produjo el check-out para la reserva N° {id_}")
        else:
            importe_a_facturar = float(
                input("Ingrese el importe total de la estadía a pagar: ")
            )  # VER CÓMO HACER EL MANEJO DE EXCEPCION SI PONE CERO O STR
            print(f"El importe ingresado es: {importe_a_facturar}")
            consumos = reserva_encontrada.get("consumos", [])
            if sum(consumos) == 0:
                print(f"La reserva {id_} no posee consumos del frigobar")
                consumo_total = 0
            else:
                consumo_total = 0
                for i, productos in enumerate(listado_productos):
                    nombre_producto = productos.get("NOMBRE")
                    precio_producto = productos.get("PRECIO_U")
                    consumo_total += float(precio_producto) * consumos[i]
                    if consumos[i] > 0:
                        print(
                            f"{nombre_producto} - Precio unitario: {precio_producto} - Cantidad: {consumos[i]} - Total: {float(precio_producto)*consumos[i]}"
                        )
            print(f"El importe de consumos del frigobar es de {consumo_total}")
            importe_total = importe_a_facturar + consumo_total
            print(f"El importe total a facturar es de $ {importe_total}")
            medio_de_pago = input("Ingrese el medio de pago: ")
            reserva_encontrada["importe_pagado"] = importe_total
            reserva_encontrada["medio_de_pago"] = medio_de_pago
            discriminar_iva(importe_a_facturar, consumo_total)

    except IndexError:
        print("No existe la reserva consultada")
    except AssertionError as mensaje:
        print(mensaje)


def emitir_nota_de_crédito(listado_reservas: List[Dict]) -> None:
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

    try:
        for reserva in listado_reservas:
            if reserva["id_"] == id_ and reserva["estado"] == "desocupada":
                importe_pagado = reserva.get("importe_pagado", 0)
                importe_a_anular = float(
                    input("Ingrese el importe total a anular en nota de crédito: ")
                )
                print(f"El importe ingresado es: {importe_a_anular}")
                reserva["importe_pagado"] = importe_pagado - importe_a_anular
                discriminar_iva(importe_a_anular, 0)
    except:
        print("La reserva no tiene importes pagados")
