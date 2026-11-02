import csv
import os

ruta_generos = "generos.csv"
ruta_peliculas = "peliculas.csv"
enc_generos = ["id_genero", "nombre", "baja"]
enc_peliculas = ["id_pelicula", "nombre_pelicula", "id_genero", "resena", "url_poster", "valoracion", "anio", "baja"]

def inicializar_archivo(ruta: str, enc: list) -> None:
    if not os.path.exists(ruta):
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(enc)

def leer_registros(ruta: str, enc: list) -> list:
    inicializar_archivo(ruta, enc)
    registros = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        for fila in lector:
            if len(fila) == len(enc):
                registros.append(fila)
    return registros

def guardar_registros(ruta: str, enc: list, registros: list) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(enc)
        escritor.writerows(registros)

def leer_activos(ruta: str, enc: list) -> list:
    activos = []
    for fila in leer_registros(ruta, enc):
        if fila[-1] == "0":
            activos.append(fila)
    return activos

def id_activo(ruta: str, enc: list, id_buscado: str) -> bool:
    for fila in leer_activos(ruta, enc):
        if fila[0] == id_buscado:
            return True
    return False

def agregar_registro(ruta: str, enc: list, registro: list) -> None:
    inicializar_archivo(ruta, enc)
    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        contenido = archivo.read()
    if contenido != "" and not contenido.endswith("\n"):
        with open(ruta, "a", encoding="utf-8", newline="") as archivo:
            archivo.write("\r\n")
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(registro)

def dar_de_baja(ruta: str, enc: list, id_buscado: str) -> bool:
    filas = leer_registros(ruta, enc)
    for fila in filas:
        if fila[0] == id_buscado and fila[-1] == "0":
            fila[-1] = "1"
            guardar_registros(ruta, enc, filas)
            return True
    return False

def genero_activo(id_genero: str) -> bool:
    return id_activo(ruta_generos, enc_generos, id_genero)

def buscar_id_genero(texto: str) -> str:
    for fila in leer_activos(ruta_generos, enc_generos):
        if fila[0] == texto or fila[1].lower() == texto.lower():
            return fila[0]
    return ""

def alta_genero() -> None:
    print("--- Alta de género ---")
    id_genero = input("Ingrese el ID: ").strip()

    if id_genero == "":
        print("El ID no puede estar vacío.")
    elif genero_activo(id_genero):
        print("Ese ID ya está activo.")
    else:
        nombre = input("Ingrese el nombre: ").strip()
        agregar_registro(ruta_generos, enc_generos, [id_genero, nombre, "0"])
        print("Género guardado.")

    input("Pulse Enter para continuar...")

def baja_genero() -> None:
    print("--- Baja de género ---")
    id_genero = input("Ingrese el ID: ").strip()

    if dar_de_baja(ruta_generos, enc_generos, id_genero):
        print("Género dado de baja.")
    else:
        print("No se encontró ese género activo.")

    input("Pulse Enter para continuar...")

def modificar_genero() -> None:
    print("--- Modificación de género ---")
    id_genero = input("Ingrese el ID: ").strip()

    if genero_activo(id_genero):
        nombre = input("Ingrese el nuevo nombre: ").strip()
        dar_de_baja(ruta_generos, enc_generos, id_genero)
        agregar_registro(ruta_generos, enc_generos, [id_genero, nombre, "0"])
        print("Género modificado.")
    else:
        print("No se encontró ese género activo.")

    input("Pulse Enter para continuar...")

def consultar_generos() -> None:
    print("\n--- GÉNEROS ACTIVOS ---")
    print(f"{enc_generos[0]:<10} | {enc_generos[1]:<25}")
    print("-" * 38)

    for fila in leer_activos(ruta_generos, enc_generos):
        print(f"{fila[0]:<10} | {fila[1]:<25}")

    input("Pulse Enter para continuar...")

def pedir_datos_pelicula() -> list:
    nombre = input("Ingrese el nombre de la película: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacío.")
        return []

    texto_genero = input("Ingrese el género (ID o nombre): ").strip()
    id_genero = buscar_id_genero(texto_genero)
    if id_genero == "":
        print("Ese género no existe o está dado de baja.")
        return []

    resena = input("Ingrese la reseña: ").strip()
    url_poster = input("Ingrese URL de portada (o Enter para omitir): ").strip()
    valoracion = input("Ingrese valoración (ej. 8.5): ").strip() or "S/C"
    anio = input("Ingrese el año (ej. 2014): ").strip()
    return [nombre, id_genero, resena, url_poster, valoracion, anio]

def alta_pelicula() -> None:
    print("--- Alta de película ---")
    id_pelicula = input("Ingrese el ID: ").strip()

    if id_pelicula == "":
        print("El ID no puede estar vacío.")
    elif id_activo(ruta_peliculas, enc_peliculas, id_pelicula):
        print("Ese ID ya está activo.")
    else:
        datos = pedir_datos_pelicula()
        if len(datos) > 0:
            registro = [id_pelicula, *datos, "0"]
            agregar_registro(ruta_peliculas, enc_peliculas, registro)
            print("Película guardada.")

    input("Pulse Enter para continuar...")

