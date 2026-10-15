ARCHIVO_BASICO = "ejemplares.txt"
ARCHIVO_ARBOL = "arbol_categorias.txt"


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)


def buscar_hijo_directo(nodo_padre, dato_buscado):
    for hijo in nodo_padre.hijos:
        if hijo.dato == dato_buscado:
            return hijo
    return None


def construir_arbol_desde_catalogo(ruta_archivo=ARCHIVO_BASICO):
    raiz = Nodo("Biblioteca")

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            prestado, libro, ejemplar, autor, categoria = linea.split(",")

            nodo_categoria = buscar_hijo_directo(raiz, categoria)
            if nodo_categoria is None:
                nodo_categoria = Nodo(categoria)
                raiz.agregar_hijo(nodo_categoria)

            nodo_libro = buscar_hijo_directo(nodo_categoria, libro)
            if nodo_libro is None:
                nodo_libro = Nodo(libro)
                nodo_categoria.agregar_hijo(nodo_libro)

            estado = "Prestado" if prestado == "1" else "Disponible"
            dato_ejemplar = f"Ejemplar {ejemplar} - {autor} - {estado}"
            nodo_libro.agregar_hijo(Nodo(dato_ejemplar))

    return raiz


def recorrido_preorden(nodo, nivel=0, resultado=None):
    if resultado is None:
        resultado = []
    resultado.append((nivel, nodo.dato))
    for hijo in nodo.hijos:
        recorrido_preorden(hijo, nivel + 1, resultado)
    return resultado


def recorrido_postorden(nodo, nivel=0, resultado=None):
    if resultado is None:
        resultado = []
    for hijo in nodo.hijos:
        recorrido_postorden(hijo, nivel + 1, resultado)
    resultado.append((nivel, nodo.dato))
    return resultado


def mostrar(nodo, nivel=0):
    print("  " * nivel + nodo.dato)
    for hijo in nodo.hijos:
        mostrar(hijo, nivel + 1)


def calcular_altura(nodo):
    if not nodo.hijos:
        return 0
    alturas_hijos = []
    for hijo in nodo.hijos:
        alturas_hijos.append(calcular_altura(hijo))
    return 1 + max(alturas_hijos)


def contar_nodos(nodo):
    total = 1
    for hijo in nodo.hijos:
        total += contar_nodos(hijo)
    return total


def contar_hojas(nodo):
    if not nodo.hijos:
        return 1
    total = 0
    for hijo in nodo.hijos:
        total += contar_hojas(hijo)
    return total


def buscar(nodo, dato):
    if nodo.dato == dato:
        return True
    for hijo in nodo.hijos:
        if buscar(hijo, dato):
            return True
    return False


def nivel_de(nodo, dato, nivel=0):
    if nodo.dato == dato:
        return nivel
    for hijo in nodo.hijos:
        nivel_hijo = nivel_de(hijo, dato, nivel + 1)
        if nivel_hijo != -1:
            return nivel_hijo
    return -1


def eliminar_nodo(nodo_padre, dato_hijo):
    for hijo in nodo_padre.hijos:
        if hijo.dato == dato_hijo:
            nodo_padre.hijos.remove(hijo)
            return True
    return False


def guardar_arbol(nodo, ruta_archivo=ARCHIVO_ARBOL):
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        _escribir_nodo(nodo, archivo, nivel=0)


def _escribir_nodo(nodo, archivo, nivel):
    archivo.write(f"{nivel};{nodo.dato}\n")
    for hijo in nodo.hijos:
        _escribir_nodo(hijo, archivo, nivel + 1)


def cargar_arbol(ruta_archivo=ARCHIVO_ARBOL):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    raiz = None
    ultimo_por_nivel = {}

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        nivel_texto, dato = linea.split(";", 1)
        nivel = int(nivel_texto)
        nodo_actual = Nodo(dato)

        if nivel == 0:
            raiz = nodo_actual
        else:
            padre = ultimo_por_nivel[nivel - 1]
            padre.agregar_hijo(nodo_actual)

        ultimo_por_nivel[nivel] = nodo_actual

    return raiz


print("=" * 70)
print("1) CONSTRUCCION DEL ARBOL DESDE EL CATALOGO (ejemplares.txt)")
print("=" * 70)
arbol = construir_arbol_desde_catalogo()
mostrar(arbol)

print("\n" + "=" * 70)
print("2) ALTURA Y CONTEO DE NODOS / HOJAS")
print("=" * 70)
print("Altura del arbol:", calcular_altura(arbol))
print("Numero total de nodos:", contar_nodos(arbol))
print("Numero de hojas (ejemplares):", contar_hojas(arbol))

print("\n" + "=" * 70)
print("3) RECORRIDO PREORDEN")
print("=" * 70)
for nivel, dato in recorrido_preorden(arbol):
    print("  " * nivel + dato)

print("\n" + "=" * 70)
print("4) RECORRIDO POSTORDEN")
print("=" * 70)
for nivel, dato in recorrido_postorden(arbol):
    print("  " * nivel + dato)

print("\n" + "=" * 70)
print("5) BUSQUEDA")
print("=" * 70)
print("Buscar 'Fisica I':", buscar(arbol, "Fisica I"), "- nivel", nivel_de(arbol, "Fisica I"))
print("Buscar 'Quimica II' (no existe):", buscar(arbol, "Quimica II"))

print("\n" + "=" * 70)
print("6) ELIMINACION DE UN NODO (con todo su subarbol)")
print("=" * 70)
print("Antes de eliminar la categoria 'Politica':")
mostrar(arbol)
eliminar_nodo(arbol, "Politica")
print("\nDespues de eliminar la categoria 'Politica' (se va 'El Principe' y su ejemplar):")
mostrar(arbol)
print("Numero total de nodos tras la eliminacion:", contar_nodos(arbol))

print("\n" + "=" * 70)
print("7) PERSISTENCIA: GUARDAR Y CARGAR EL ARBOL")
print("=" * 70)
print("Arbol original (en memoria):\n")
mostrar(arbol)

guardar_arbol(arbol)

arbol_recuperado = cargar_arbol()
print("\nArbol recuperado desde 'arbol_categorias.txt':\n")
mostrar(arbol_recuperado)
