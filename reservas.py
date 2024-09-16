from datetime import datetime
# import json
import os


# FALTA LA FUNCIÓN PARA CARGAR EL JSON


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def registrar_reserva(lista_reservas: list) -> None:
    """Contrato: registra una reserva a partir de los datos ingresados por el usuario. Valida si existe la misma reserva
        si coincide DNI con fecha de inicio y fecha de fin. También valida que la habitación no esté ocupada en la fecha de inicio indicada.
    Pre: el nombre, apellido, domicilio calle, localidad y provincia deben ser strings y ser ingresados en completas mayúsculas.
        DNI debe ser un número entero positivo de 7 u 8 caracteres.
        El N° de domicilio es el número de casa, debe ser un entero distinto de cero, así como el piso. El departamento puede ser un string o un entero.
        El número de habitación debe ser un entero entre 1 y 29, que son la cantidad de habitaciones.
        Las fechas de comienzo y de final de la estadía deben tener el formato DD para el día, MM para el mes y AA para el año.
        El importe de la reserva debe ser un entero superior a cero. El medio de pago debe ser un string.
        La lista de reservas proviene de y se guarda en un JSON.
    Pos: almacena los datos en un JSON y genera automáticamente un número de reserva.
    """
    nombre = input("Ingrese el nombre del huesped: ")
    apellido = input("Apellido: ")
    dni = int(input("Ingrese el número de DNI sin puntos: "))
    domicilio_calle = input("Domicilio: ingrese la calle: ")
    domicilio_numero = int(input("Altura de la calle: "))
    domicilio_piso = int(input("Piso: "))
    domicilio_dpto = input("Departamento: ")
    localidad = input("Localidad: ")
    provincia = input("Provincia: ")
    num_habitacion = int(
        input("Ingrese el número de habitación en la que se alojará: ")
    )
    fecha_reserva = datetime.now().date()
    dia_ini = int(input("Ingrese el día de inicio de la estadía: "))
    mes_ini = int(input("Indique el mes: "))
    anio_ini = int(input("Indique el año: "))
    dia_fin = int(input("Ingrese el día de finalización de la estadía: "))
    mes_fin = int(input("Indique el mes: "))
    anio_fin = int(input("Indique el año: "))
    
    for reserva in lista_reservas:
        apellido_registrado = lista_reservas.get('apellido')
        dia_ini_registrado = lista_reservas.get('dia_ini')
        mes_ini_registrado = lista_reservas.get('mes_ini')
        anio_ini_registrado = lista_reservas.get('anio_ini')
        num_habitacion_registrado = lista_reservas.get('num_habitacion')
        if apellido_registrado == apellido and dia_ini_registrado == dia_ini and mes_ini_registrado == mes_ini and anio_ini_registrado == anio_ini and num_habitacion_registrado == num_habitacion:
            print("La reserva ya fue registrada")
        else:
            print(f"Datos personales: {nombre} {apellido} - DNI N°: {dni}")
            print(
                f"Domicilio: {domicilio_calle} N° {domicilio_numero } - Piso {domicilio_piso} - Departamento {domicilio_dpto} - {localidad} - {provincia}"
            )
            print(f"Fecha de reserva: {fecha_reserva} - Habitación: {num_habitacion}")
            print(
                f"Inicio estadía: {dia_ini}/{mes_ini}/{anio_ini} - Fin estadía: {dia_fin}/{mes_fin}/{anio_fin}"
            )
            confirmacion = int(
                input("Ingrese 1 si los datos son correctos y 0 si son incorrectos: ")
            )
            if confirmacion == 0:
                clear()
            else:
                if num_habitacion_registrado == num_habitacion and dia_ini_registrado == dia_ini and mes_ini_registrado == mes_ini and anio_ini_registrado == anio_ini:
                    print("La habitación no está disponible en la fecha indicada")
                else:
                    id_reserva = str(
                        10
                    )  # ACÁ HAY QUE CREAR UN NÚMERO DE RESERVA PROGRESIVO ASCENDENTE A PARTIR DEL ÚLTIMO DEL JSON, NO SÉ CÓMO HACERLO.
                    
                    data = {
                        "id": id_reserva,
                        "nombre": nombre,
                        "apellido": apellido,
                        "DNI": str(dni),
                        "calle": domicilio_calle,
                        "numero": str(domicilio_numero),
                        "piso": str(domicilio_piso),
                        "dpto": str(domicilio_dpto),
                        "localidad": localidad,
                        "provincia": provincia,
                        "habitacion": str(num_habitacion),
                        "fecha reserva": str(fecha_reserva),
                        "inicio estadia": f"{str(dia_ini)}/{str(mes_ini)}/{str(anio_ini)}",
                        "fin estadia": f"{str(dia_fin)}/{str(mes_fin)}/{str(anio_ini)}",
                        "estado reserva": "reservada"
                    }
                lista_reservas.append(data)
                # AGREGAR LA PARTE PARA GRABAR EL DICCIONARIO EN EL ARCHIVO JSON

