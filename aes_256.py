# -*- coding: utf-8 -*-
"""aes-256.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11kSw7Wdzv7slBJ1igEtrf0MuhSb6_NUN
"""

pip install cryptography

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64

# Función para generar una clave AES de 32 bytes
def generar_clave(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Función para guardar la clave en un archivo
def guardar_clave(key: bytes, filepath: str):
    with open(filepath, 'wb') as f:
        f.write(base64.b64encode(key))
    print(f"Clave guardada en: {filepath}")

# Función para cargar la clave desde un archivo
def cargar_clave(filepath: str) -> bytes:
    with open(filepath, 'rb') as f:
        key = base64.b64decode(f.read())
    print(f"Clave cargada desde: {filepath}")
    return key

# Función para cifrar un archivo
def cifrar_archivo(filepath: str, key: bytes, output_folder: str):
    with open(filepath, 'rb') as f:
        data = f.read()

    # Relleno para que sea múltiplo del bloque
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Genera un IV aleatorio
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Guarda el archivo cifrado
    encrypted_file_path = os.path.join(output_folder, os.path.basename(filepath) + '.enc')
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + encrypted_data)
    print(f"Archivo cifrado guardado en: {encrypted_file_path}")

    # Elimina el archivo original
    os.remove(filepath)
    print(f"Archivo original eliminado: {filepath}")

# Función para descifrar un archivo
def descifrar_archivo(filepath: str, key: bytes, output_folder: str):
    with open(filepath, 'rb') as f:
        data = f.read()

    # Extrae IV y datos cifrados
    iv = data[:16]
    encrypted_data = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Quita el relleno
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Guarda el archivo descifrado
    decrypted_file_path = os.path.join(output_folder, os.path.basename(filepath).replace('.enc', ''))
    with open(decrypted_file_path, 'wb') as f:
        f.write(unpadded_data)
    print(f"Archivo descifrado guardado en: {decrypted_file_path}")

    # Elimina el archivo cifrado
    os.remove(filepath)
    print(f"Archivo cifrado eliminado: {filepath}")

# Preguntar si el usuario quiere cifrar o descifrar
def main():
    print("=== Sistema de Cifrado/Descifrado AES ===")
    clave_path = './clave_aes.key'

    # Preguntar si cargar una clave existente o generar una nueva
    if os.path.exists(clave_path):
        usar_clave_existente = input("¿Deseas cargar la clave existente? (s/n): ").strip().lower() == 's'
        if usar_clave_existente:
            key = cargar_clave(clave_path)
        else:
            print("Generando nueva clave...")
            password = input("Introduce una contraseña para generar la clave: ")
            salt = os.urandom(16)  # Sal aleatoria
            key = generar_clave(password, salt)
            guardar_clave(key, clave_path)
    else:
        print("No se encontró una clave existente. Generando nueva clave...")
        password = input("Introduce una contraseña para generar la clave: ")
        salt = os.urandom(16)  # Sal aleatoria
        key = generar_clave(password, salt)
        guardar_clave(key, clave_path)

    # Carpetas
    input_folder = input('./input_files')
    encrypted_folder = input('./encrypted_files')
    decrypted_folder = input('./decrypted_files')

    # Crear carpetas de salida si no existen
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(encrypted_folder, exist_ok=True)
    os.makedirs(decrypted_folder, exist_ok=True)

    # Preguntar al usuario
    opcion = input("¿Qué deseas hacer? (cifrar/descifrar): ").strip().lower()

    if opcion == "cifrar":
        for filename in os.listdir(input_folder):
            filepath = os.path.join(input_folder, filename)
            if os.path.isfile(filepath):
                cifrar_archivo(filepath, key, encrypted_folder)
        print("Todos los archivos en la carpeta de entrada han sido cifrados y los originales eliminados.")
    elif opcion == "descifrar":
        for filename in os.listdir(encrypted_folder):
            filepath = os.path.join(encrypted_folder, filename)
            if os.path.isfile(filepath):
                descifrar_archivo(filepath, key, decrypted_folder)
        print("Todos los archivos cifrados han sido descifrados y los originales eliminados.")
    else:
        print("Opción no válida. Por favor, elige 'cifrar' o 'descifrar'.")

if __name__ == "__main__":
    main()