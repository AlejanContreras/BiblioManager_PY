# =====================================================================
# ARBOL GENERICO - BIBLIO MANAGER (Segundo momento evaluativo)
# =====================================================================
# Este modulo representa el catalogo de Biblio Manager como un arbol
# generico (N-aria, no binario) con 4 niveles:
#
#   Nivel 0: raiz          -> "Biblioteca"
#   Nivel 1: categoria     -> ej. "Matematicas", "Fisica"
#   Nivel 2: libro         -> ej. "Calculo I", "Fisica I"
#   Nivel 3: ejemplar      -> hoja: una copia fisica de un libro
#
# Se eligio esta jerarquia (y no un arbol binario) porque la relacion real
# entre categorias, libros y ejemplares NO es de "menor/mayor" como en un
# arbol binario de busqueda: una categoria puede tener varios libros, y un
# libro puede tener varios ejemplares. Esa relacion de "varios hijos por
# nodo" es exactamente lo que modela un arbol generico.
#
# La clase Nodo y las funciones de guardado/carga del arbol siguen el
# mismo diseno visto en clase (sesiones 24_09 y 1_10 de Estructuras de
# Datos II: arbol_con_archivo.py, arbol_generos_musica.py y
# ProfundizacionArboles.py): un nodo solo guarda "dato" (un texto) e
# "hijos", y agregar_hijo es un METODO de la propia clase Nodo, no una
# funcion aparte. Por eso cualquier nodo, sin importar su nivel, ya sabe
# agregarse hijos a si mismo: esa es la funcion reutilizable que en el
# Taller Autonomo de arboles no existia (alli cada relacion se armaba a
# mano, caso por caso).
#
# El arbol se construye a partir del MISMO archivo de persistencia que ya
# se usaba en el primer momento evaluativo (ARCHIVO_BASICO = ejemplares.txt,
# formato "prestado,libro,ejemplar,autor,categoria"), para que el arbol no
# sea una estructura aislada sino una lectura jerarquica de los datos que la
# aplicacion ya guarda en disco. Como el nodo solo tiene un campo "dato", la
# informacion de autor y estado de prestamo de cada ejemplar se guarda como
# parte de ese mismo texto (ver construir_arbol_desde_catalogo).
# =====================================================================

ARCHIVO_BASICO = "ejemplares.txt"          # mismo archivo del primer momento
ARCHIVO_ARBOL = "arbol_categorias.txt"     # persistencia propia del arbol


# ---------------------------------------------------------------------
# NODO DEL ARBOL
# ---------------------------------------------------------------------
class Nodo:
    """Un nodo generico del arbol, con la misma forma en cualquier nivel.

    Atributos:
        dato   (str): texto que identifica al nodo. Segun el nivel donde
                       quede el nodo es el nombre de la categoria, el
                       titulo del libro, o la descripcion de un ejemplar
                       (numero, autor y estado de prestamo).
        hijos  (list[Nodo]): hijos directos de este nodo. Puede tener
                       0, 1 o muchos hijos: por eso es un arbol generico
                       y no binario.
    """

    def __init__(self, dato):
        self.dato = dato
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        """Agrega nodo_hijo como hijo directo de este nodo. Al ser un
        metodo de la propia clase, sirve igual para colgar una categoria
        de la raiz, un libro de una categoria, o un ejemplar de un libro:
        es la unica forma de insertar usada en todo el modulo."""
        self.hijos.append(nodo_hijo)

    def __repr__(self):
        return f"Nodo({self.dato})"


def buscar_hijo_directo(nodo_padre, dato_buscado):
    """Busca entre los HIJOS DIRECTOS de nodo_padre uno cuyo dato sea
    dato_buscado. Se usa al construir el arbol, para saber si una
    categoria o un libro ya existen antes de crear uno nuevo (y asi no
    duplicar nodos cuando dos ejemplares comparten libro o categoria)."""
    for hijo in nodo_padre.hijos:
        if hijo.dato == dato_buscado:
            return hijo
    return None


