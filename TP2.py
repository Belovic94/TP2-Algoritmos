import csv

CANT_OPCIONES = 5
AÑO = 2016

# ----------------------------------------------------------------------------------------------------------
# |                                 Cargo los datos del archivo en memoria                                 |
# ----------------------------------------------------------------------------------------------------------


def cargar_datos_supermercado_en_diccionario(arch):
    """Ingresa como parametro la ruta de un archivo csv con 2 campos.
    Devuelve un diccionario con el primer campo del archivo como clave y el segundo como valor"""
    try:
        with open(arch, "r") as f_archivo:
            dicc = {}
            archivo_csv = csv.reader(f_archivo)
            encabezado = next(archivo_csv)
            for clave, valor in archivo_csv:
                clave = int(clave)
                dicc[clave] = dicc.get(clave, "") + valor
        return dicc
    except IOError:
        raise IOError

def verificar_registro_principal(registro, encabezado):
    """Recibe una lista con la linea actual del archivo precio.csv y el encabezado del mismo archivo. Devuelve True si la linea esta bien cargada y False sino lo esta"""
    try:

        if len(registro) == len(encabezado):
            if registro[0].isdigit() and registro[1].isdigit(): 
                float(registro[3])
                if len(registro[2]) == 6:
                    if es_año(registro[2][:4]) and es_mes(registro[2][4:]):
                        return True

        return False
    except TypeError: # por si entra None o el precio no es numérico
        return False

def verificar_registro_secundario(registro, encabezado):
    """Recibe una lista con la linea actual del archivo productos.csv y el encabezado del mismo archivo. Devuelve True si la linea esta bien cargada y False sino lo esta """
    try: 
        if len(registro) != len(encabezado):
            return False
        try:
            assert type(registro[1]) == str
        except AssertionError:
            return False
        return True
    except TypeError: # por si entra None
        return False

def cargar_datos_en_diccionario(arch1, arch2, arch3):
    """Ingresa como parametros 3 archivos. Devuelve un diccionario con los datos
    de los archivos de la forma {PRODUCTO:{SUPERMERCADO:{FECHA:PRECIO}"""
    # abro el archivo de 4 campos y el de los producto.
    try:
        with open(arch1, "r") as principal, open(arch2, "r") as secundario:
            # cargo los datos del  archivo de los supermercados y lo meto en un diccionario.
            diccionario_sup = cargar_datos_supermercado_en_diccionario(arch3)
            datos_productos_csv = csv.reader(secundario)
            archivo_csv = csv.reader(principal)
            encabezado_principal = next(archivo_csv, None) # obtiene el encabezado
            encabezado_secundario = next(datos_productos_csv, None) # obtiene el encabezado
            registro_principal = next(archivo_csv, None)
            registro_secundario = next(datos_productos_csv, None)
            dicc_productos = {}
            lista_registros_fallidos = []
            # empieza corte de control por producto.
            # Mientras registro_principal y registro_secundario no sean None.
            while registro_principal and registro_secundario:
                while not verificar_registro_principal(registro_principal, encabezado_principal) and registro_principal:
                    lista_registros_fallidos.append(registro_principal)
                    registro_principal = next(archivo_csv, None)
                while not verificar_registro_secundario(registro_secundario, encabezado_secundario) and registro_secundario:
                    registro_secundario = next(datos_productos_csv, None)
                
                id_producto = int(registro_principal[1])
                dicc_supermercados = {}
            
                while registro_principal and id_producto == int(registro_principal[1]) and id_producto <= int(registro_secundario[0]):
                    # recorro archivo productos hasta encontrar el id producto
                    if int(registro_principal[1]) < int(registro_secundario[0]):
                        while not verificar_registro_principal(registro_principal,encabezado_principal) and registro_principal:
                            lista_registros_fallidos.append(registro_principal)
                            registro_principal = next(archivo_csv, None)
                        id_producto = registro_principal[1]
                        continue
                
                    supermercado = int(registro_principal[0])
                    nom_supermercado = diccionario_sup.get(supermercado, "")
                    dicc_fechas = {}
                
                    while registro_principal and supermercado == int(registro_principal[0]):
                        dicc_fechas[registro_principal[2]] = float(registro_principal[3]) 
                        registro_principal = next(archivo_csv, None)
                        while not verificar_registro_principal(registro_principal, encabezado_principal) and registro_principal:
                            lista_registros_fallidos.append(registro_principal)
                            registro_principal = next(archivo_csv, None)

                    dicc_supermercados[nom_supermercado] = dicc_fechas
            
                if dicc_supermercados != {}:  # si el diccionario está vacío, no lo guarda.
                    dicc_productos[registro_secundario[1]] = dicc_supermercados # La clave va a ser el nombre del producto
                registro_secundario = next(datos_productos_csv, None)
        return dicc_productos, lista_registros_fallidos
    except IOError:
        print("No se encontro el/los archivo/s. Ingrese bien la ruta/nombre del archivo/s")

