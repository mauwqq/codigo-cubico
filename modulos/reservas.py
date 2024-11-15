from typing import Tuple, Callable, Dict, List
import re
from datetime import datetime
from tabulate import tabulate
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

validaciones_errores = {
    "nombre": {
        "patron": r"^[a-zA-Z]+$",
        "mensajes": {
            "vacío": "El nombre no puede estar vacío.",
            "invalido": "El nombre debe ser una sola palabra sin espacios ni símbolos.",
            "sin_numeros": "El nombre no puede contener números.",
            "sin_simbolos": "El nombre no puede contener símbolos.",
        },
        "verificar_longitud": True,
    },
    "apellido": {
        "patron": r"^[a-zA-Z]+$",
        "mensajes": {
            "vacío": "El apellido no puede estar vacío.",
            "invalido": "El apellido debe ser una sola palabra sin espacios ni símbolos.",
            "sin_numeros": "El apellido no puede contener números.",
            "sin_simbolos": "El apellido no puede contener símbolos.",
        },
        "verificar_longitud": True,
    },
    "domicilio": {
        "Calle": {
            "patron": r"^[a-zA-Z0-9 ]+$",
            "mensajes": {
                "vacío": "La calle no puede estar vacía.",
                "sin_simbolos": "La calle no puede contener símbolos.",
            },
            "permitir_vacio": False,
        },
        "Altura": {
            "patron": r"^\d+$",
            "mensajes": {
                "vacío": "La altura no puede estar vacía.",
                "sin_simbolos": "La altura no puede contener símbolos.",
                "invalido": "La altura no debe contener letras.",
            },
            "permitir_vacio": False,
        },
        "Piso": {
            "patron": r"^\d*$",
            "mensajes": {"sin_simbolos": "El piso no puede tener símbolos."},
            "permitir_vacio": True,
        },
        "Departamento": {
            "patron": r"^[a-zA-Z0-9 ]*$",
            "mensajes": {"sin_simbolos": "El departamento no puede tener símbolos."},
            "permitir_vacio": True,
        },
        "Localidad": {
            "patron": r"^[a-zA-Z0-9 ]+$",
            "mensajes": {
                "vacío": "La localidad no puede estar vacía.",
            },
            "permitir_vacio": False,
        },
        "Provincia": {
            "patron": r"^[a-zA-Z ]+$",
            "mensajes": {"vacío": "La provincia no puede estar vacía."},
            "permitir_vacio": False,
        },
    },
    "dni": {
        "patron": r"^\d{7,8}$",
        "mensajes": {
            "vacío": "El DNI no puede estar vacío.",
            "longitud": "El DNI debe contener solo números y tener entre 7 y 8 caracteres.",
        },
        "verificar_longitud": True,
    },
    "n_habitacion": {
        "patron": r"^\d+$",
        "mensajes": {
            "vacío": "El número de habitación no puede estar vacío.",
            "invalido": "El número de habitación debe contener solo dígitos.",
            "sin_simbolos": "El número de habitación no puede contener símbolos ni letras.",
        },
    },
}