# ---------------------------------------------------------------------
# CONSTRUCCION DEL ARBOL A PARTIR DEL CATALOGO (integracion con archivos)
# ---------------------------------------------------------------------
def construir_arbol_desde_catalogo(ruta_archivo=ARCHIVO_BASICO):
    """Lee el catalogo plano (el mismo ejemplares.txt del primer momento,
    formato 'prestado,libro,ejemplar,autor,categoria') y construye el
    arbol Biblioteca -> Categoria -> Libro -> Ejemplar.

    Por cada linea del archivo:
      1. Busca (o crea) el nodo de la categoria bajo la raiz.
      2. Busca (o crea) el nodo del libro bajo esa categoria.
      3. Crea el nodo del ejemplar (siempre nuevo, es la hoja) bajo el
         libro. Como el nodo solo tiene 'dato', el autor y el estado de
         prestamo se escriben dentro del mismo texto del nodo.
    Todas las inserciones usan agregar_hijo, el metodo propio de Nodo.
    """
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


# ---------------------------------------------------------------------
# RECORRIDOS (preorden y postorden)
# ---------------------------------------------------------------------
def recorrido_preorden(nodo, nivel=0, resultado=None):
    """Recorrido PREORDEN: primero se visita el nodo, despues sus hijos
    (de izquierda a derecha). Util para mostrar la jerarquia de arriba
    hacia abajo y para guardar el arbol en archivo (ver guardar_arbol),
    porque un padre siempre aparece ANTES que sus hijos."""
    if resultado is None:
        resultado = []
    resultado.append((nivel, nodo.dato))
    for hijo in nodo.hijos:
        recorrido_preorden(hijo, nivel + 1, resultado)
    return resultado


def recorrido_postorden(nodo, nivel=0, resultado=None):
    """Recorrido POSTORDEN: primero se visitan todos los hijos, y al final
    el propio nodo. Util, por ejemplo, para procesos que necesitan resolver
    primero las partes mas profundas del arbol (los ejemplares) antes de
    resumir la informacion del nodo que los contiene (el libro o la
    categoria)."""
    if resultado is None:
        resultado = []
    for hijo in nodo.hijos:
        recorrido_postorden(hijo, nivel + 1, resultado)
    resultado.append((nivel, nodo.dato))
    return resultado


def mostrar(nodo, nivel=0):
    """Imprime el arbol con sangria segun el nivel, para verlo de forma
    legible en consola (demo en vivo). Recorre en preorden, igual que
    'mostrar' en el material de clase."""
    print("  " * nivel + nodo.dato)
    for hijo in nodo.hijos:
        mostrar(hijo, nivel + 1)


# ---------------------------------------------------------------------
# ALTURA, CONTEO Y BUSQUEDA (recursivos)
# ---------------------------------------------------------------------
def calcular_altura(nodo):
    """Altura de un nodo = numero de aristas desde ese nodo hasta la hoja
    mas profunda de su subarbol.

    Caso base: un nodo sin hijos (una hoja, aqui siempre un ejemplar)
    tiene altura 0.
    Caso recursivo: la altura es 1 (la arista hacia el hijo) + la mayor
    altura entre todos los hijos.
    """
    if not nodo.hijos:
        return 0
    alturas_hijos = []
    for hijo in nodo.hijos:
        alturas_hijos.append(calcular_altura(hijo))
    return 1 + max(alturas_hijos)


def contar_nodos(nodo):
    """Cuenta TODOS los nodos del subarbol (incluyendo el propio nodo).

    Caso base: si no hay hijos, el subarbol tiene 1 nodo (el mismo nodo).
    Caso recursivo: 1 (el propio nodo) + la suma de nodos de cada hijo.
    """
    total = 1
    for hijo in nodo.hijos:
        total += contar_nodos(hijo)
    return total


def contar_hojas(nodo):
    """Cuenta solo las hojas del subarbol (nodos sin hijos; en este arbol,
    siempre nodos tipo ejemplar).

    Caso base: un nodo sin hijos ES una hoja -> cuenta como 1.
    Caso recursivo: no es hoja -> se suman las hojas de cada hijo.
    """
    if not nodo.hijos:
        return 1
    total = 0
    for hijo in nodo.hijos:
        total += contar_hojas(hijo)
    return total