# ----------------------------------------------------------------------------------------------------------
# |                                 Inflacion por Supermercado y Prodcuto                                  |
# ----------------------------------------------------------------------------------------------------------


def inflacion_por_supermercado(diccionario,fechas):
    """Recibe com parametro un diccionario y una tupla de fechas. Devuelve la inflacion total de los supermercados en un diccionario"""
    inflacion_total = {}
    cantidad_de_productos = 1
    for producto in diccionario.keys():
        try:
            inflacion = calcular_inflacion(diccionario, producto, fechas)
            for supermercado, inflacion_producto in inflacion:
                if supermercado not in inflacion_total.keys(): # se fija si es el primer producto del supermercado
                    # asigna una lista al diccionario de inflacion total
                    # la lista esta compuesta por la inflacion del producto y la cantidad de productos que tiene el supermercado hasta el momento
                    inflacion_total[supermercado] = [inflacion_producto, cantidad_de_productos] 
                    continue
                valor_anterior = inflacion_total.pop(supermercado)
                inflacion_total[supermercado] = [valor_anterior[0] + inflacion_producto, valor_anterior[1] + 1]
        except TypeError:
            continue
    for supermercado, lista_inflacion_cantproductos in inflacion_total.items():
        inflacion_total[supermercado] = lista_inflacion_cantproductos[0] / lista_inflacion_cantproductos[1]
    if not inflacion_total.items():
        return None
    return inflacion_total.items()

def calcular_inflacion(diccionario, producto, fechas):  
    """Recibe como parametro un diccionario, una cadena y una tupla de fechas.
    Devuelve una lista de tuplas, donde cada tupla contiene el nombre del supermercado y su inflacion"""
    inflacion = []
    supermercado = diccionario.get(producto,{}) # asigna en la variable supermercado, un dicionario cuya clave
                                                # es el nombre del supermercado y el valor es otro diccionario de fechas
    for clave in supermercado:
        try:
            dicc_fechas = supermercado.get(clave, {})
            precioi = dicc_fechas.get(fechas[0], None)
            preciof = dicc_fechas.get(fechas[1], None)
            inflacion.append((clave, 100 * ((preciof - precioi) / precioi)))
        except TypeError: # Si el supermercado no tiene el producto para alguna de las fechas, pasa al siguiente supermercado
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


#----------------------------------------------------------------------------------------------------------
# |                                 Inflacion general promedio                                            |
# --------------------------------------------------------------------------------------------------------


def inflacion_general_promedio(diccionario, fechas):
    """Recibe como parametro un diccionario y un rango de fechas. Devuelve la inflacion general promedio de todos los productos """
    inflacion_promedio = 0
    for producto in diccionario.keys():
        try:
            inflacion = calcular_inflacion(diccionario, producto, fechas)
            inflacion_total_producto = 0
            for supermecado, inflacion_parcial_producto in inflacion:
                inflacion_total_producto += inflacion_parcial_producto
            inflacion_promedio  += inflacion_total_producto / len(inflacion)
        except TypeError:
            continue
    return (inflacion_promedio / len(diccionario.keys())), fechas

def mostrar_inflacion_promedio(inflacion_promedio, fechas):
    """Recibe un número flotante con la inflacion promedio y lo imprime por pantalla"""
    print("La inflacion general promedio entre las fechas {} y {} es : {:.2f}% ".format(fechas[0], fechas[1], inflacion_promedio))


#------------------------------------------------------------------------------------------------------
# |                                 Mejor Precio Producto                                             |
# -----------------------------------------------------------------------------------------------------


def mejor_precio_supermercado(diccionario, producto, fecha):
    """Recibe como parametro un diccionario, el nombre de un producto y una fecha. Devuelve el precio más bajo  y el nombre del supermecado que vende el producto a ese precio"""
    precio_supermercado = []
    supermecado = diccionario.get(producto,{})
    print(supermecado)
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
        except TypeError: # si el supermercado no vende el producto en esa fecha, pasa al siguiente
            continue
    return supermercado_mejor_precio, mejor_precio


def mostrar_mejor_precio(supermercado,precio):
    try:
        print("El precio más bajo del producto es ${:.2f} y se encuentra en el supermercado {}".format(precio,supermercado))
    except TypeError: # Si el producto no se vende en ningun supermercado para esa fecha, tira error
        raise TypeError("El producto no se vende en ninguno de los supermercados para esa fecha ")

