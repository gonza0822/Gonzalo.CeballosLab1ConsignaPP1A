import re
import json
import os

archivocsv = "C:\\Users\\gonza\\Documents\\tecnicatura\\1A\\programacion1\\ejemplo1\\primer_parcial\\insumos.csv"

def mostrar_datos_ordenados(lista:list):
    for elementos in lista:
        print(f'{elementos["ID"]}, {elementos["NOMBRE"]}, {elementos["MARCA"]}, {elementos["PRECIO"]}, {elementos["CARACTERISTICAS"]},')

def cargar_datos(archivo:str):
    with open(archivo, "r", encoding='utf-8') as file:
        contenido = file.read()
    lista_contenido = contenido.split("\n")
    lista_listas = []
    lista_contenido = list(filter(lambda cadenas: cadenas != "", lista_contenido))
    for insumos in lista_contenido:
        elementos = insumos.split(",")
        lista_listas.append(elementos)   
    lista_insumos = []
    for i in range(len(lista_listas)):
        diccionario_insumos = {}
        if(i == 0):
            keys = lista_listas[i]
        else:
            diccionario_insumos[keys[0]] = lista_listas[i][0]
            diccionario_insumos[keys[1]] = lista_listas[i][1]
            diccionario_insumos[keys[2]] = lista_listas[i][2]
            diccionario_insumos[keys[3]] = lista_listas[i][3]
            diccionario_insumos[keys[4]] = lista_listas[i][4]
            lista_insumos.append(diccionario_insumos)
    return lista_insumos



def listar_cantidad_marcas(lista:list):
    lista_marcas = set()
    diccionario_cantidad_marcas = {}
    for insumos in lista:
        lista_marcas.add(insumos["MARCA"])
    for marcas in lista_marcas:
        diccionario_cantidad_marcas[marcas] = 0
    for i in range(len(lista)):
       for marcas in lista_marcas:
           if(lista[i]["MARCA"] == marcas):
               diccionario_cantidad_marcas[marcas] += 1
    for marcas in diccionario_cantidad_marcas:
        print(f"La marca {marcas} tiene {diccionario_cantidad_marcas[marcas]} insumos")



def listar_insumos_marca(lista:list):
    lista_marcas = set()
    lista_nombres_precios_marcas = []
    for insumos in lista:
        lista_marcas.add(insumos["MARCA"])
    for i in range(len(lista)):
       for marcas in lista_marcas:
           if(lista[i]["MARCA"] == marcas):
               lista_insumos = [lista[i]["NOMBRE"], lista[i]["MARCA"], lista[i]["PRECIO"]]
               lista_nombres_precios_marcas.append(lista_insumos)
    for insumos in lista_nombres_precios_marcas:
        print(f"el producto {insumos[0]} tiene la marca {insumos[1]}  y el precio es {insumos[2]}")



def insumos_por_caracteristicas(lista:list):
    caracteristica = input("¿Que caracteristica desea listar?")
    caracteristica = caracteristica.capitalize()
    lista_insumos_caracteristicas = list(filter(lambda insumo: re.search(caracteristica, insumo["CARACTERISTICAS"]), lista))
    if(len(lista_insumos_caracteristicas) == 0):
        print("Error esa carcteristica no exite")
    else:
        return lista_insumos_caracteristicas
    
    
    
def listar_insumos_ordenados(lista:list):
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i +1, tam):
            if (lista[i]["MARCA"] > lista[j]["MARCA"]) or ((lista[i]["MARCA"] == lista[j]["MARCA"]) and (lista[i]["PRECIO"] < lista[j]["PRECIO"])):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux
    mostrar_datos_ordenados(lista)

