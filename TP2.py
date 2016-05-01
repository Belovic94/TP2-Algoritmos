import csv

CANT_OPCIONES = 5
AÑO = 2016

# ----------------------------------------------------------------------------------------------------------
# |                                 Cargo los datos del archivo en memoria                                 |
# ---------------------------------------------------------------------------------------------------------


def cargar_datos_supermercado_en_diccionario(arch):
    """Ingresa como parametro la ruta de un archivo csv con 2 campos.
    Devuelve un diccionario con el primer campo del archivo como clave y el segundo como valor"""
    with open(arch, "r") as f_archivo:
        dicc = {}
        archivo_csv = csv.reader(f_archivo)
        encabezado = next(archivo_csv)
        for clave, valor in archivo_csv:
            dicc[clave] = dicc.get(clave, "") + valor
    return dicc


def cargar_datos_en_diccionario(arch1, arch2, arch3):
    """Ingresa como parametros 3 archivos. Devuelve un diccionario con los datos de los archivos."""
    # abro el archivo de 4 campos y el de los producto.
    with open(arch1, "r") as principal, open(arch2, "r") as secundario:
        # cargo los datos del  archivo de los supermercados y lo meto en un diccionario.
        diccionario_sup = cargar_datos_supermercado_en_diccionario(arch3)
        datos_productos_csv = csv.reader(secundario)
        archivo_csv = csv.reader(principal)
        encabezado_principal = next(archivo_csv, None)
        encabezado_secundario = next(datos_productos_csv, None)
        registro_principal = next(archivo_csv, None)
        registro_secundario = next(datos_productos_csv, None)
        dicc_productos = {}
        # empieza corte de control por producto.
        # Mientras registro_principal y registro_secundario no sean None.
        while registro_principal and registro_secundario:
            id_producto = registro_principal[1]
            dicc_supermercados = {}
            while registro_principal and id_producto == registro_principal[1] and id_producto <= registro_secundario[0]:
                # recorro archivo productos hasta encontrar el id producto
                if registro_principal[1] < registro_secundario[0]:
                    registro_principal = next(archivo_csv, None)
                    id_producto = registro_principal[1]
                    continue  # vuelve a comprobar la condicion del While
                supermercado = registro_principal[0]
                nom_supermercado = diccionario_sup.get(supermercado, "")
                dicc_fechas = {}
                while registro_principal and supermercado == registro_principal[0]:
                    dicc_fechas[registro_principal[2]] = float(registro_principal[3])
                    registro_principal = next(archivo_csv, None)
                dicc_supermercados[nom_supermercado] = dicc_fechas
            if dicc_supermercados != {}:  # si el diccionario de supermercado esta vacio no lo guarda.
                # La clave va a ser el nombre del producto
                dicc_productos[registro_secundario[1].lower()] = dicc_supermercados
            # lee la siguiente linea del archivo secundario
            registro_secundario = next(datos_productos_csv, None)
    return dicc_productos

# ----------------------------------------------------------------------------------------------------------
# |                                 Inflacion por Supermercado y Prodcuto                                  |
# ----------------------------------------------------------------------------------------------------------


def inflacion_por_supermercado(diccionario,fechas):
    """Recibe com parametro un diccionario y una tupla de fechas. Devuelve la inflacion total de los supermercados en un diccionario"""
    inflacion_total = {}
    cantidad_de_productos = 1
    for producto in diccionario.keys():
        inflacion = calcular_inflacion(diccionario, producto, fechas)
        for supermercado,inflacion_producto in inflacion:
            if supermercado not in inflacion_total.keys():
                inflacion_total[supermercado] = [inflacion_producto,cantidad_de_productos]
                continue
            valor_anterior = inflacion_total.pop(supermercado)
            inflacion_total[supermercado] = inflacion_total.get(supermercado,[]) + [valor_anterior[0] + inflacion_producto, valor_anterior[1] + 1]
    for supermercado,lista in inflacion_total.items():
        inflacion_total[supermercado] = lista[0] / lista[1]
    return inflacion_total.items()

def calcular_inflacion(diccionario, producto, fechas):  
    """Recibe como parametro un diccionario, una cadena y una tupla de fechas.
    Devuelve una lista de tuplas, donde cada tupla contiene el nombre del supermercado y su inflacion"""
    inflacion = []
    supermercado = diccionario.get(producto,{})
    # asigna en la variable supermercado, un dicionario cuya clave
    # es el nombre del supermercado y el valor es otro diccionario de fechas
    for clave in supermercado:
        try:
            dicc_fechas = supermercado.get(clave, {})
            precioi = dicc_fechas.get(fechas[0], None)
            preciof = dicc_fechas.get(fechas[1], None)
            inflacion.append((clave, 100 * ((preciof - precioi) / precioi)))
        except TypeError:
            continue
    if inflacion:
        return inflacion
    return None

def mostrar_inflacion(lista):
    "Recibe como parametro una secuencia. Imprime por pantalla los diferentes supermercados y su inflacion"
    try:
        for supermercado,inflacion in lista:
            print("La inflacion del supermercado {} es {:.2f}% ".format(supermercado,inflacion))
    except:
        raise TypeError("El producto no se vende en ninguno de los supermercados para ese rango de fechas")


#------------------------------------------------------------------------------------------------------
# |                                 Inflacion general promedio                                            |
# ----------------------------------------------------------------------------------------------------


