# Biblio Manager

Sistema de gestión bibliotecaria construido de forma progresiva a lo largo del curso de Estructuras de Datos II (Fundación Universitaria Compensar). Proyecto de John Alejandro Contreras Valencia y Thomas Andrés Romero Florez.

## Organización del repositorio

El código está organizado en una carpeta por corte evaluativo:

```
codigo/
├── Corte 1/   -> persistencia en archivos (acceso secuencial, acceso directo,
│                 ordenación externa, mezcla directa)
└── Corte 2/   -> árbol genérico del catálogo (Biblioteca -> Categoría -> Libro
                  -> Ejemplar), construido sobre los mismos archivos del Corte 1
```

## Requisitos

Python 3.10 o superior. El proyecto no usa ninguna librería externa (ver `requirements.txt`): solo la biblioteca estándar de Python.

## Cómo ejecutar

### Corte 1 — persistencia en archivos

```
cd "Corte 1"
python biblio_manager.py
```

Al ejecutarse, carga el catálogo de ejemplo (`DATOS_EJEMPLO`), genera el archivo `ejemplares.txt` y muestra en la terminal, en orden, el catálogo inicial, una actualización de ejemplar, la lectura por acceso directo, un cambio de estado de préstamo, la ordenación externa por categoría y la ordenación por mezcla directa por autor. No requiere ninguna entrada del usuario.

### Corte 2 — árbol genérico del catálogo

```
cd "Corte 2"
python arbol_biblioteca.py
```

Requiere que exista `ejemplares.txt` en la misma carpeta (ya incluido, con los mismos 7 ejemplares de ejemplo del Corte 1). Al ejecutarse, construye el árbol del catálogo y muestra en la terminal, en orden: la construcción del árbol, la altura y el conteo de nodos y hojas, los recorridos en preorden y en posorden, una búsqueda existente y otra inexistente, la eliminación de una categoría completa con su descendencia, y finalmente guarda el árbol en `arbol_categorias.txt` y verifica que, al recargarlo, coincide exactamente con el árbol guardado.

## Documento y demás entregables

El documento de entrega, los diagramas, el video de mockups y la presentación de cada corte están en la carpeta `Entrega_Avances_Proyectos` (fuera de este repositorio de código), organizados también por corte.
