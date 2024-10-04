<<<<<<< HEAD
from datetime import datetime
import os
from typing import List, Dict
=======
from typing import Tuple, Callable, Dict, List
import re
from datetime import datetime
>>>>>>> e60989d (Registro de reservas terminado y consulta de reservas tambien. reservas.json ahora tiene estado y consumos.)

meses = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

<<<<<<< HEAD
def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")
=======
errores = {
    "nombre": {
        "vacío": "El nombre no puede estar vacío.",
        "invalido": "El nombre debe ser una sola palabra sin espacios ni símbolos.",
    },
    "apellido": {
        "vacío": "El apellido no puede estar vacío.",
        "invalido": "El apellido debe ser una sola palabra sin espacios ni símbolos.",
    },
}

def solicitar_input(validacion: Callable[[str], str], msj: str) -> str:
    """Solicita un valor al usuario y lo valida con la función dada.
>>>>>>> e60989d (Registro de reservas terminado y consulta de reservas tambien. reservas.json ahora tiene estado y consumos.)


def registrar_reserva(lista_reservas: List[Dict]) -> None:
    """Registra una reserva a partir de los datos ingresados por el usuario.
    Valida si existe la misma reserva si coincide DNI con fecha de inicio y
    fecha de fin. También valida que la habitación no esté ocupada en la fecha
    de inicio indicada.
    
    Pre: La lista de reservas proviene de y se guarda en un JSON.
    
    Pos: almacena los datos en un JSON y genera automáticamente un número de
         reserva.
    
    """
<<<<<<< HEAD
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
    encontrado = False
    for reserva in lista_reservas:
        apellido_registrado = reserva.get("apellido")
        dia_ini_registrado = reserva.get("inicio estadia").split("/")[0]
        mes_ini_registrado = reserva.get("inicio estadia").split("/")[1]
        anio_ini_registrado = reserva.get("inicio estadia").split("/")[2]
        num_habitacion_registrado = reserva.get("habitacion")
        if (
            apellido_registrado == apellido
            and dia_ini_registrado == str(dia_ini)
            and mes_ini_registrado == str(mes_ini)
            and anio_ini_registrado == str(anio_ini)
            and num_habitacion_registrado == str(num_habitacion)
        ):
            print("La reserva ya fue registrada")
            encontrado = True
            break
    if not encontrado:
        print(f"Datos personales: {nombre} {apellido} - DNI N°: {dni}")
        print(
            f"Domicilio: {domicilio_calle} N° {domicilio_numero} - Piso {domicilio_piso} - Departamento {domicilio_dpto} - {localidad} - {provincia}"
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
            return
        for reserva in lista_reservas:
            if (
                reserva.get("habitacion") == str(num_habitacion)
                and reserva.get("inicio estadia").split("/")[0] == str(dia_ini)
                and reserva.get("inicio estadia").split("/")[1] == str(mes_ini)
                and reserva.get("inicio estadia").split("/")[2] == str(anio_ini)
            ):
                print("La habitación no está disponible en la fecha indicada")
                return

        id_reserva = str(len(lista_reservas) + 1)

        data = {
            "ID": id_reserva,
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
            "fin estadia": f"{str(dia_fin)}/{str(mes_fin)}/{str(anio_fin)}",
            "estado": "reservada",
        }

        lista_reservas.append(data)


def consultar_reserva(listado_reservas: List[Dict]) -> int:
    """Recibe una lista de servas de un JSON y permite consultar si una reserva
    existe y sus datos, por el apellido y nombre del huesped.
    Pre: por teclado debe ingresarse el apellido y el nombre con mayúsculas.
    
    Post: devuelve el ID de la reserva consultada para ser usado en otras
          funciones.
    
    """
    apellido_consulta = input("Ingrese el apellido del huesped: ")
    nombre_consulta = input("Ingrese el nombre del huesped: ")
    for reserva in listado_reservas:
        apellido = reserva.get("apellido")
        nombre = reserva.get("nombre")
        ID = reserva.get("ID")
        DNI = reserva.get("DNI")
        calle = reserva.get("calle")
        numero = reserva.get("numero")
        piso = reserva.get("piso")
        dpto = reserva.get("dpto")
        localidad = reserva.get("localidad")
        provincia = reserva.get("provincia")
        habitacion = reserva.get("habitacion")
        fecha_reserva = reserva.get("fecha reserva")
        inicio_estadia = reserva.get("inicio estadia")
        fin_estadia = reserva.get("fin estadia")
        estado_reserva = reserva.get("estado")
        """
        if apellido == apellido_consulta and nombre == nombre_consulta:
            print(f"ID: {ID} - Datos personales: {nombre} {apellido} - DNI N°: {DNI}")
            print(
                f"Domicilio: {calle} N° {numero} - Piso {piso} - Departamento {dpto} - {localidad} - {provincia}"
            )
            print(f"Fecha de reserva: {fecha_reserva} - Habitación: {habitacion}")
            print(
                f"Inicio estadía: {inicio_estadia} - Fin estadía: {fin_estadia} - Estado: {estado_reserva}"
            )
        else:
            print("No hay reservas registradas para ese huesped")
        """
        return ID
    return 0


def anular_reserva(listado_reservas: List[Dict]) -> None:
    """Anula una reserva llamando a la función "consultar_reserva". Primero la
    muestra para confirmar.
    
    Pre: Recibe una reserva desde la función "consultar_reserva".
    
    Post: Modifica el estado de la reserva a "anulada".
    
    """
    id_anular = consultar_reserva(listado_reservas)
    for reserva in listado_reservas:
        if id_anular in reserva["ID"]:
            confirmacion = int(
                input(
                    "Ingrese 1 si los datos para confirmar la anulación y 0 para salir: "
                )
            )
            if confirmacion == 0:
                clear()
            else:
                print(
                    "EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA REEMPLAZAR EL VALOR DE LA KEY A ANULADA"
                )


def registrar_check_in(listado_reservas: List[Dict]) -> None:
    """Registra el check-in del huesped sobre una reserva llamando a la función
    "consultar_reserva". Primero la muestra para confirmar.
    
    Pre: Recibe una reserva desde la función "consultar_reserva".
    
    Post: Modifica el estado de la reserva a "ocupada".
    
    """
    id_modificar = consultar_reserva(listado_reservas)
    for reserva in listado_reservas:
        if id_modificar in reserva["ID"]:
            confirmacion = int(
                input(
                    "Ingrese 1 si los datos para confirmar el check-in y 0 para salir: "
                )
            )
            if confirmacion == 0:
                clear()
            else:
                print(
                    "EN ESTA PARTE TIENE QUE HABER UNA BÚSQUEDA DENTRO DEL JSON PARA REEMPLAZAR EL VALOR DE LA KEY A OCUPADA"
                )


def registrar_check_out(listado_reservas: List[Dict]) -> None:
    """Registra el check-out del huesped sobre una reserva llamando a la función
    "consultar_reserva". Primero la muestra para confirmar.
    
    Pre: Recibe una reserva desde la función "consultar_reserva".
    
    Post: Modifica el estado de la reserva a "ocupada".
    
    """
    id_modificar = consultar_reserva(listado_reservas) 
    reserva_encontrada = False
    # entra en la reserva 1 aunque la reserva no haya sido encontrada 
    """
    for reserva in listado_reservas:
        if reserva["ID"] == id_modificar:
            reserva_encontrada = True
            print(f"Datos de la reserva:\n{reserva}")
            confirmacion = int(
                input("Ingrese 1 si los datos son correctos para confirmar el check-out y 0 para salir: ")
            )
            if confirmacion == 0:
                clear()
                return 
            reserva["estado"] = "desocupada"
            print("Check-out registrado exitosamente.")
            break
    """
    if not reserva_encontrada:
        print("No se encontró la reserva con el ID proporcionado.")
=======
    while True:
        try:
            return validacion(input(msj))
        except ValueError as e:
            print(e)


def validar_con_regex(
    patron: str,
    valor: str,
    mensajes: Dict[str, str],
    verificar_longitud: bool = True,
    permitir_vacio: bool = False,
) -> str:
    """Valida un valor contra una expresión regular y otras condiciones.

    Pre: patron es una expresión regular, valor es la cadena a validar,
         mensajes es un diccionario con mensajes de error, y los parámetros
         booleanos indican si se verifica la longitud y si se permite un valor vacío.

    Post: Retorna el valor validado o "" si permitir_vacio es True y el valor es vacío.

    """
    valor = valor.strip()
    if permitir_vacio and not valor:
        return ""
    if not valor:
        raise ValueError(mensajes["vacío"])
    if not re.match(patron, valor):
        raise ValueError(mensajes["invalido"])
    if verificar_longitud and len(valor) < 3:
        raise ValueError("El campo debe tener al menos tres letras.")
    return valor.title()


def validar_dni(dni: str) -> int: # dni tambien puede ser len(7)
    """Valida que el DNI ingresado tenga el formato correcto.

    Pre: dni es una cadena que representa el DNI.

    Post: Retorna el DNI como un entero si es válido.
          ValueError si el DNI no es válido.

    """
    dni = re.sub(r"\D", "", dni)
    if len(dni) != 8:
        raise ValueError("El DNI debe contener 8 caracteres numéricos.")
    return int(dni)


def validar_domicilio(campo: str, valor: str) -> str:
    """Valida un campo de domicilio utilizando expresiones regulares.

    Pre: campo es el nombre del campo a validar y valor es la cadena a validar.

    Post: Retorna el valor validado.
          ValueError si el valor no es válido.

    """
    validaciones = {
        "Calle": (
            r"^[a-zA-Z0-9 ]+$",
            "La calle no puede estar vacía.",
            "La calle no puede contener símbolos.",
        ),
        "Altura": (
            r"^\d+$",
            "La altura no puede estar vacía.",
            "La altura debe ser un número entero.",
        ),
        "Piso": (r"^\d*$", "Ingrese un piso válido.", ""),
        "Departamento": (
            r"^[a-zA-Z0-9 ]*$",
            "El departamento no puede tener símbolos.",
            "",
        ),
        "Localidad": (
            r"^[a-zA-Z0-9 ]+$",
            "La localidad no puede estar vacía.",
            "Debe ingresar una localidad.",
        ),
        "Provincia": (
            r"^[a-zA-Z ]+$",
            "La provincia no puede estar vacía.",
            "Debe ingresar una provincia.",
        ),
    }
    patron, mensaje_vacio, mensaje_invalido = validaciones[campo]
    verificar_longitud = campo in ["Localidad", "Provincia"]
    permitir_vacio = campo in ["Piso", "Departamento"]
    return validar_con_regex(
        patron,
        valor,
        {"vacío": mensaje_vacio, "invalido": mensaje_invalido},
        verificar_longitud,
        permitir_vacio,
    )


def solicitar_datos_domicilio() -> Tuple[str, str, str, int, str, str]:
    """Solicita y valida los datos de domicilio al usuario.

    Pre: No recibe nada.

    Post: Retorna una tupla con los datos de domicilio:
          (Calle, Altura, Piso, Departamento, Localidad, Provincia).

    """
    print("Domicilio")
    campos = [
        ("Provincia", True),
        ("Localidad", True),
        ("Calle", True),
        ("Altura", True),
        ("Piso", False),
        ("Departamento", False),
    ]
    datos_domicilio = {
        campo: solicitar_input(
            lambda x: validar_domicilio(campo, x),
            f"{campo}: " if requerido else f"{campo} ('Enter' si no aplica): ",
        )
        for campo, requerido in campos
    }
    return datos_domicilio


def solicitar_datos_cliente() -> Tuple[str, str, int, str, str, str, int, str, str]:
    """Solicita y valida los datos del cliente.

    Pre: No recibe nada.

    Post: Retorna una tupla con los datos del cliente:
          (Nombre, Apellido, DNI, Calle, Altura, Piso, Departamento, Localidad, Provincia).

    """

    nombre = solicitar_input(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["nombre"]),
        "Nombre: ",
    )
    apellido = solicitar_input(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["apellido"]),
        "Apellido: ",
    )
    dni = solicitar_input(validar_dni, "DNI: ")
    domicilio = solicitar_datos_domicilio()
    return (
        nombre,
        apellido,
        dni,
        domicilio["Calle"],
        domicilio["Altura"],
        domicilio["Piso"],
        domicilio["Departamento"],
        domicilio["Localidad"],
        domicilio["Provincia"],
    )


def comprobar_bisiesto(anio: int) -> bool:
    """Comprueba si un año es bisiesto.

    Pre: Recibe el año como un número entero.

    Post: Si el entero es divisible por cuatro y no es divisible
          por 100, o es divisible por 400 es bisiesto y devuelve True, si no False.

    """
    return (anio % 4 == 0) and (anio % 100 != 0) or (anio % 400 == 0)


def verificar_fecha_valida(dia: int, mes: int, anio: int) -> bool:
    """Valida si la fecha dada es correcta según el formato DDMMAAAA.

    Pre: fecha debe ser un string en formato DDMMAAAA.

    Post: Retorna True si la fecha es válida, y False en caso contrario,
          considerando el número de días de cada mes y los años bisiestos.

    """
    if comprobar_bisiesto(anio):
        meses.update({2: 29})
    return (mes in meses) and (dia <= meses.get(mes))


def pedir_num(msj: str) -> int:
    """Pide un numero al usuario y lo devuelve.

    Pre: No recibe nada.

    Post: Devuelve n un numero entero.

    """
    while True:
        try:
            n = int(input(msj))
            if n > 0:
                break
        except ValueError:
            print("Debe ingresar un numero valida.")
    return n


def pedir_fecha(msj: str) -> str:
    """Pide un numero al usuario y lo devuelve.

    Pre: No recibe nada.

    Post: Devuelve n un numero entero.

    """
    while True:
        try:
            fecha = input(msj)
            if len(fecha) == 8 and fecha.isdigit():
                break
            raise ValueError()
        except ValueError:
            print("Debe ingresar una fecha valida. En formato DDMMAAAA.")
    return fecha


def validar_fecha(fecha_inicio: List[str], fecha_fin: List[str] = None) -> bool:
    """Valida que la fecha de inicio sea mayor a la actual o que la fecha de fin sea mayor que la de inicio.

    Pre: fecha_inicio y fecha_fin son listas en el formato [DD, MM, AAAA].
         Si fecha_fin no se proporciona, se compara fecha_inicio con la fecha actual.

    Post: Retorna True si la fecha de fin es mayor a la de inicio, o si la fecha de inicio es mayor a la actual.

    """
    anio_i, mes_i, dia_i = fecha_inicio[2], fecha_inicio[1], fecha_inicio[0]
    if fecha_fin is None:
        anio_actual, mes_actual, dia_actual = str(datetime.now().date()).split("-")
        return (anio_i, mes_i, dia_i) > (anio_actual, mes_actual, dia_actual)
    anio_f, mes_f, dia_f = fecha_fin[2], fecha_fin[1], fecha_fin[0]
    return (anio_f, mes_f, dia_f) > (anio_i, mes_i, dia_i)


def validar_ingreso_fecha(msj: str) -> List[int]:
    while True:
        try:
            fecha = re.split(r"(\d{2})(\d{2})(\d{4})", pedir_fecha(msj))[1:-1]
            if verificar_fecha_valida(
                int(fecha[0]), int(fecha[1]), int(fecha[2])
            ) and validar_fecha(fecha):
                break
            raise ValueError("Ingrese una fecha valida.")
        except ValueError as e:
            print(e)
    return fecha


def registrar_reserva(reservas: List[Dict]):
    """Registra una nueva reserva en la lista de reservas.

    Pre: reservas es una lista de diccionarios que contiene todas las reservas.

    Post: Agrega una nueva reserva a la lista de reservas con todos los datos validados.

    """
    nombre, apellido, dni, calle, altura, piso, dpto, localidad, provincia = (
        solicitar_datos_cliente()
    )
    print(nombre, apellido, dni, calle, altura, piso, dpto, localidad, provincia)
    n_habitacion = pedir_num("Ingrese el número de habitación donde se alojará: ")
    fecha_reserva = str(datetime.now().date()).replace("-", "/")
    while True:
        try:
            fecha_i = validar_ingreso_fecha(
                "Ingrese el inicio de la estadía (DDMMAAAA): "
            )
            fecha_f = validar_ingreso_fecha("Ingrese el fin de la estadía (DDMMAAAA): ")
            if validar_fecha(fecha_i, fecha_f):
                break
            raise ValueError(
                "Error: La fecha de fin debe ser posterior a la fecha de inicio."
            )
        except ValueError as e:
            print(e)
    reserva = {
        "ID": len(reservas)+1,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "provincia": provincia,
        "localidad": localidad,
        "calle": calle,
        "altura": altura,
        "piso": piso if piso else '',
        "departamento": dpto if dpto else '',
        "n_habitacion": n_habitacion,
        "fecha_reserva": fecha_reserva,
        "fecha_inicio": "/".join(fecha_i),
        "fecha_fin": "/".join(fecha_f),
    }
    reservas.append(reserva)
    print("Reserva registrada con éxito.")
    return reservas


def consultar_reserva(reservas: List[Dict]):
    nombre = solicitar_input(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["nombre"]),
        "Nombre: ",
    )
    apellido = solicitar_input(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["apellido"]),
        "Apellido: ",
    )
    reserva_encontrada = list(reserva for reserva in reservas if reserva['nombre'] == nombre and reserva['apellido'] == apellido)
    if not reserva_encontrada:
        return 0
    return reserva_encontrada[0]['ID']


def anular_reserva(reservas: List[Dict]):
    if consultar_reserva(reservas):
        
        return reservas


def registrar_check_in(reservas: List[Dict]):
    pass


def registrar_check_out(reservas: List[Dict]):
    pass
>>>>>>> e60989d (Registro de reservas terminado y consulta de reservas tambien. reservas.json ahora tiene estado y consumos.)