def inflacion_general_promedio(diccionario, fechas):
    """Recibe como parametro un diccionario y un rango de fechas. Devuelve la inflacion general promedio de todos los productos """
    inflacion_promedio = 0
    for producto in diccionario.keys():
        print(producto)
        inflacion = calcular_inflacion(diccionario, producto, fechas)
        inflacion_total_producto = 0
        for supermecado,inflacion_parcial_producto in inflacion:
            inflacion_total_producto += inflacion_parcial_producto
        inflacion_promedio  += inflacion_total_producto / len(inflacion)
    return (inflacion_promedio / len(diccionario.keys())), fechas

def mostrar_inflacion_promedio(inflacion_promedio, fechas):
    """Recibe un número flotante con la inflacion promedio y lo imprime por pantalla"""
    print("La inflacion general promedio entre las fechas {} y {} es : {:.2f}".format(fechas[0], fechas[1], inflacion_promedio))


#------------------------------------------------------------------------------------------------------
# |                                 Mejor Precio Producto                                             |
# ----------------------------------------------------------------------------------------------------


def mejor_precio_supermercado(diccionario, producto, fecha):
    """Recibe como parametro un diccionario, el nombre de un producto y una fecha. Devuelve el precio más bajo  y el nombre del supermecado que vende el producto a ese precio"""
    precio_supermercado = []
    supermecado = diccionario.get(producto,{})
    mejor_precio = None 
    for clave in supermecado:
        try:
            dicc_fechas = supermecado[clave]
            precio = dicc_fechas.get(fecha, None)
            if  not mejor_precio: # el primer precio siempre va a ser el mejor precio
                mejor_precio = precio
                supermercado_mejor_precio = clave
            elif precio < mejor_precio:
                mejor_precio = precio
                supermercado_mejor_precio = clave
        except TypeError:
            continue
    return supermercado_mejor_precio, mejor_precio


def mostrar_mejor_precio(supermercado,precio):
    print("El precio más bajo del producto es ${:.2f} y se encuentra en el supermercado {}".format(precio,supermercado))


# -----------------------------------------------------------------------------------
# |                             Mostrar Menu y Main                                 |
# ----------------------------------------------------------------------------------


def mostrar_menu():
    print("")
    print("1. Inflación por supermercado")
    print("2. Inflación por producto")
    print("3. Inflación general promedio")
    print("4. Mejor precio para un producto")
    print("5. Salir")


def main():
    datos = cargar_datos_en_diccionario("archivo.csv", "archivo2.csv", "archivo3.csv")
    while True:
        mostrar_menu()
        opcion = pedir_opcion()
        if opcion == "5":
            break
        
        if opcion == "1":
            inflacion = inflacion_por_supermercado(datos, (pedir_fecha(),pedir_fecha()))
            mostrar_inflacion(inflacion)
        
        if opcion == "2":
            try:
                inflacion = calcular_inflacion(datos, pedir_producto(), (pedir_fecha(),pedir_fecha()))
                mostrar_inflacion(inflacion)
            except (TypeError, KeyError) as error:
                print("Error: ", error)
        
        if opcion == "3":
            inflacion_promedio,fechas = inflacion_general_promedio(datos, (pedir_fecha(),pedir_fecha()))
            mostrar_inflacion_promedio(inflacion_promedio,fechas)
        
        if opcion == "4":
            try:
                supermercado, precio = mejor_precio_supermercado(datos, pedir_producto(), pedir_fecha())
                mostrar_mejor_precio(supermercado, precio)
            except TypeError:
                print("El producto no se vende en ninguno de los supermercados para esa fecha ")




# -----------------------------------------------------------------------------
# |                             Ingreso datos                                 |
# -----------------------------------------------------------------------------


def pedir_opcion():
    return verif_ingreso_opcion(input("Opción: "))

def pedir_fecha():
    print ("Ingrese una fecha")
    año = verif_ingreso_año(input("Año (en formato AAAA): ")) # puse que ingrese una sola fecha para hacerlo más general. Aparte la opcion 4 pide una sola fecha.
    mes = verif_ingreso_mes(input("Mes (número): "))
    return año + mes

def pedir_producto():# falta hacer que la eleccion del producto sea inteligente como especifica el tp
    return input('Producto a estudiar: ').lower()

# ----------------------------------------------------------------------------
# |                             Verificaciones                               |
# ----------------------------------------------------------------------------

def verif_ingreso_mes(cadena):
    while not es_mes(cadena):
        cadena = input('Ingrese el número de mes: ')
    if len(cadena) == 1:
        return '0' + cadena
    return cadena


def verif_ingreso_año(cadena):
    while not es_año(cadena):
        cadena = input('Ingrese el año en formato AAAA: ')
    return cadena


def verif_ingreso_opcion(cadena):
    """Recibe una cadena ingresada por el usuario y no la devuelve hasta que
    sea un número perteneciente a las opciones posibles"""
    while not es_numero_opcion(cadena):
        cadena = input("Ingrese un número de opción: ")
    return cadena


def es_numero_opcion(cadena):
    return cadena.isdigit() and int(cadena) <= CANT_OPCIONES


def es_mes(cadena):
    return cadena.isdigit() and 12 >= int(cadena) > 0


def es_año(cadena):
    return cadena.isdigit() and len(cadena) == 4 and 0 < int(cadena) <= AÑO

main()
