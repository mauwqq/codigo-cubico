from datetime import datetime
from modulos import menu
from typing import List, Dict, Tuple


def pedir(valid, inpt: str,  err: str):
    try:
        val = valid(input(inpt))
        return val
    except Exception as _:
        _ = None
        print(err)
        pedir(valid, inpt, err)
        return _


def valid_dni(val) -> int:
    if not (int(val) > 0) and not (len(val) == 8):
        raise ValueError("Inserte un DNI valido.")
    return int(val)


def pedir_nombre(valor: str) -> str:
    if not valor:
        raise ValueError(f"El {valor} no puede estar vacío.")
    if any(c.isdigit() for c in valor):
        raise ValueError(f"El {valor} no puede contener números.")
    return valor


def pedir_datos_domicilio() -> Tuple[str, int, int, str, str, str]:
    print("Domicilio")

    def calle_valida(d_calle):
        if not d_calle:
            raise ValueError("Debe ingresar una calle valida.")
        return d_calle
    d_calle = pedir(calle_valida, "calle:", "calle valida")

    def num_valido(d_numero):
        if not d_numero.isdigit() or int(d_numero) <= 0:
            raise ValueError("Debe ingresar una altura válida.")
        return d_numero

    d_numero = pedir(num_valido, "Ingrese la altura: ", "da una altura valida")

    def piso_valido(d_piso):
        d_piso = int(d_piso) if d_piso.isdigit() else 0
        return d_piso
    d_piso = pedir(piso_valido, "Ingrese el piso ('Enter' para 0): ", "no era un numero")

    def dpt_valido(d_dpto):
        d_dpto = d_dpto if d_dpto else 0
        return d_dpto
    d_dpto = pedir(dpt_valido, "Departamento ('Enter' si no aplica): ", "error")

    def localidad_valida(localidad):
        if not localidad:
            raise ValueError("Debe ingresar una Localidad.")
        return localidad

    localidad = pedir(localidad_valida, "Localidad: ", "error")

    def provincia_valida(provincia):
        if not provincia:
            raise ValueError("Debe ingresar una provincia.")
        return provincia

    provincia = pedir(provincia_valida, "Provincia: ", "error")

    return (d_calle, d_numero, d_piso, d_dpto, localidad, provincia)


def pedir_datos_cliente() -> Tuple[str, str]:
    nombre = pedir(pedir_nombre, "nombre:", "no puede contener numeros")
    apellido = pedir(pedir_nombre, "apellido:", "no puede contener numeros")
    dni = pedir(valid_dni, "dni:", "Dni es 8 numeros")
    d_calle, d_numero, d_piso, d_dpto, localidad, provincia = pedir_datos_domicilio()
    return (
        nombre,
        apellido,
        dni,
        d_calle,
        d_numero,
        d_piso,
        d_dpto,
        localidad,
        provincia,
    )


def pedir_dni() -> int:
    while True:
        try:
            dni = int(input("Ingrese el DNI sin puntos: "))
            if (dni > 0) and (len(str(dni)) == 8):
                break
            print("Debe ingresar un numero valido.")
        except ValueError:
            print("Debe ingresar un numero.")
    return dni


def pedir_nombre_apellido(valor: str) -> str:
    while True:
        try:
            dato = input(f"Ingrese el {valor}: ").strip()
            if not dato:
                raise ValueError(f"El {valor} no puede estar vacío.")
            if any(c.isdigit() for c in dato):
                raise ValueError(f"El {valor} no puede contener números.")
            return dato
        except ValueError as e:
            print(e)



def pedir_datos_domicilio() -> Tuple[str, int, int, str, str, str]:
    menu.clear()
    print("Domicilio")
    while True:
        try:
            d_calle = input("Ingrese la calle: ").strip()
            if not d_calle:
                raise ValueError("Debe ingresar una calle valida.")
            d_numero = input("Ingrese la altura: ")
            if not d_numero.isdigit() or int(d_numero) <= 0:
                raise ValueError("Debe ingresar una altura válida.")
            d_piso = input("Ingrese el piso ('Enter' para 0): ").strip()
            d_piso = int(d_piso) if d_piso.isdigit() else 0
            d_dpto = input("Departamento ('Enter' si no aplica): ").strip()
            d_dpto = d_dpto if d_dpto else 0
            localidad = input("Localidad: ").strip()
            if not localidad:
                raise ValueError("Debe ingresar una Localidad.")
            provincia = input("Provincia: ").strip()
            if not provincia:
                raise ValueError("Debe ingresar una provincia.")
            return (d_calle, d_numero, d_piso, d_dpto, localidad, provincia)
        except ValueError as e:
            print(e)



def pedir_datos_cliente() -> Tuple[str, str]:
    nombre, apellido = pedir_nombre_apellido("nombre"), pedir_nombre_apellido(
        "apellido"
    )
    dni = pedir_dni()
    d_calle, d_numero, d_piso, d_dpto, localidad, provincia = pedir_datos_domicilio()
    return (
        nombre,
        apellido,
        dni,
        d_calle,
        d_numero,
        d_piso,
        d_dpto,
        localidad,
        provincia,
    )


def registrar_reserva(lista_reservas: List[Dict]) -> None:
    """Registra una reserva a partir de los datos ingresados por el usuario.
    Valida si existe la misma reserva si coincide DNI con fecha de inicio y
    fecha de fin. También valida que la habitación no esté ocupada en la fecha
    de inicio indicada.

    Pre: La lista de reservas proviene de y se guarda en un JSON.

    Pos: almacena los datos en un JSON y genera automáticamente un número de
         reserva.

    """
    nombre, apellido, dni, d_calle, d_numero, d_piso, d_dpto, localidad, provincia = (
        pedir_datos_cliente()
    )
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
            f"Domicilio: {d_calle} N° {d_numero} - Piso {d_piso} - Departamento {d_dpto} - {localidad} - {provincia}"
        )
        print(f"Fecha de reserva: {fecha_reserva} - Habitación: {num_habitacion}")
        print(
            f"Inicio estadía: {dia_ini}/{mes_ini}/{anio_ini} - Fin estadía: {dia_fin}/{mes_fin}/{anio_fin}"
        )

        confirmacion = int(
            input("Ingrese 1 si los datos son correctos y 0 si son incorrectos: ")
        )

        if confirmacion == 0:
            menu.clear()
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
            "calle": d_calle,
            "numero": str(d_numero),
            "piso": str(d_piso),
            "dpto": str(d_dpto),
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
                menu.clear()
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
                menu.clear()
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
