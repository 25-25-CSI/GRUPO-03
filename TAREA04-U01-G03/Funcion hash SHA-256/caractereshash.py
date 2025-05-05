import hashlib
import os
import time
from tabulate import tabulate  # pip install tabulate

# Método que genera el archivo con la cantidad de palabras especificada
def generar_archivo_texto(cantidad_palabras, ruta_archivo):
    palabras = "hola mundo " * cantidad_palabras  # Generar texto con palabras repetidas
    with open(ruta_archivo, "w") as archivo:
        archivo.write(palabras.strip())

# Método que lee el archivo, valida su contenido y genera el hash
def leer_y_generar_hash(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None, None, None, None, None

    # Medir el tiempo de lectura del archivo
    inicio_lectura = time.time()
    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.read().strip()
    fin_lectura = time.time()

    if not contenido:
        print(f"Error: El archivo {ruta_archivo} está vacío o es nulo.")
        return None, None, None, None, None

    tiempo_lectura = fin_lectura - inicio_lectura
    caracteres_antes = len(contenido.replace(" ", ""))

    # Medir el tiempo de generación del hash
    inicio_hash = time.time()
    hash_obj = hashlib.sha256(contenido.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    fin_hash = time.time()

    tiempo_hash = fin_hash - inicio_hash
    caracteres_despues = len(hash_hex)

    return hash_hex, tiempo_lectura, tiempo_hash, caracteres_antes, caracteres_despues

if __name__ == "__main__":
    carpeta_textos = "textos_generados_hash"
    if not os.path.exists(carpeta_textos):
        os.makedirs(carpeta_textos)

    cantidades_palabras = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    resultados = []

    archivo_resultados = "resultados_hash.txt"
    with open(archivo_resultados, "w") as archivo:
        archivo.write("Resultados de Hash:\n")
        archivo.write("Cantidad de Palabras | Hash SHA-256 | Tiempo Lectura (segundos) | Tiempo Hash (segundos) | Caracteres Antes | Caracteres Después\n")
        archivo.write("-" * 140 + "\n")

    for cantidad in cantidades_palabras:
        nombre_archivo = f"texto_{cantidad}_palabras.txt"
        ruta_archivo = os.path.join(carpeta_textos, nombre_archivo)

        print(f"Generando archivo con {cantidad} palabras...")
        generar_archivo_texto(cantidad, ruta_archivo)

        hash_hex, tiempo_lectura, tiempo_hash, caracteres_antes, caracteres_despues = leer_y_generar_hash(ruta_archivo)
        if hash_hex and tiempo_lectura and tiempo_hash:
            with open(archivo_resultados, "a") as archivo:
                archivo.write(f"{cantidad} | {hash_hex} | {tiempo_lectura:.6f} | {tiempo_hash:.6f} | {caracteres_antes} | {caracteres_despues}\n")

            resultados.append([
                cantidad,
                hash_hex,
                f"{tiempo_lectura:.6f} segundos",
                f"{tiempo_hash:.6f} segundos",
                caracteres_antes,
                caracteres_despues
            ])

    print("\nResultados Finales:")
    print(tabulate(resultados, headers=["Cantidad de Palabras", "Hash SHA-256", "Tiempo Lectura", "Tiempo Hash", "Caracteres Antes", "Caracteres Después"]))