# -----------------------------------------------------------------------------------
# |                             Mostrar Menu y Main                                 |
# -----------------------------------------------------------------------------------


def mostrar_menu():
    """Imprime el menú principal"""
    lista_opciones = [  'Inflación por supermercado',
                        'Inflación por producto',
                        'Inflación general promedio',
                        'Mejor precio para un producto',
                        'Salir']
    imprimir_opciones(lista_opciones)


def main():
    """Inicia un programa con interfaz amigable para cálculos de inflación, entre otros, utilizando tres archivos csv."""
    datos, lista_registros_fallidos = cargar_datos_en_diccionario("precios.csv", "productos.csv", "supermercados.csv")
    imprimir_opciones(lista_registros_fallidos)
    opcion = ""
    while opcion != 5:
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion == 1:
            try:
                inflacion = inflacion_por_supermercado(datos, (pedir_fecha(), pedir_fecha()))
                mostrar_inflacion(inflacion)
            except TypeError:
                print("Ningún producto se vende entre ese rango de fechas")

        if opcion == 2:
            try:
                inflacion = calcular_inflacion(datos, pedir_producto(datos),
                                               (pedir_fecha(), pedir_fecha()))
                mostrar_inflacion(inflacion)
            except (TypeError, KeyError) as error:
                print(error)

        if opcion == 3:
            inflacion_promedio, fechas = inflacion_general_promedio(datos,
                                                                    (pedir_fecha(), pedir_fecha()))
            mostrar_inflacion_promedio(inflacion_promedio, fechas)
        if opcion == 4:
            try:
                supermercado, precio = mejor_precio_supermercado(datos, pedir_producto(datos),
                                                                 pedir_fecha())
                mostrar_mejor_precio(supermercado, precio)
            except TypeError as error:
                print(error)

    print("Hasta luego.")



def imprimir_opciones(lista):
    """Imprime una lista de opciones"""
    for x in range(len(lista)):
        print(str(x + 1) + ". " + str(lista[x]))




# -----------------------------------------------------------------------------
# |                             Ingreso datos                                 |
# -----------------------------------------------------------------------------


def pedir_opcion(cantidad = CANT_OPCIONES):
   """Pide el ingreso de una opcion"""
   return verif_ingreso_opcion(input("Su elección: "), cantidad)

def pedir_fecha():
    print ("Ingrese una fecha")
    año = verif_ingreso_año(input("Año (en formato AAAA): ")) 
    mes = verif_ingreso_mes(input("Mes (número): "))
    return año + mes

def pedir_producto(diccionario):
   """Pide un nombre de producto (o una parte de él)"""
   return verif_ingreso_producto(input('Producto buscado: '), diccionario)

# ----------------------------------------------------------------------------
# |                             Verificaciones                               |
# ----------------------------------------------------------------------------



def buscar_producto_ingresado(cadena, diccionario):
    """Busca la cadena en el diccionario pasado por parámetro y devuelve
    todas las claves que contienen la cadena en forma de lista, desordenada"""
    listaaux = []
    for nombre_producto in diccionario:
        if cadena.lower() in nombre_producto.lower():
            listaaux += [nombre_producto]
    if not listaaux:
        return None
    return listaaux

def verif_ingreso_producto(cadena, diccionario):
    """Dada una cadena 'de busqueda' y un diccionario, muestra todos los productos
    que contengan la cadena y se solicita que se elija uno de ellos. Devuelve
    la descripcion del producto elegido"""
    try:
        encontrados = buscar_producto_ingresado(cadena, diccionario)
        imprimir_opciones(encontrados)
        buscado = encontrados[pedir_opcion(len(encontrados)) - 1]
        return buscado
    except TypeError:
        raise TypeError("No se encontro ningun producto con nombre {} ".format(cadena))

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


def verif_ingreso_opcion(cadena, cantidad):
    """Recibe una cadena ingresada por el usuario y no la devuelve hasta que sea un número perteneciente a las opciones posibles"""
    while not es_numero_opcion(cadena, cantidad):
        cadena = input("Ingrese un número de opción: ")
    return int(cadena)


def es_numero_opcion(cadena, cantidad_opciones):
    """Verifica que la cadena sea una de las opciones posibles, establecidas por la
    cantidad pasada por parámetro"""
    return cadena.isdigit() and int(cadena) <= cantidad_opciones


def es_mes(cadena):
    return cadena.isdigit() and 12 >= int(cadena) > 0


def es_año(cadena):
    return cadena.isdigit() and len(cadena) == 4 and 0 < int(cadena) <= AÑO

main()