def baja_pelicula() -> None:
    print("--- Baja de película ---")
    id_pelicula = input("Ingrese el ID: ").strip()

    if dar_de_baja(ruta_peliculas, enc_peliculas, id_pelicula):
        print("Película dada de baja.")
    else:
        print("No se encontró esa película activa.")

    input("Pulse Enter para continuar...")

def modificar_pelicula() -> None:
    print("--- Modificación de película ---")
    id_pelicula = input("Ingrese el ID: ").strip()

    if not id_activo(ruta_peliculas, enc_peliculas, id_pelicula):
        print("No se encontró esa película activa.")
    else:
        datos = pedir_datos_pelicula()
        if len(datos) > 0:
            dar_de_baja(ruta_peliculas, enc_peliculas, id_pelicula)
            registro = [id_pelicula, *datos, "0"]
            agregar_registro(ruta_peliculas, enc_peliculas, registro)
            print("Película modificada.")

    input("Pulse Enter para continuar...")

def mostrar_peliculas(lista: list) -> None:
    if len(lista) == 0:
        print("No se encontraron películas.")
    else:
        print(f"{'ID':<8} | {'Nombre':<30} | {'Género':<8} | Reseña")
        print("-" * 80)
        for fila in lista:
            print(f"{fila[0]:<8} | {fila[1]:<30} | {fila[2]:<8} | {fila[3]}")
        print(f"\nTotal: {len(lista)}")

def consultar_por_genero() -> None:
    print("\n--- CONSULTA POR GÉNERO ---")
    texto_genero = input("Ingrese el género (ID o nombre): ").strip()
    id_genero = buscar_id_genero(texto_genero)
    encontradas = []

    for fila in leer_activos(ruta_peliculas, enc_peliculas):
        if fila[2] == id_genero:
            encontradas.append(fila)

    mostrar_peliculas(encontradas)
    input("Pulse Enter para continuar...")

def consultar_por_nombre() -> None:
    print("\n--- CONSULTA POR NOMBRE ---")
    texto = input("Ingrese el nombre o parte del nombre: ").strip().lower()
    encontradas = []

    if texto == "":
        print("Debe ingresar un texto.")
    else:
        for fila in leer_activos(ruta_peliculas, enc_peliculas):
            if texto in fila[1].lower():
                encontradas.append(fila)
        mostrar_peliculas(encontradas)

    input("Pulse Enter para continuar...")

def menu_generos() -> None:
    while True:
        print("\n--- MENÚ DE GÉNEROS ---")
        print("1. Alta de género")
        print("2. Baja de género")
        print("3. Modificar género")
        print("4. Consultar géneros")
        print("5. Volver")

        opcion = input("Elija una opción: ").strip()

        match opcion:
            case "1":
                alta_genero()
            case "2":
                baja_genero()
            case "3":
                modificar_genero()
            case "4":
                consultar_generos()
            case "5":
                break
            case _:
                print("Opción incorrecta.")

def menu_abm_peliculas() -> None:
    while True:
        print("\n--- MENÚ DE PELÍCULAS ---")
        print("1. Alta de película")
        print("2. Baja de película")
        print("3. Modificar película")
        print("4. Volver")

        opcion = input("Elija una opción: ").strip()

        match opcion:
            case "1":
                alta_pelicula()
            case "2":
                baja_pelicula()
            case "3":
                modificar_pelicula()
            case "4":
                break
            case _:
                print("Opción incorrecta.")

def menu_consultas_peliculas() -> None:
    while True:
        print("\n--- CONSULTAS DE PELÍCULAS ---")
        print("1. Consulta por género")
        print("2. Consulta por nombre")
        print("3. Volver")

        opcion = input("Elija una opción: ").strip()

        match opcion:
            case "1":
                consultar_por_genero()
            case "2":
                consultar_por_nombre()
            case "3":
                break
            case _:
                print("Opción incorrecta.")

def menu_principal() -> None:
    inicializar_archivo(ruta_generos, enc_generos)
    inicializar_archivo(ruta_peliculas, enc_peliculas)

    while True:
        print("\n=== CATÁLOGO DE PELÍCULAS ===")
        print("1. ABM de géneros y consultas (Programas 1 y 3)")
        print("2. ABM de películas (Programa 2)")
        print("3. Consultas y búsquedas de películas (Programa 4)")
        print("4. Salir")

        opcion = input("Elija una opción: ").strip()

        match opcion:
            case "1":
                menu_generos()
            case "2":
                menu_abm_peliculas()
            case "3":
                menu_consultas_peliculas()
            case "4":
                print("Fin del programa.")
                break
            case _:
                print("Opción incorrecta.")

if __name__ == "__main__":
    menu_principal()