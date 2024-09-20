# esta seccion es de consumos del frigobar


from tablas_del_sistema import imprimir_tabla, cargar_data


def pedir_numero(msj):
    """Solicita un número al usuario y valida su entrada.

    Pre: Recibe un mensaje "msj" tipo string para mostrar al usuario.

    Post: Devuelve el número ingresado si es válido (contiene solo dígitos).
          Si no es válido, vuelve a solicitar la entrada.

    """
    while True:
        num = input(msj)
        if num.isdigit():
            return num
        print("Error, ingrese un número válido.")


def pedir_id(data):
    """Solicita el ID de un producto y verifica si existe en los datos.

    Pre: Recibe una lista "data" que contiene los productos con su ID.

    Post: Devuelve el ID si existe en los datos. Si no, vuelve a solicitar la
          entrada hasta que el ID sea válido.

    """
    while True:
        num = pedir_numero("Ingrese el id del producto a agregar: ")
        if any(producto["ID"] == str(num) for producto in data):
            return num
        print("Error, el id ingresado no existe.")


"""
def seleccionar_habitacion():
    imprimir_tabla("data/habitaciones.csv")
    return habitacion


def cargar_elemento():
    return None

    
"""


def main():
    data = cargar_data("data/productos.csv")
    imprimir_tabla("data/productos.csv")
    id_elemento = pedir_id(data)
    cant = pedir_numero("ingrese la cantidad que desea cargar: ")
    n_hab = pedir_numero("ingrese el numero de habiatacion para cargar el consumo: ")


main()
