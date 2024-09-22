from modulos import reservas
from modulos import tablas_del_sistema
from typing import List, Dict

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
