from typing import Tuple, Callable, Dict, List
import re


def pedir(validar: Callable[[str], str], msj: str) -> str:
    """Solicita un valor al usuario y lo valida con la función dada.

    Pre: validar es una función que recibe una cadena y devuelve una cadena.
         msj es un mensaje que se muestra al usuario.

    Post: Retorna el valor validado ingresado por el usuario.

    """
    while True:
        try:
            return validar(input(msj))
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
    if permitir_vacio and valor == "":
        return ""
    if not valor:
        raise ValueError(mensajes["vacío"])
    if not re.match(patron, valor):
        raise ValueError(mensajes["invalido"])
    if verificar_longitud and len(valor) < 3:
        raise ValueError("El campo debe tener al menos tres letras.")
    return valor.title()


def validar_dni(dni: str) -> int:
    """Valida que el DNI ingresado tenga el formato correcto.

    Pre: dni es una cadena que representa el DNI.

    Post: Retorna el DNI como un entero si es válido.
          ValueError si el DNI no es válido.

    """
    dni = re.sub(r'\D', '', dni)
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
            "La altura debe ser un número entero.",
            "La altura no puede estar vacía.",
        ),
        "Piso": (r"^\d*$", "Ingrese un piso válido.", "El piso no puede estar vacío."),
        "Departamento": (
            r"^[a-zA-Z0-9 ]*$",
            "El departamento no puede tener símbolos.",
            "",
        ),
        "Localidad": (
            r"^[a-zA-Z0-9 ]+$",
            "Debe ingresar una localidad.",
            "La localidad no puede estar vacía.",
        ),
        "Provincia": (
            r"^[a-zA-Z ]+$",
            "Debe ingresar una provincia.",
            "La provincia no puede estar vacía.",
        ),
    }
    patron, mensaje_vacio, mensaje_invalido = validaciones[campo]
    verificar_longitud = campo != "Altura"
    permitir_vacio = campo in ["Piso", "Departamento"]
    return validar_con_regex(
        patron,
        valor,
        {"vacío": mensaje_vacio, "invalido": mensaje_invalido},
        verificar_longitud,
        permitir_vacio,
    )


def pedir_datos_domicilio() -> Tuple[str, int, int, str, str, str]:
    """Solicita y valida los datos de domicilio al usuario.

    Post: Retorna una tupla con los datos de domicilio:
          (Calle, Altura, Piso, Departamento, Localidad, Provincia).

    """
    print("Domicilio")
    datos_domicilio = [
        pedir(
            lambda x: validar_domicilio(campo, x), f"{campo} ('Enter' si no aplica): "
        )
        for campo in [
            "Calle",
            "Altura",
            "Piso",
            "Departamento",
            "Localidad",
            "Provincia",
        ]
    ]
    return tuple(datos_domicilio)


def pedir_datos_cliente() -> Tuple[str, str, int, str, int, int, str, str, str]:
    """Solicita y valida los datos del cliente.

    Post: Retorna una tupla con los datos del cliente:
          (Nombre, Apellido, DNI, Calle, Altura, Piso, Departamento, Localidad, Provincia).

    """
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
    nombre = pedir(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["nombre"]),
        "Nombre: ",
    )
    apellido = pedir(
        lambda x: validar_con_regex(r"^[a-zA-Z]+$", x, errores["apellido"]),
        "Apellido: ",
    )
    dni = pedir(validar_dni, "DNI: ")
    # El '*' o 'unpacking' expande la tupla con los valores que retorna pedir_datos_domicilio().
    return (nombre, apellido, dni, *pedir_datos_domicilio())


def registrar_reserva(reservas: List[Dict]):
    pass


def consultar_reserva(reservas: List[Dict]):
    pass


def anular_reserva(reservas: List[Dict]):
    pass


def registrar_check_in(reservas: List[Dict]):
    pass


def registrar_check_out(reservas: List[Dict]):
    pass


if __name__ == "__main__":
    print(pedir_datos_cliente())