def consultar_reserva(listado_reservas: list) -> int:
    '''Contrato: recibe una lista de servas de un JSON y permite consultar si una reserva existe y sus datos, por el apellido y nombre del huesped.
    Pre: por teclado debe ingresarse el apellido y el nombre con mayúsculas.
    Pos: devuelve el ID de la reserva consultada para ser usado en otras funciones.
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
        else:
            print("No hay reservas registradas para ese huesped")
    return id

def anular_reserva(listado_reservas: list) -> None:
    '''Contrato: anula una reserva llamando a la función "consultar_reserva". Primero la muestra para confirmar.
    Pre: recibe una reserva desde la función "consultar_reserva".
    Pos: modifica el estado de la reserva a "anulada".
    '''
    id_anular = consultar_reserva(listado_reservas)
    for reserva in listado_reservas:
        match id_anular:
            case id_reserva if id_reserva in reserva:
                confirmacion = int(input("Ingrese 1 si los datos para confirmar la anulación y 0 para salir: "))
                if confirmacion == 0:
                    clear()
                else:
                    print("EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA REEMPLAZAR EL VALOR DE LA KEY A ANULADA")

def registrar_check_in(listado_reservas: list) -> None:
    '''Contrato: registra el check-in del huesped sobre una reserva llamando a la función "consultar_reserva". Primero la muestra para confirmar.
    Pre: recibe una reserva desde la función "consultar_reserva".
    Pos: modifica el estado de la reserva a "ocupada".
    '''
    id_modificar = consultar_reserva(listado_reservas)
    for reserva in listado_reservas:
        match id_modificar:
            case id_reserva if id_reserva in reserva:
                confirmacion = int(input("Ingrese 1 si los datos para confirmar el check-in y 0 para salir: "))
                if confirmacion == 0:
                    clear()
                else:
                    print("EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA REEMPLAZAR EL VALOR DE LA KEY A OCUPADA")


def registrar_check_out(listado_reservas: list) -> None:
    '''Contrato: registra el check-out del huesped sobre una reserva llamando a la función "consultar_reserva". Primero la muestra para confirmar.
    Pre: recibe una reserva desde la función "consultar_reserva".
    Pos: modifica el estado de la reserva a "ocupada".
    '''
    id_modificar = consultar_reserva(listado_reservas)
    for reserva in listado_reservas:
        match id_modificar:
            case id_reserva if id_reserva in reserva:
                confirmacion = int(input("Ingrese 1 si los datos para confirmar el check-out y 0 para salir: "))
                if confirmacion == 0:
                    clear()
                else:
                    print("EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA REEMPLAZAR EL VALOR DE LA KEY A CHECK-OUT")

if __name__ == "__main__":
    listado_de_reservas = {} # DESPUÉS ESTE LISTADO VA A VENIR DEL JSON
    registrar_reserva(listado_de_reservas)