def buscar(nodo, dato):
    """Busqueda recursiva en todo el arbol (no solo en los hijos directos).

    Caso base: el dato del nodo actual coincide con el buscado -> True.
    Caso recursivo: no coincide -> se pregunta lo mismo a cada hijo, hasta
    encontrarlo o hasta agotar las hojas.
    """
    if nodo.dato == dato:
        return True
    for hijo in nodo.hijos:
        if buscar(hijo, dato):
            return True
    return False


# ---------------------------------------------------------------------
# ELIMINACION (un nodo + todo su subarbol, de la lista de hijos del padre)
# ---------------------------------------------------------------------
def eliminar_nodo(nodo_padre, dato_hijo):
    """Quita de nodo_padre.hijos el hijo directo cuyo dato sea dato_hijo,
    junto con TODO su subarbol (todos sus descendientes se van con el,
    porque Python libera la referencia completa al quitarla de la lista).

    Devuelve True si se elimino algo, False si no se encontro entre los
    hijos directos de nodo_padre.
    """
    for hijo in nodo_padre.hijos:
        if hijo.dato == dato_hijo:
            nodo_padre.hijos.remove(hijo)
            return True
    return False


# ---------------------------------------------------------------------
# PERSISTENCIA DEL ARBOL EN ARCHIVO DE TEXTO
# ---------------------------------------------------------------------
def guardar_arbol(nodo, ruta_archivo=ARCHIVO_ARBOL):
    """Guarda el arbol en un archivo de texto plano, una linea por nodo,
    en orden PREORDEN, con el formato 'nivel;dato'.

    Se usa preorden (y no postorden) porque al guardar en ese orden, el
    padre de cada nodo SIEMPRE aparece en una linea anterior con nivel
    inmediatamente menor. Eso es justamente lo que permite reconstruir la
    jerarquia completa al leer el archivo de nuevo (ver cargar_arbol).
    """
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        _escribir_nodo(nodo, archivo, nivel=0)


def _escribir_nodo(nodo, archivo, nivel):
    archivo.write(f"{nivel};{nodo.dato}\n")
    for hijo in nodo.hijos:
        _escribir_nodo(hijo, archivo, nivel + 1)


def cargar_arbol(ruta_archivo=ARCHIVO_ARBOL):
    """Reconstruye el arbol leyendo el archivo generado por guardar_arbol.

    Como el archivo quedo en orden preorden, el padre de cada linea nueva
    es siempre el ULTIMO nodo que se leyo en el nivel inmediatamente
    anterior. Por eso se guarda en 'ultimo_por_nivel' una referencia al
    nodo mas reciente creado en cada nivel, y se usa esa referencia como
    padre al insertar el nodo actual (con agregar_hijo, el mismo metodo
    que usa el resto del modulo).
    """
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


# ---------------------------------------------------------------------
# VERIFICACION DE INTEGRIDAD (arbol guardado == arbol recargado)
# ---------------------------------------------------------------------
def verificar_persistencia(raiz_original, ruta_archivo=ARCHIVO_ARBOL):
    """Guarda el arbol, lo vuelve a leer desde el archivo, y compara el
    recorrido preorden de ambos para confirmar que la persistencia no
    perdio ni altero ningun dato.

    Esto responde directamente a la observacion del Taller Autonomo de
    arboles: alli no existia ninguna verificacion programatica de que el
    arbol recargado coincidiera con el guardado; aqui se hace de forma
    automatica cada vez que se guarda el arbol.
    """
    guardar_arbol(raiz_original, ruta_archivo)
    raiz_recargada = cargar_arbol(ruta_archivo)

    original = recorrido_preorden(raiz_original)
    recargado = recorrido_preorden(raiz_recargada)
    coincide = original == recargado

    print("\nVERIFICACION DE PERSISTENCIA")
    if coincide:
        print(f"OK -> el arbol recargado desde '{ruta_archivo}' coincide "
              f"exactamente con el arbol guardado ({len(original)} nodos).")
    else:
        print("ERROR -> el arbol recargado NO coincide con el original.")
    return coincide


# =====================================================================
# DEMOSTRACION (ejecucion en vivo / evidencia de pruebas)
# =====================================================================
if __name__ == "__main__":

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
    print("Buscar 'Fisica I':", buscar(arbol, "Fisica I"))
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
    print("7) PERSISTENCIA Y VERIFICACION")
    print("=" * 70)
    verificar_persistencia(arbol)
