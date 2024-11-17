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

validaciones = {
    "Nombre": {
        "patron": r"^[a-zA-Z]+$",
        "mensajes": {
            "vacio": "El nombre no puede estar vacío.",
            "invalido": "El nombre debe ser una sola palabra sin espacios ni símbolos.",
            "sin_numeros": "El nombre no puede contener números.",
            "sin_simbolos": "El nombre no puede contener símbolos.",
        },
        "verificar_longitud": True,
        "sin_numeros": True,
        "sin_simbolos": True,
    },
    "Apellido": {
        "patron": r"^[a-zA-Z]+$",
        "mensajes": {
            "vacio": "El apellido no puede estar vacío.",
            "invalido": "El apellido debe ser una sola palabra sin espacios ni símbolos.",
            "sin_numeros": "El apellido no puede contener números.",
            "sin_simbolos": "El apellido no puede contener símbolos.",
        },
        "verificar_longitud": True,
        "sin_numeros": True,
        "sin_simbolos": True,
    },
    "domicilio": {
        "Calle": {
            "patron": r"^[a-zA-Z0-9 ]+$",
            "mensajes": {
                "vacio": "La calle no puede estar vacía.",
                "sin_simbolos": "La calle no puede contener símbolos.",
                "invalido": "Ingrese una calle valida.",
            },
            "sin_simbolos": True,
        },
        "Altura": {
            "patron": r"^\d+$",
            "mensajes": {
                "vacio": "La altura no puede estar vacía.",
                "sin_simbolos": "La altura no puede contener símbolos.",
                "invalido": "La altura no debe contener letras.",
            },
            "sin_simbolos": True,
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
                "vacio": "La localidad no puede estar vacía.",
            },
            "sin_simbolos": True,
        },
        "Provincia": {
            "patron": r"^[a-zA-Z0-9 ]+$",
            "mensajes": {"vacio": "La provincia no puede estar vacía."},
            "sin_simbolos": True,
        },
    },
    "Mail": {
        "patron": r"^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$",
        "mensajes": {
            "vacio": "El mail no puede estar vacio.",
            "invalido": "Ingrese un mail valido.",
        },
        "verificar_longitud": True,
    },
    "Telefono": {
        "patron": r"^\+[0-9]{11,15}$",
        "mensajes": {
            "vacio": "El telefono no puede estar vacio.",
            "invalido": "Ingrese un telefono valido.",
        },
        "verificar_longitud": True,
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


def validar_regex(patron: str, valor: str) -> bool:
    """Se le da un patron regex y un dato, comprueba si el dato cumple con el patron.

    Pre: patron es un string.
         valor es un string.

    Post: Devuelve un booleano.

    """
    return bool(re.match(patron, valor))


def validar(
    patron: str,
    valor: str,
    mensajes: Dict[str, str],
    verificar_longitud: bool = False,
    permitir_vacio: bool = False,
    sin_numeros: bool = False,
    sin_simbolos: bool = False,
) -> str:
    """Valida un valor con una expresión regular y mensajes personalizados.

    Pre: patron es una cadena que representa la expresión regular para la validación.
         valor es la cadena que se valida.
         mensajes es un diccionario con mensajes de error personalizados.
         verificar_longitud es un booleano que indica si se debe verificar la longitud mínima.
         permitir_vacio es un booleano que indica si se permite un valor vacío.
         sin_numeros es un booleano que indica si se debe verificar que no tenga numeros.
         sin_simbolos es un booleano que indica si se debe verificar que no tenga simbolos.

    Post: Retorna el valor validado, formateado correctamente.

    Raises: ValueError si el valor no cumple con las condiciones de validación.

    """
    valor = valor.strip()
    if permitir_vacio and not valor:
        return ""
    if not valor:
        raise ValueError(mensajes.get("vacío", "El campo no puede estar vacio."))

    if sin_numeros and any(char.isdigit() for char in valor):
        raise ValueError(
            mensajes.get("sin_numeros", "El campo no puede contener números.")
        )
    if sin_simbolos and not validar_regex(r"^[a-zA-Z0-9 ]+$", valor):
        raise ValueError(
            mensajes.get("sin_simbolos", "El campo no puede contener símbolos.")
        )
    if not validar_regex(patron, valor):
        raise ValueError(mensajes["invalido"])
    if verificar_longitud and len(valor) < 3:
        raise ValueError("El campo debe tener al menos tres letras.")
    return valor.title()


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


def solicitar_datos_cliente() -> Tuple[str, str, int, str, str, str, str, str, str]:
    """Solicita y valida los datos del cliente.

    Pre: No recibe parámetros.

    Post: Retorna una tupla con los datos del cliente validados.

    """
    resultados = {}
    for campo, config in validaciones.items():
        if isinstance(
            config, dict
        ):  # Comprueba si el campo que esta comprobando es un dicionario.
            if all(
                isinstance(subconfig, dict) for subconfig in config.values()
            ):  # Comprueba si todos los valores de un diccionario son diccionarios.
                resultados[campo] = {}
                for subcampo, subconfig in config.items():
                    resultados[campo][subcampo] = solicitar_input(
                        lambda x: validar(
                            subconfig["patron"],
                            x,
                            subconfig["mensajes"],
                            verificar_longitud=subconfig.get(
                                "verificar_longitud", False
                            ),
                            permitir_vacio=subconfig.get("permitir_vacio", False),
                            sin_numeros=subconfig.get("sin_numeros", False),
                            sin_simbolos=subconfig.get("sin_simbolos", False),
                        ),
                        f"{subcampo}: ",
                    )
            else:
                resultados[campo] = solicitar_input(
                    lambda x: validar(
                        config["patron"],
                        x,
                        config["mensajes"],
                        verificar_longitud=config.get("verificar_longitud", False),
                        permitir_vacio=config.get("permitir_vacio", False),
                        sin_numeros=config.get("sin_numeros", False),
                        sin_simbolos=config.get("sin_simbolos", False),
                    ),
                    f"{campo}: ",
                )
    dni = solicitar_input(lambda x: validar_dni(x), "DNI: ")
    return (
        resultados["Nombre"],
        resultados["Apellido"],
        dni,
        resultados["Mail"].lower(),
        resultados["Telefono"],
        resultados["domicilio"]["Calle"],
        resultados["domicilio"]["Altura"],
        resultados["domicilio"]["Piso"],
        resultados["domicilio"]["Departamento"],
        resultados["domicilio"]["Localidad"],
        resultados["domicilio"]["Provincia"],
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


def habitacion() -> str:
    """Pregunta en que habitacion se va a alojar el huesped y si existe la habitacion
    y no esta ocupada devuelve el numero de habitacion.

    Pre: Ninguno.

    Post: Devuelve un string.

    Raises: ValueError: Si no se encontraron habitaciones disponibles,
            si el numero ingresado no es un numero,
            si el numero de habitacion no corresponde a una habitacion,
            si la habitacion esta ocupada.

    """
    habitaciones = tablas_del_sistema.cargar_data("data/habitaciones.csv")
    if not habitaciones:
        raise ValueError("No se encontraron habitaciones disponibles.")
    while True:
        try:
            n_habitacion = input("Ingrese el número de habitación: ").strip()
            if not n_habitacion.isdigit():
                raise ValueError("El número de habitación debe ser un valor numérico.")
            n_habitacion = int(n_habitacion)
            if str(n_habitacion) not in [
                habitacion["NUMERO_HABITACION"] for habitacion in habitaciones
            ]:
                raise ValueError(f"La habitación {n_habitacion} no existe.")
            if not habitacion_desocupada(n_habitacion):
                raise ValueError(f"La habitación {n_habitacion} está ocupada.")
            break
        except ValueError as e:
            print(e)
    return str(n_habitacion)


def registrar_cliente(
    nombre: str,
    apellido: str,
    dni: int,
    localidad: str,
    provincia: str,
    calle: str,
    altura: str,
    piso: str,
    dpto: str,
    tel: str,
    mail: str,
) -> None:
    """Registra los datos del cliente que esta reservando, en el archivo data/clientes.csv.

    Pre: nombre, apellido, localidad, provincia, calle, altura, piso, dpto, tel, mail son strings.
         dni es un entero.

    Post: No devuelve nada.

    """
    clientes = tablas_del_sistema.cargar_data("data/clientes.csv")
    clientes.append(
        {
            "ID": f"{str(len(clientes)+1)}",
            "NOMBRE": nombre,
            "APELLIDO": apellido,
            "DNI": str(dni),
            "LOCALIDAD": localidad,
            "PROVINCIA": provincia,
            "CALLE": calle,
            "PISO": piso,
            "ALTURA": altura,
            "DPTO": dpto,
            "TELEFONO": tel,
            "MAIL": mail,
        }
    )
    tablas_del_sistema.guardar_data(clientes, "data/clientes.csv")
    print("Cliente añadido correctamente.")
    return None


def registrar_reserva(reservas: List[Dict]) -> None:
    """Registra una nueva reserva en la lista de reservas.

    Pre: reservas es una lista de diccionarios que contiene todas las reservas.

    Post: Añade la reserva y la carga a el json con cargar_data(), devuelve None.

    """
    if not reservas:
        return None
    (
        nombre,
        apellido,
        dni,
        mail,
        tel,
        calle,
        altura,
        piso,
        dpto,
        localidad,
        provincia,
    ) = solicitar_datos_cliente()
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
    registrar_cliente(
        nombre,
        apellido,
        dni,
        localidad,
        provincia,
        calle,
        altura,
        piso,
        dpto,
        tel,
        mail,
    )
    return None


def consultar_reserva(reservas: List[Dict]) -> int:
    """Pide el nombre y apellido del huesped y busca si tiene una reserva hecha,
    si la encuentra la devuelve, sino devuelve 0.

    Pre: reservas es la lista de diccionarios donde cada diccionario es una reserva.

    Post: Si encuentra la reserva, devuelve el id de la reserva, sino, devuelve 0.

    """
    nombre = solicitar_input(
        lambda x: validar(
            validaciones["Nombre"]["patron"],
            x,
            validaciones["Nombre"]["mensajes"],
            verificar_longitud=True,
            sin_numeros=True,
            sin_simbolos=True,
        ),
        "Nombre: ",
    )
    apellido = solicitar_input(
        lambda x: validar(
            validaciones["Apellido"]["patron"],
            x,
            validaciones["Apellido"]["mensajes"],
            verificar_longitud=True,
            sin_numeros=True,
            sin_simbolos=True,
        ),
        "Apellido: ",
    )
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