def realizar_compras(lista:list):
    lista_compras = []
    while True:
        lista_elementos = []
        marca_usuario = input("¿Que marca desea comprar?")
        marca_usuario = marca_usuario.lower()
        lista_elementos = list(filter(lambda elementos: marca_usuario == elementos["MARCA"].lower(), lista))
        if(len(lista_elementos) == 0):
            print("Esa marca no existe") 
            break
        print("Estos son los productos de esa marca")
        for insumos in lista_elementos:
            print(f'{insumos["ID"]} ,{insumos["NOMBRE"]}, {insumos["MARCA"]} {insumos["PRECIO"]}, {insumos["CARACTERISTICAS"]}')
        producto_usuario = input("¿Que producto desea comprar?(escriba el numero del producto)")
        for insumos in lista_elementos:
            if(producto_usuario == insumos["ID"]):
                lista_compras.append(insumos)
                print("Agregado al carrito")
        if(len(lista_compras) == 0):
            print("Ese producto no esta en esa marca")
        eleccion_usuario = input("¿Desea seguir comprando s/n?")
        while(eleccion_usuario != "n" and eleccion_usuario != "s"):
            eleccion_usuario = input("la respuesta debe ser s(si) o n(no)")
            print(eleccion_usuario)
        if(eleccion_usuario == "n"):
            contador = 0
            total_compra = 0
            with open("texto.txt", "w", encoding="utf-8") as file:
                file.write("Compra de insumos: \n---------------------------\n")
                for insumos in lista_compras:
                    contador += 1
                    precio = insumos["PRECIO"].replace("$", "")
                    total_compra += float(precio) 
                    file.write(f'{insumos["NOMBRE"]}, {insumos["MARCA"]}, {insumos["CARACTERISTICAS"]},  PRECIO: {insumos["PRECIO"]}\n')
                file.write(f"Cantidad de productos: {contador}\nTotal: {total_compra:.2f}")
            print("compra realizada")
            break


def guardar_json(lista:list):
    lista_alimentos = []
    for insumos in lista:
        coincidencia = re.search(r"Alimento", insumos["NOMBRE"])
        if(coincidencia):
            lista_alimentos.append(insumos)
    with open("alimentos.json", "w", encoding="utf-8") as file:
        json.dump(lista_alimentos, file, ensure_ascii=False, indent=4)


def leer_json():
    with open("alimentos.json", "r") as file:
        contenido = file.read()
        lista_alimentos = json.loads(contenido)
    mostrar_datos_ordenados(lista_alimentos)

#esta funcion solo es para la funcion actuatizar_precios
def aumentar_precios(insumos):
        aumento = 8.4
        insumos["PRECIO"] = str(round(float(insumos["PRECIO"].replace("$", "")) + (float(insumos["PRECIO"].replace("$", "")) * (aumento/100)), 2))
        return insumos

def actualizar_precios(lista:list):
    lista_actualizada = list(map(aumentar_precios, lista))
    with open(archivocsv, "w", encoding="utf-8") as file:
        file.write("\nID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for insumos in lista_actualizada:
            file.write(f'{insumos["ID"]},{insumos["NOMBRE"]},{insumos["MARCA"]},${insumos["PRECIO"]},{insumos["CARACTERISTICAS"]}\n')

def menu():
    flag_cargar_datos = False
    flag_JSON = False

    while True:
        os.system("cls")
        print("cerrar esto")
        print("""*** Menu de opciones ***
    --------------------------
    1-Cargar datos desde archivo
    2-Listar cantidad de insumos por marca
    3-Listar insumos por marca
    4-Buscar insumo por caracteristica
    5-Listar insumos ordenados
    6-Realizar compras
    7-Guardar en formaro JSON
    8-Leer desde formato JSON
    9-Actualizar-precios
    10-Salir del programa""")
        opcion = input("Ingrese una opcion: ")
        while(not opcion.isdigit() or (float(opcion) < 1 or float(opcion) > 10)):
            opcion = input("No es una opcion valida, por favor ingrese otra: ")

        match(opcion):
            case "1":
                flag_cargar_datos = True
                cargar_datos(archivocsv)
            case "2":
                if(flag_cargar_datos):
                    listar_cantidad_marcas(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "3":
                if(flag_cargar_datos):
                    listar_insumos_marca(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "4":
                if(flag_cargar_datos):
                    insumos_por_caracteristicas(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "5":
                if(flag_cargar_datos):
                    listar_insumos_ordenados(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "6":
                if(flag_cargar_datos):
                    realizar_compras(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "7":
                flag_JSON = True
                if(flag_cargar_datos):
                    guardar_json(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "8":
                if(flag_JSON):
                    leer_json()
                else:
                    print("Para realizar esto debes primero guardar los datos en un archivo JSON")
            case "9":
                if(flag_cargar_datos):
                    actualizar_precios(cargar_datos(archivocsv))
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "10":
                print("Saliste del programa")
                break

        os.system("pause")
