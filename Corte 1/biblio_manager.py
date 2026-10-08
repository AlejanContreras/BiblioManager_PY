ARCHIVO_BASICO = "ejemplares.txt"                    
ARCHIVO_DIRECTO = "ejemplares_directo.txt"           
ARCHIVO_USADO = "ejemplares_usado.txt"               
ARCHIVO_ORD_CATEGORIA = "ejemplares_ordenados_categoria.txt"  
ARCHIVO_ORD_AUTOR = "ejemplares_ordenados_autor.txt"          

# archivos temporales para mezcla directa
RUN_A = "run_a.txt"
RUN_B = "run_b.txt"
RUN_TEMP = "run_temp.txt"

DATOS_EJEMPLO = [
    (1, "Calculo I", 1, "Baldor", "Matematicas"),
    (0, "Calculo I", 2, "Baldor", "Matematicas"),
    (1, "El Principe", 3, "Maquiavelo", "Politica"),
    (0, "Fisica I", 4, "Serway", "Fisica"),
    (1, "Fisica I", 5, "Serway", "Fisica"),
    (0, "Etica a Nicomaco", 6, "Aristoteles", "Filosofia"),
    (0, "Algebra Lineal", 7, "Grossman", "Matematicas"),
]


# OPERACIONES BASICAS DE ARCHIVO
# crea y mantiene los 5 datos de cada ejemplar desde cero

#crear
def agregar_ejemplar(prestado, libro, ejemplar, autor, categoria):
    with open(ARCHIVO_BASICO, "a", encoding="utf-8") as archivo:
        linea = f"{prestado},{libro},{ejemplar},{autor},{categoria}\n"
        archivo.write(linea)

