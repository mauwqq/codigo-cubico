from typing import List, Dict
from modulos import reservas
from modulos import tablas_del_sistema

<<<<<<< HEAD
def emitir_facturas(
    listado_reservas: List[Dict], listado_consumos_frigobar: List[Dict]
) -> None:
    ID = reservas.consultar_reserva(tablas_del_sistema.cargar_data("data/reservas.json"))
    for reserva in listado_reservas:
        if reserva["ID"] == ID:
            if reserva["estado"] == "check-out":
                importe_a_facturar = float(
                    input("Ingrese el importe total de la estadía a pagar: ")
                )
                print(f"El importe ingresado es: {importe_a_facturar}")
                for consumos in listado_consumos_frigobar:
                    apellido_frigobar = listado_consumos_frigobar.get("apellido")
                    nombre_frigobar = listado_consumos_frigobar.get("nombre")
                    id_frigobar = listado_consumos_frigobar.get("id_reserva")
                    importe_consumos = listado_consumos_frigobar.get("total")
                    if (
                        apellido_frigobar == apellido_consulta
                        and nombre_frigobar == nombre_consulta
                        and id_frigobar == id
                    ):
                        print(
                            f"El importe de consumos del frigobar es de {importe_consumos}"
                        )
                importe_total = importe_a_facturar + importe_consumos
                print(f"El importe total a facturar es de $ {importe_total}")
                medio_de_pago = input("Ingrese el medio de pago: ")
                print(
                    "EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA AGREGAR EL IMPORTE PAGADO Y EL MEDIO DE PAGO A LA RESERVA"
                )
            # FALTARÍA ADEMÁS AGREGAR SI LA FACTURA ES A O B DEPENDIENDO DE LA CONDICIÓN FISCAL Y EL DESAGREGADO DEL IVA EN CASO DE QUE SEA A
=======
def consultar_consumos(ID: int) -> float:
    '''Busca una reserva por su ID. Toma las cantidades consumidas de cada producto
    que están dentro del listado de reservas y las multiplica por las cantidades 
    consumidas.
    Muestra un listado de productos consumidos y el importe total.

    Pre: el listado de reservas se trae de reservas.json y el de productos
    de productos.csv a través de la función cargar_data dentro de tablas_del_sistema.
    El ID se pasa como parámetro desde la función emitir_facturas.

    Post: muestra a través de un print el listado de consumos. Devuelve el importe
    total a facturar.
    FALTA
    
    '''
    
    listado_reservas = reservas.consultar_reserva(tablas_del_sistema.cargar_data("data/reservas.json"))
    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    consumos = [reserva[ID].get("consumos") for reserva in listado_reservas] 
    if sum(consumos) == 0:
        print(f"La reserva {ID} no posee consumos del frigobar")
    else:
        consumo_total = 0
        for i, (codigo, productos) in enumerate(listado_productos.items()):
            nombre_producto = productos.get("NOMBRE")
            precio_producto = productos.get("PRECIO_U")
            consumo_total += precio_producto*consumos[i]
            if consumos[i] > 0:
                print(f"{nombre_producto} - Precio unitario: {precio_producto} - Cantidad: {consumos[i]} - Total: {precio_producto*consumos[i]}")

    return consumo_total

def discriminar_IVA(importe_hospedaje: float, importe_frigobar: float) -> None:
    '''Consulta la condición frente al IVA del cliente. Si es Responsable Incripto (RI)
    o monotributista, discriminará el IVA de los importes totales, separando
    el hospedaje de los consumos del frigobar. Si es consumidor final o exento
    no discriminará el IVA.

    Pre: pasar como argumento el improte del hospedaje y el de los consumos del
    frigobar. Pedirá al usuario que indique la condición frente al IVA.

    Post: no devolverá nada sino que imrpmimirá el neto, IVA y total, separando 
    hospedaje de consumos del frigobar.
    '''
    while True:
        try:
            condicion_IVA = int(input("Indique la condición frente al IVA del cliente, siendo 1 para monotributo o RI y 2 para consumidor final o exento"))
            if condicion_IVA == 1:
                print(f"Hospedaje: neto $ {importe_hospedaje / 1.21} - IVA $ {importe_hospedaje * 0.21} - Total $ {importe_hospedaje}")
                print(f"Consumos frigobar: neto $ {importe_frigobar / 1.21} - IVA $ {importe_frigobar * 0.21} - Total $ {importe_frigobar}")
            if condicion_IVA == 2:
                print(f"Hospedaje: Total $ {importe_hospedaje}")
                print(f"Consumos frigobar: Total $ {importe_frigobar}")
        except ValueError:
            print("Ingrese un número válido")


def emitir_facturas(listado_reservas: List[Dict]) -> None:
    '''Busca una reserva por su ID. Si el estado es "check-out" pide el importe de la estadía.
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
    '''
    
    ID = reservas.consultar_reserva(tablas_del_sistema.cargar_data("data/reservas.json")) # FUNCIONA RARO
    if ID == 0:
        print("No existe la reserva consultada")
    else:
        reserva_encontrada = list(reserva for reserva in listado_reservas if reserva["ID"] == str(ID))[0]
        if reserva_encontrada and reserva_encontrada['estado'] != "desocupada":
            print(f"{reserva_encontrada['estado']}")
            print(f"Aún no se produjo el check-out para la reserva N° {ID}")
        else:
            importe_a_facturar = float(input("Ingrese el importe total de la estadía a pagar: "))
            print(f"El importe ingresado es: {importe_a_facturar}")
            importe_consumos_frigobar = consultar_consumos(ID)
            print(f"El importe de consumos del frigobar es de {importe_consumos_frigobar}")
            importe_total = importe_a_facturar + importe_consumos_frigobar
            print(f"El importe total a facturar es de $ {importe_total}")
            medio_de_pago = input("Ingrese el medio de pago: ")
            reserva_encontrada['importe_pagado'] = importe_total
            reserva_encontrada['medio_de_pago'] = medio_de_pago
            discriminar_IVA(importe_a_facturar,importe_consumos_frigobar)

def emitir_nota_de_crédito(listado_reservas: List[Dict]) -> None:
    '''Busca una reserva por su ID. Si el estado es "check-out" pide el importe a
    anular, ya que una nota de crédito implica la disminución del importe
    original. Pregunta el importe a anular. Pregunta la condición frente al IVA. En caso
    de que el cliente sea monotributista o Responsable Inscripto se discrimina el IVA.
    Luego muestra el importe total a facturar con los datos.

    Pre: el listado de reservas proviene de reservas.json. El importe a anular
    y la condición frente al IVA se preguntan. 

    Post: no tiene un return sino que muestra en pantalla el importe que
    debe cargar en la nota de crédito luego en AFIP.
    '''
    
    ID = reservas.consultar_reserva(tablas_del_sistema.cargar_data("data/reservas.json"))
    for reserva in listado_reservas:
        if reserva["ID"] == ID and reserva["estado"] == "desocupada":
            importe_pagado = reserva.get["importe_pagado"]
            importe_a_anular = float(input("Ingrese el importe total a anular en nota de crédito: "))
            print(f"El importe ingresado es: {importe_a_anular}")
            reserva['importe_pagado'] = importe_pagado - importe_a_anular
            discriminar_IVA(importe_a_anular, 0)

>>>>>>> e918dae (modificados facturacion y menu)