def solicitar_input(validacion: Callable[[str], str], msj: str) -> str:
    """Solicita un valor al usuario y lo valida con la función dada.

    Pre: validacion es una función que recibe una cadena y devuelve una cadena.
         msj es un mensaje que se muestra al usuario.

    Post: Retorna el valor validado ingresado por el usuario.

    Raises: ValueError si la entrada no es válida según la función de validación proporcionada.

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
    """Valida un valor con una expresión regular y mensajes personalizados.

    Pre: patron es una cadena que representa la expresión regular para la validación.
         valor es la cadena que se valida.
         mensajes es un diccionario con mensajes de error personalizados.
         verificar_longitud es un booleano que indica si se debe verificar la longitud mínima.
         permitir_vacio es un booleano que indica si se permite un valor vacío.

    Post: Retorna el valor validado, formateado correctamente.

    Raises: ValueError si el valor no cumple con las condiciones de validación.

    """
    valor = valor.strip()
    if permitir_vacio and not valor:
        return ""
    if not valor:
        raise ValueError(mensajes.get("vacío", "El campo no puede estar vacio."))
    if not re.match(patron, valor):
        if any(char.isdigit() for char in valor):
            raise ValueError(
                mensajes.get("sin_numeros", "El campo no puede contener números.")
            )
        if not re.match(r"^[a-zA-Z0-9 ]+$", valor):
            raise ValueError(
                mensajes.get("sin_simbolos", "El campo no puede contener símbolos.")
            )
        raise ValueError(mensajes["invalido"])
    if verificar_longitud and len(valor) < 3:
        raise ValueError("El campo debe tener al menos tres letras.")
    return valor.title()


def validar_campo(campo: str, valor: str) -> str:
    """Valida un campo de datos, incluyendo los campos de domicilio.

    Pre: campo es una cadena que representa el nombre del campo a validar.
         valor es la cadena que se valida.

    Post: Retorna el valor validado del campo.

    Raises: ValueError si el campo no cumple con las condiciones de validación definidas.

    """
    es_domicilio = campo in validaciones_errores["domicilio"]
    validacion = (
        validaciones_errores["domicilio"][campo]
        if es_domicilio
        else validaciones_errores[campo]
    )
    patron = validacion["patron"]
    mensajes = validacion["mensajes"]
    permitir_vacio = validacion.get("permitir_vacio", False)
    verificar_longitud = validacion.get("verificar_longitud", False)
    return validar_con_regex(
        patron, valor, mensajes, verificar_longitud, permitir_vacio
    )


def validar_dni(dni: str) -> int:
    """Valida que el DNI ingresado tenga el formato correcto.

    Pre: dni es una cadena que representa el DNI.

    Post: Retorna el DNI como un entero si es válido.

    Raises: ValueError si el DNI no es válido.

    """
    dni = re.sub(r"\D", "", dni)
    if not dni:
        raise ValueError("El DNI no puede estar vacío.")
    if len(dni) > 8 or len(dni) < 7:
        raise ValueError("El DNI debe contener entre 7 o 8 caracteres numéricos.")
    return int(dni)


def solicitar_datos_domicilio() -> Dict[str, str]:
    """Solicita y valida los datos de domicilio del usuario.

    Pre: No recibe parámetros.

    Post: Retorna un diccionario con los datos de domicilio validados.

    Raises: ValueError si alguno de los campos de domicilio no es válido.

    """
    print("Domicilio")
    campos = [
        "Provincia",
        "Localidad",
        "Calle",
        "Altura",
        "Piso",
        "Departamento",
    ]
    # Estructura generada
    # {'Provincia': '', 'Localidad': '', 'Calle': '', 'Altura': '0', 'Piso': '0', 'Departamento': '0'}
    return {
        campo: solicitar_input(
            lambda x: validar_campo(campo, x),
            (
                f"{campo}: "
                if validaciones_errores["domicilio"]
                .get(campo, {})
                .get("mensajes", {})
                .get("vacío", "")
                else f"{campo} ('Enter' si no aplica): "
            ),
        )
        for campo in campos
    }


def solicitar_datos_cliente() -> Tuple[str, str, int, str, str, str, str, str, str]:
    """Solicita y valida los datos del cliente.

    Pre: No recibe parámetros.

    Post: Retorna una tupla con los datos del cliente validados.

    Raises: ValueError si alguno de los campos del cliente no es válido.

    """
    nombre = solicitar_input(lambda x: validar_campo("nombre", x), "Nombre: ")
    apellido = solicitar_input(lambda x: validar_campo("apellido", x), "Apellido: ")
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


def verificar_fecha_valida(dia: int, mes: int, anio: int) -> bool:
    """Valida si la fecha dada es correcta según el formato DDMMAAAA.

    Pre: dia, mes y anio son enteros que representan la fecha.

    Post: Retorna True si la fecha es válida, y False en caso contrario,
          considerando el número de días de cada mes y los años bisiestos.

    """
    if (not (anio % 4) and (anio % 100 != 0)) or not (anio % 400):
        meses.update({2: 29})
    return (mes in meses) and (dia <= meses.get(mes))


def pedir_fecha(msj: str) -> str:
    """Pide una fecha al usuario en formato DDMMAAAA y la devuelve.

    Pre: msj es un mensaje que se muestra al usuario para solicitar la fecha.

    Post: Devuelve la fecha ingresada como una cadena.

    Raises: ValueError si la fecha no está en el formato correcto.

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
    """Valida que la fecha de inicio sea mayor a la actual o que la fecha de fin
    sea mayor que la de inicio.

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
    """Valida y solicita una fecha de ingreso al usuario.

    Pre: msj es un mensaje que se muestra al usuario para solicitar la fecha.

    Post: Retorna una lista con la fecha ingresada en formato [DD, MM, AAAA].
          Si la fecha ingresada no es válida, solicita nuevamente la entrada hasta que sea correcta.

    Raises: ValueError si la fecha no pasa la verificacion.

    """
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


def habitacion_desocupada(n: int) -> bool:
    """Verifica si una habitación está desocupada revisando las reservas.

    Pre: n es un numero entero.

    Post: True si la habitacion no esta ocupada, de lo contrario False.

    """
    reservas = tablas_del_sistema.cargar_data("data/reservas.json")
    if not reservas:
        return True
    reservas_habitacion = [
        reserva for reserva in reservas if reserva["habitacion"] == str(n)
    ]
    if not reservas_habitacion:
        return True
    if any(
        reserva["estado"] not in ["anulada", "desocupada"]
        for reserva in reservas_habitacion
    ):
        return False
    return True


def habitacion() -> int:
    """Pide un numero de habitacion hasta que se ingrese uno valido y lo devuelve.

    Pre: No recibe nada.

    Post: Devuelve un numero entero.

    Raises: ValueError si la habitacion no existe.

    """
    habitaciones = tablas_del_sistema.cargar_data("data/habitaciones.csv")
    if not habitaciones:
        return 0
    while True:
        try:
            n_habitacion = solicitar_input(
                lambda x: validar_campo("n_habitacion", x), "Número de habitación: "
            )
            if str(n_habitacion) not in [
                habitacion["NUMERO_HABITACION"] for habitacion in habitaciones
            ]:
                raise ValueError(f"La habitacion {n_habitacion} no existe.")
            if not habitacion_desocupada(n_habitacion):
                raise ValueError("La habitacion se encuentra ocupada.")
            break
        except ValueError as e:
            print(e)
    return n_habitacion


def registrar_reserva(reservas: List[Dict]) -> None:
    """Registra una nueva reserva en la lista de reservas.

    Pre: reservas es una lista de diccionarios que contiene todas las reservas.

    Post: Añade la reserva y la carga a el json con cargar_data(), devuelve None.

    """
    if not reservas:
        return None
    nombre, apellido, dni, calle, altura, piso, dpto, localidad, provincia = (
        solicitar_datos_cliente()
    )
    n_habitacion = habitacion()
    if not n_habitacion:
        return None
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
    listado_productos = tablas_del_sistema.cargar_data("data/productos.csv")
    reserva = {
        "ID": str(len(reservas) + 1),
        "nombre": nombre,
        "apellido": apellido,
        "dni": str(dni),
        "provincia": provincia,
        "localidad": localidad,
        "calle": calle,
        "altura": altura,
        "piso": piso if piso else "",
        "departamento": dpto if dpto else "",
        "habitacion": str(n_habitacion),
        "fecha_reserva": fecha_reserva,
        "fecha_inicio": "/".join(fecha_i),
        "fecha_fin": "/".join(fecha_f),
        "estado": "reservada",
        "consumos": [0 for producto in listado_productos] if listado_productos else [0],
    }
    reservas.append(reserva)
    tablas_del_sistema.guardar_data(reservas, "data/reservas.json")
    print("Reserva registrada con éxito.")
    return None


def consultar_reserva(reservas: List[Dict]) -> int:
    """Pide el nombre y apellido del huesped y busca si tiene una reserva hecha,
    si la encuentra la devuelve, sino devuelve 0.

    Pre: reservas es la lista de diccionarios donde cada diccionario es una reserva.

    Post: Si encuentra la reserva, devuelve el id de la reserva, sino, devuelve 0.

    """
    nombre = solicitar_input(lambda x: validar_campo("nombre", x), "Nombre: ")
    apellido = solicitar_input(lambda x: validar_campo("apellido", x), "Apellido: ")
    reserva_encontrada = list(
        reserva
        for reserva in reservas
        if reserva["nombre"] == nombre and reserva["apellido"] == apellido
    )
    if not reserva_encontrada:
        return 0
    return int(reserva_encontrada[0]["ID"])


def datos_reserva() -> None:
    """
    Muestra los detalles de una reserva, según el ID consultado en la lista de reservas.
    Si no se encuentra la reserva o no se ingresa un ID válido, no se muestra nada.

    Pre: No recibe nada.

    Post: None.

    """
    reservas = tablas_del_sistema.cargar_data("data/reservas.json")
    if not reservas:
        return None
    id_ = consultar_reserva(reservas)
    if not id_:
        print("No se ingresó un ID válido.")
        return None
    reserva = next((reserva for reserva in reservas if reserva["ID"] == str(id_)), None)
    if reserva:
        print(tabulate([reserva], headers="keys", tablefmt="grid"))
    else:
        print(f"No se encontró una reserva con el ID {id_}.")
    return None


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


def registrar_check_in(reservas: List[Dict]) -> None:
    """Registra el check-in de un huésped en la lista de reservas.

    Pre: reservas es una lista de diccionarios que contiene todas las reservas.

    Post: Actualiza el estado de la reserva a 'check-in' si se encuentra y está reservada.
          Si no se encuentra la reserva, muestra un mensaje informando de ello.

    """
    id_reserva = consultar_reserva(reservas)
    if not id_reserva:
        print("No se encontró ninguna reserva con esos datos.")
        return None
    for reserva in reservas:
        if reserva["ID"] == str(id_reserva) and reserva["estado"] == "reservada":
            reserva["estado"] = "check-in"
            print(f"Check-in realizado con éxito para la reserva N{reserva['ID']}.")
            tablas_del_sistema.guardar_data(reservas, "data/reservas.json")
            return None
    print("No se encontró una reserva 'reservada' con esos datos.")


def registrar_check_out(reservas: List[Dict]) -> None:
    """Registra el check-out de un huésped en la lista de reservas.

    Pre: reservas es una lista de diccionarios que contiene todas las reservas.

    Post: Actualiza el estado de la reserva a 'check-out' si se encuentra y está en progreso.
          Si no se encuentra la reserva, muestra un mensaje informando de ello.

    """
    id_reserva = consultar_reserva(reservas)
    if not id_reserva:
        print("No se encontró ninguna reserva con esos datos.")
        return None
    for reserva in reservas:
        if reserva["ID"] == id_reserva and reserva["estado"] == "check-in":
            reserva["estado"] = "desocupada"
            print(f"Check-out realizado con éxito para la reserva N{reserva['ID']}.")
            tablas_del_sistema.guardar_data(reservas, "data/reservas.json")
            return None
    print("No se encontró una reserva en estado 'check-in' con esos datos.")
