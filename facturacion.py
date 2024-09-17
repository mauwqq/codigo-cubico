def emitir_facturas(listado_reservas: list, listado_consumos_frigobar: list) -> None:
    '''Contrato: genera los datos necesarios para que se pueda emitir la factura luego desde la página de AFIP. Recibe la lista
    de reservas, busca por apellido y nombre del huesped la reserva. Si el estado de la reserva es "ckeck-out" entonces se puede generar 
    la factura. Contempla tanto los consumos del frigobar como la tarifa de la habitación. La fecha de emisión será la del sistema.
    Pre: se deben proporcionar los JSON de la lista de reservas y de la lista de consumos del frigobar. Se ingresa por teclado el apellido
    y nombre del huesped, el importe de la tarifa a abonar y el medio de pago. 
    Pos: el importe pagado total se almacena en la reserva junto con el medio de pago.
    '''
    apellido_consulta = input("Ingrese el apellido del huesped en mayúsculas: ")
    nombre_consulta = input("Ingrese el nombre del huesped en mayúsculas: ")
    for reserva in listado_reservas:
        apellido = listado_reservas.get('apellido')
        nombre = listado_reservas.get('nombre')
        id = listado_reservas.get('id_reserva')
        DNI = listado_reservas.get('DNI')
        calle = listado_reservas.get('calle')
        numero = listado_reservas.get('numero')
        piso = listado_reservas.get('piso')
        dpto = listado_reservas.get('dpto')
        localidad = listado_reservas.get('localidad')
        provincia = listado_reservas.get('provincia')
        habitacion = listado_reservas.get('habitacion')
        fecha_reserva = listado_reservas.get('fecha reserva')
        inicio_estadia = listado_reservas.get('inicio estadia')
        fin_estadia = listado_reservas.get('fin estadia')
        estado_reserva = listado_reservas.get('estado reserva')
        if apellido == apellido_consulta and nombre == nombre_consulta:
            print(f"ID: {id} - Datos personales: {nombre} {apellido} - DNI N°: {DNI}")
            print(
                f"Domicilio: {calle} N° {numero} - Piso {piso} - Departamento {dpto} - {localidad} - {provincia}"
            )
            print(f"Fecha de reserva: {fecha_reserva} - Habitación: {habitacion}")
            print(
                f"Inicio estadía: {inicio_estadia} - Fin estadía: {fin_estadia} - Estado: {estado_reserva}"
            )
        if estado_reserva == 'check-out':
            importe_a_facturar = float(input("Ingrese el importe total de la estadía a pagar: "))
            print(f"El importe ingresado es: {importe_a_facturar}")
            for consumos in listado_consumos_frigobar:
                apellido_frigobar = listado_consumos_frigobar.get('apellido')
                nombre_frigobar = listado_consumos_frigobar.get('nombre')
                id_frigobar = listado_consumos_frigobar.get('id_reserva')
                importe_consumos = listado_consumos_frigobar.get('total')
                if apellido_frigobar == apellido_consulta and nombre_frigobar == nombre_consulta and id_frigobar == id:
                    print(f"El importe de consumos del frigobar es de {importe_consumos}")
            importe_total = importe_a_facturar + importe_consumos
            print(f"El importe total a facturar es de $ {importe_total}")
            medio_de_pago = input("Ingrese el medio de pago: ")
            print("EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA AGREGAR EL IMPORTE PAGADO Y EL MEDIO DE PAGO A LA RESERVA")
            # FALTARÍA ADEMÁS AGREGAR SI LA FACTURA ES A O B DEPENDIENDO DE LA CONDICIÓN FISCAL Y EL DESAGREGADO DEL IVA EN CASO DE QUE SEA A


