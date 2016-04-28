import csv
def cargar_datos_supermercado_en_diccionario(arch):
    """Ingresa como parametro la ruta de un archivo csv con 2 campos. Devuelve un diccionario con el primer campo del archivo como clave y el segundo como valor"""
    with open(arch,"r") as f_archivo:
        dicc={}
        archivo_csv=csv.reader(f_archivo)
        encabezado=next(archivo_csv)
        for clave,valor in archivo_csv:
            dicc[clave]=dicc.get(clave,"") + valor
    return dicc
def cargar_datos_en_diccionario(arch1,arch2,arch3):
    """Ingresa como parametros 3 archivos. Devuelve un diccionario con los datos de los archivos."""
    with open(arch1,"r") as principal, open(arch2,"r") as secundario: # abro el archivo de 4 campos y el de los producto.
        diccionario_sup=cargar_datos_supermercado_en_diccionario(arch3)# cargo los datos del  archivo de los supermercados y lo meto en un diccionario.
        datos_productos_csv=csv.reader(secundario)
        archivo_csv=csv.reader(principal)
        encabezado_principal=next(archivo_csv,None) #saca el encabezado del archivo.
        encabezado_secundario=next(datos_productos_csv,None)
        registro_principal=next(archivo_csv,None) # lee la primera linea del archivo principal.
        registro_secundario=next(datos_productos_csv,None)# lee la primera linea del archivo secundario.
        dicc_productos={}
        while registro_principal and registro_secundario: # empieza corte de control por producto. Mientras registro_principal y registro_secundario no sean None.
            id_producto=registro_principal[1]
            dicc_supermercados={}
            while registro_principal and id_producto==registro_principal[1] and id_producto<=registro_secundario[0]:
                if registro_principal[1]<registro_secundario[0]:
                    registro_principal=next(archivo_csv,None)# lee la siguiente linea del archivo principal
                    id_producto=registro_principal[1]
                    continue # vuelve a comprobar la condicion del While
                supermercado=registro_principal[0]
                nom_supermercado=diccionario_sup.get(supermercado,"")# obtiene el nombre del supermercado del diccionario anterior
                dicc_fechas={}
                while registro_principal and supermercado==registro_principal[0]:
                    dicc_fechas[registro_principal[2]]=dicc_fechas.get(registro_principal[2],0) + float(registro_principal[3])
                    registro_principal=next(archivo_csv,None) # lee la siguiente linea del archivo principal
                dicc_supermercados[nom_supermercado]=dicc_fechas
            if dicc_supermercados!={}:# si el diccionario de supermercado esta vacio no lo guarda.
                dicc_productos[registro_secundario[1]]=dicc_supermercados # La clave va a ser el nombre del producto
            registro_secundario=next(datos_productos_csv,None) #lee la siguiente linea del archivo secundario
    return dicc_productos

def calcular_inflacion(diccionario,producto,fechas): # En revision / Este sería el punto 2
    """Recibe como parametro un diccionario, una cadena y una tupla de fechas. Devuelve uan lista de tuplas, donde cada tupla contiene el nombre del supermercado y su inflacion"""
    inflacion=[]
    supermercado=diccionario.get(producto,{}) # asigna en la variable supermercado, un dicionario cuya clave es el nombre del supermercado y el valor es otro diccionario de fechas
    for clave in supermercado:
        dicc_fechas=supermercado.get(clave,{})
        precioi=dicc_fechas.get(fechas[0],0)
        preciof=dicc_fechas.get(fechas[1],0)
        inflacion.append((clave,100*((preciof-precioi)/precioi)))
    return inflacion

def mostrar_menu():
    print("1. Inflación por supermercado")
    print("2. Inflación por producto")
    print("3. Inflación general promedio")
    print("4. Mejor precio para un producto")
    print("5. Salir")

def main():
    cargar_datos_en_diccionario("archivo.csv","archivo2.csv","archivo3.csv")
    while true:
        mostrar_menu
        opcion=input("Opcion: ")
        if opcion==5:
            break

fechas=("201601","201602")
print(cargar_datos_en_diccionario("archivo.csv","archivo2.csv","archivo3.csv"))
print(calcular_inflacion(cargar_datos_en_diccionario("archivo.csv","archivo2.csv","archivo3.csv"),"Galletitas Okebon",fechas))
