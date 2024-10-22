from typing import Tuple, Callable, Dict, List
import re
from datetime import datetime
from modulos import tablas_del_sistema

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

    Pre: validar es una función que recibe una cadena y devuelve una cadena.
         msj es un mensaje que se muestra al usuario.

    Post: Retorna el valor validado ingresado por el usuario.

    """
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


def validar_dni(dni: str) -> int:  # dni tambien puede ser len(7)
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

    Post: Retorna True si la fecha de fin es mayor a la de inicio, o si la fecha de
          inicio es mayor a la actual. 

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
        "ID": len(reservas) + 1,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "provincia": provincia,
        "localidad": localidad,
        "calle": calle,
        "altura": altura,
        "piso": piso if piso else "",
        "departamento": dpto if dpto else "",
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
    reserva_encontrada = list(
        reserva
        for reserva in reservas
        if reserva["nombre"] == nombre and reserva["apellido"] == apellido
    )
    if not reserva_encontrada:
        return 0
    return reserva_encontrada[0]["ID"]


def anular_reserva(reservas: List[Dict]) -> None:
    """Anula una reserva cambiando su estado a 'cancelada'.

    Pre: reservas es la lista de diccionarios donde cada diccionario es una reserva.

    Post: Si encuentra la reserva, cambia el estado a 'cancelada' y la retorna.
          Si no encuentra la reserva, devuelve la lista original.

    """
    id_reserva = consultar_reserva(reservas)
    if not id_reserva:
        print("No se encontró ninguna reserva con esos datos.")
        return None
    for reserva in reservas:
        if reserva["ID"] == str(id_reserva):
            reserva["estado"] = "cancelada"
            print(f"Reserva {id_reserva} cancelada exitosamente.")
            tablas_del_sistema.guardar_data(reservas, "data/reservas.json")
    return None


def registrar_check_in(reservas: List[Dict]):
    pass


def registrar_check_out(reservas: List[Dict]):
    pass