#leer
def listar_ejemplares():
    with open(ARCHIVO_BASICO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            print(campos)

#actualizar
def actualizar_ejemplar(id_buscado, nuevo_libro=None, nueva_categoria=None):
    lineas_nuevas = []
    with open(ARCHIVO_BASICO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            if campos[2] == str(id_buscado):
                if nuevo_libro:
                    campos[1] = nuevo_libro
                if nueva_categoria:
                    campos[4] = nueva_categoria
            lineas_nuevas.append(",".join(campos) + "\n")

    with open(ARCHIVO_BASICO, "w", encoding="utf-8") as archivo:
        archivo.writelines(lineas_nuevas)

#eliminar
def eliminar_ejemplar(id_buscado):
    lineas_nuevas = []
    with open(ARCHIVO_BASICO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            if campos[2] != str(id_buscado):
                lineas_nuevas.append(linea)

    with open(ARCHIVO_BASICO, "w", encoding="utf-8") as archivo:
        archivo.writelines(lineas_nuevas)

#cargar los 7 libros en el archivo
def cargar_datos_ejemplo():
    open(ARCHIVO_BASICO, "w", encoding="utf-8").close()
    for prestado, libro, ejemplar, autor, categoria in DATOS_EJEMPLO:
        agregar_ejemplar(prestado, libro, ejemplar, autor, categoria)
    print("Catalogo de ejemplo cargado (7 ejemplares).")


#ACCESO DIRECTO 
# cambia el estado de prestado a 0/1 prestado o no

ANCHO_LIBRO = 30
ANCHO_AUTOR = 20
ANCHO_CATEGORIA = 15
REGISTRO_LEN = 1 + ANCHO_LIBRO + 4 + ANCHO_AUTOR + ANCHO_CATEGORIA + 1
#len = length

def construir_registro(prestado, libro, ejemplar, autor, categoria):
    return (
        str(prestado).ljust(1) +
        libro[:ANCHO_LIBRO].ljust(ANCHO_LIBRO) +
        str(ejemplar).zfill(4) +
        autor[:ANCHO_AUTOR].ljust(ANCHO_AUTOR) +
        categoria[:ANCHO_CATEGORIA].ljust(ANCHO_CATEGORIA) +
        "\n"
    )


def preparar_archivo_directo(total_registros):
    with open(ARCHIVO_DIRECTO, "w", encoding="utf-8") as archivo:
        for i in range(total_registros):
            archivo.write(construir_registro(0, "", i + 1, "", ""))


def agregar_directo(prestado, libro, ejemplar, autor, categoria):
    registro = construir_registro(prestado, libro, ejemplar, autor, categoria)
    with open(ARCHIVO_DIRECTO, "r+", encoding="utf-8") as archivo:
        archivo.seek((ejemplar - 1) * REGISTRO_LEN)
        archivo.write(registro)


def leer_directo(ejemplar):
    with open(ARCHIVO_DIRECTO, "r", encoding="utf-8") as archivo:
        archivo.seek((ejemplar - 1) * REGISTRO_LEN)
        registro = archivo.read(REGISTRO_LEN)

    if len(registro) < REGISTRO_LEN:
        print("Ese ejemplar no existe en el archivo directo.")
        return None

    prestado = registro[0:1]
    libro = registro[1:1 + ANCHO_LIBRO].strip()
    idLeido = registro[1 + ANCHO_LIBRO:5 + ANCHO_LIBRO].strip()
    autor = registro[5 + ANCHO_LIBRO:5 + ANCHO_LIBRO + ANCHO_AUTOR].strip()
    categoria = registro[5 + ANCHO_LIBRO + ANCHO_AUTOR:5 + ANCHO_LIBRO + ANCHO_AUTOR + ANCHO_CATEGORIA].strip()

    estado = "PRESTADO" if prestado == "1" else "DISPONIBLE"
    print(f"[{idLeido}] {libro} - {autor} ({categoria}) - {estado}")
    return (prestado, libro, idLeido, autor, categoria)


def cambiar_estado_prestamo(ejemplar, nuevo_prestado):
    with open(ARCHIVO_DIRECTO, "r+", encoding="utf-8") as archivo:
        archivo.seek((ejemplar - 1) * REGISTRO_LEN)
        archivo.write(str(nuevo_prestado))


def sincronizar_directo_desde_catalogo():
    """Lee el catalogo maestro (ejemplares.txt) y reconstruye el archivo
    de longitud fija con esos mismos ejemplares."""
    with open(ARCHIVO_BASICO, "r", encoding="utf-8") as archivo:
        registros = [linea.strip().split(",") for linea in archivo if linea.strip()]

    if not registros:
        print("El catalogo esta vacio, no hay nada que sincronizar.")
        return

    preparar_archivo_directo(len(registros))
    for prestado, libro, ejemplar, autor, categoria in registros:
        agregar_directo(prestado, libro, int(ejemplar), autor, categoria)
    print(f"Archivo de acceso directo sincronizado ({len(registros)} ejemplares).")


#ORDENACION EXTERNA POR SELECCION REPETIDA 
# reordena tod el catalogo segun su categoria

INDICE_CATEGORIA = 5  # usado,prestado,libro,ejemplar,autor,categoria
INDICE_AUTOR_MEZCLA = 3  # prestado,libro,ejemplar,autor,categoria 


def contar_registros(archivo):
    total = 0
    with open(archivo, "r", encoding="utf-8") as f:
        for _ in f:
            total += 1
    return total


def preparar_archivo_usado_desde_catalogo():
    #copia el catalogo y le agrega un 0 como idenfificacion de usado
    with open(ARCHIVO_BASICO, "r", encoding="utf-8") as entrada, \
         open(ARCHIVO_USADO, "w", encoding="utf-8") as salida:
        for linea in entrada:
            if linea.strip():
                salida.write("0," + linea)


def buscar_minimo_no_usado(archivo, indice_campo):
    minimo = None
    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for linea in archivo_full:
            campos = linea.strip().split(",")
            if campos[0] == "1":
                continue
            valor = campos[indice_campo]  # categoria y autor no se convierte a int
            if minimo is None or valor < minimo[1]:
                minimo = (campos, valor)
    return minimo[0] if minimo else None


def marcar_usado(archivo, id_registro):
    lineas_nuevas = []
    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for linea in archivo_full:
            campos = linea.strip().split(",")
            if campos[3] == id_registro:
                campos[0] = "1"
            lineas_nuevas.append(",".join(campos))

    with open(archivo, "w", encoding="utf-8") as archivo_full:
        for linea in lineas_nuevas:
            archivo_full.write(linea + "\n")


def ordenar_externa(archivo_entrada, archivo_salida, indice_campo):
    total = contar_registros(archivo_entrada)
    with open(archivo_salida, "w", encoding="utf-8") as salida:
        for _ in range(total):
            registro = buscar_minimo_no_usado(archivo_entrada, indice_campo)
            if registro is None:
                break
            salida.write(",".join(registro) + "\n")
            marcar_usado(archivo_entrada, registro[3])


def ejecutar_ordenacion_externa():
    preparar_archivo_usado_desde_catalogo()
    ordenar_externa(ARCHIVO_USADO, ARCHIVO_ORD_CATEGORIA, INDICE_CATEGORIA)
    print("\nEjemplares ordenados por CATEGORIA:")
    with open(ARCHIVO_ORD_CATEGORIA, "r", encoding="utf-8") as f:
        for linea in f:
            print(linea.strip())

#ORDENACION POR MEZCLA DIRECTA reordena todo el catalogo segun el autor

def distribuir_corridas(archivo_entrada, archivo_a, archivo_b, tam_corrida):
    #lee todas las lineas del archivo de entrada
    with open(archivo_entrada, "r", encoding="utf-8") as entrada:
        lineas = entrada.readlines()

    #las reparte en dos archivos (A y B), alternando de a tamaño del grupo ordenado en tamaño del grupo ordenado
    with open(archivo_a, "w", encoding="utf-8") as a, \
         open(archivo_b, "w", encoding="utf-8") as b:
        turno = 0
        for i in range(0, len(lineas), tam_corrida):
            bloque = lineas[i:i + tam_corrida]
            destino = a if turno == 0 else b
            destino.writelines(bloque)
            turno = 1 - turno  #cambia de A a B (o de B a A) para el siguiente bloque


def fusionar_pares(archivo_a, archivo_b, archivo_salida, tam_corrida, indice_campo):
    with open(archivo_a, "r", encoding="utf-8") as a, \
         open(archivo_b, "r", encoding="utf-8") as b, \
         open(archivo_salida, "w", encoding="utf-8") as salida:

        lineas_a = a.readlines()
        lineas_b = b.readlines()
        # indice a y b
        ia, ib = 0, 0

        #mientras queden bloques por comparar en A o en B
        while ia < len(lineas_a) or ib < len(lineas_b):
            #toma el siguiente bloque de A y el siguiente de B
            corrida_a = lineas_a[ia:ia + tam_corrida]
            corrida_b = lineas_b[ib:ib + tam_corrida]
            ia += tam_corrida
            ib += tam_corrida

            #compara elemento por elemento y escribe primero el mas chico de los dos
            ja, jb = 0, 0
            while ja < len(corrida_a) and jb < len(corrida_b):
                valor_a = corrida_a[ja].strip().split(",")[indice_campo]
                valor_b = corrida_b[jb].strip().split(",")[indice_campo]
                if valor_a <= valor_b:
                    salida.write(corrida_a[ja])
                    ja += 1
                else:
                    salida.write(corrida_b[jb])
                    jb += 1
            #si a alguno de los dos bloques le quedo algo sin escribir, se agrega al final
            while ja < len(corrida_a):
                salida.write(corrida_a[ja])
                ja += 1
            while jb < len(corrida_b):
                salida.write(corrida_b[jb])
                jb += 1


def ordenar_mezcla_directa(archivo_entrada, archivo_salida, indice_campo):
    total = contar_registros(archivo_entrada)
    #si hay 0 o 1 ejemplares no hay nada que ordenar
    if total <= 1:
        with open(archivo_entrada, "r", encoding="utf-8") as e, \
             open(archivo_salida, "w", encoding="utf-8") as s:
            s.writelines(e.readlines())
        return

    #primer reparto: bloques de 1 en 1, porque todavia nada esta ordenado
    distribuir_corridas(archivo_entrada, RUN_A, RUN_B, 1)
    tam_corrida = 1
    #cada vuelta duplica el tamano del bloque ya ordenado (1, 2, 4, 8...) hasta cubrir todo
    while tam_corrida < total:
        fusionar_pares(RUN_A, RUN_B, RUN_TEMP, tam_corrida, indice_campo)
        tam_corrida *= 2
        if tam_corrida < total:
            #se reparte de nuevo, ahora por bloques del nuevo tamaño, para la siguiente vuelta
            distribuir_corridas(RUN_TEMP, RUN_A, RUN_B, tam_corrida)

    #ya quedo un solo bloque con todo el archivo ordenado, se guarda como resultado final
    with open(RUN_TEMP, "r", encoding="utf-8") as e, \
         open(archivo_salida, "w", encoding="utf-8") as s:
        s.writelines(e.readlines())


def ejecutar_mezcla_directa():
    #muestra el resultado ya ordenado por autor
    ordenar_mezcla_directa(ARCHIVO_BASICO, ARCHIVO_ORD_AUTOR, INDICE_AUTOR_MEZCLA)
    print("\nEjemplares ordenados por AUTOR:")
    with open(ARCHIVO_ORD_AUTOR, "r", encoding="utf-8") as f:
        for linea in f:
            print(linea.strip())


if __name__ == "__main__":

    #OPERACIONES BASICAS
    cargar_datos_ejemplo()
    print("\nCATALOGO INICIAL")
    listar_ejemplares()
    actualizar_ejemplar(4, nueva_categoria="Ciencias")
    print("\nCATALOGO DESPUES DE ACTUALIZAR EL EJEMPLAR 4")
    listar_ejemplares()

    #ACCESO DIRECTO
    sincronizar_directo_desde_catalogo()
    print("\nLECTURA DIRECTA")
    leer_directo(3)
    leer_directo(1)
    print("\nCAMBIANDO EL ESTADO DE PRESTAMO DEL EJEMPLAR 1")
    cambiar_estado_prestamo(1, 0)
    leer_directo(1)

    #ORDENACION EXTERNA
    ejecutar_ordenacion_externa()
    #MEZCLA DIRECTA
    ejecutar_mezcla_directa()
