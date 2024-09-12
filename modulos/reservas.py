from datetime import datetime
import json
import os


def cargar_configuracion(ruta_archivo: str) -> dict[str]:
    """Cargar informacion de un archivo JSON."""
    try:
        with open(ruta_archivo, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: no se encontro: {ruta_archivo}.")
        return []
    except json.JSONDecodeError as e:
        print("Error: {e}")
        return []


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def registrar_reserva(lista_reservas: dict[str]) -> None:
    """Contrato: registra una reserva a partir de los datos ingresados por el usuario. Valida si existe la misma reserva
        si coincide DNI con fecha de inicio y fecha de fin. También valida que la habitación no esté ocupada en la fecha de inicio indicada.
    Pre: el nombre, apellido, domicilio calle, localidad y provincia deben ser strings. DNI debe ser un número entero positivo de 7 u 8 caracteres.
        El N° de domicilio es el número de casa, debe ser un entero distinto de cero, así como el piso. El departamento puede ser un string o un entero.
        El número de habitación debe ser un entero entre 1 y 29, que son la cantidad de habitaciones.
        Las fechas de comienzo y de final de la estadía deben tener el formato DD para el día, MM para el mes y AA para el año.
        El importe de la reserva debe ser un entero superior a cero. El medio de pago debe ser un string.
        La lista de reservas proviene de y se guarda en un JSON.
    Pos: almacena los datos en un JSON y genera automáticamente un número de reserva.
    """
    nombre = input("Ingrese el nombre del huesped: ")
    apellido = input("Apellido: ")
    DNI = int(input("Ingrese el número de DNI sin puntos: "))
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

    # apellido_registrado = lista_reservas.get('apellido')
    # dia_ini_registrado = lista_reservas.get('dia_ini')
    # mes_ini_registrado = lista_reservas.get('mes_ini')
    # anio_ini_registrado = lista_reservas.get('anio_ini')
    # num_habitacion_registrado = lista_reservas.get('num_habitacion')
    # if apellido_registrado == apellido and dia_ini_registrado == dia_ini and mes_ini_registrado == mes_ini and anio_ini_registrado == anio_ini:
    #    print("La reserva ya ha sido registrada")
    # else:
    print(f"Datos personales: {nombre} {apellido} - DNI N°: {DNI}")
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
        # if num_habitacion_registrado == num_habitacion and dia_ini_registrado == dia_ini and mes_ini_registrado == mes_ini and anio_ini_registrado == anio_ini:
        #    print("La habitación no está disponible en la fecha indicada")
        # else:
        ID_reserva = str(
            10
        )  # ACÁ HAY QUE CREAR UN NÚMERO DE RESERVA PROGRESIVO ASCENDENTE A PARTIR DEL ÚLTIMO DEL JSON, NO SÉ CÓMO HACERLO.
        data = {
            "ID": ID_reserva,
            "nombre": nombre,
            "apellido": apellido,
            "DNI": str(DNI),
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
        }
        listado_de_reservas.append(data)
        with open("reservas.json", "w", encoding="utf-8") as file:
            json.dump(
                listado_de_reservas, file, ensure_ascii=False, indent=4
            )  # esta parte no funciona porque no termino de entender cómo llamar al archivo JSON


if __name__ == "__main__":
    listado_de_reservas = cargar_configuracion("reservas.json")
    registrar_reserva(listado_de_reservas)
