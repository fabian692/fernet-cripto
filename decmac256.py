import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def cargar_clave_personalizada():
    """Solicita la ruta de la clave y la carga."""
    ruta_clave = input("🔑 Ingresa la ruta del archivo de clave (clave.enc): ").strip()

    if not os.path.exists(ruta_clave):
        print("❌ Error: No se encontró el archivo de clave.")
        exit(1)

    with open(ruta_clave, "rb") as f:
        salt = base64.b64decode(f.readline().strip())  # Leer salt (no se usa en descifrado)
        clave = base64.b64decode(f.readline().strip())  # Leer clave

    print("🔓 Clave cargada correctamente.")
    return clave

def descifrar_archivo(ruta_cifrada: str, clave: bytes):
    """Descifra un archivo .enc usando AES en modo CBC y lo restaura con su nombre original."""
    try:
        # Leer IV y datos cifrados
        with open(ruta_cifrada, "rb") as f:
            iv = base64.b64decode(f.readline().strip())  # Leer IV
            datos_cifrados = base64.b64decode(f.read())  # Leer datos cifrados

        # Configurar el descifrador
        cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        datos_padded = decryptor.update(datos_cifrados) + decryptor.finalize()

        # Eliminar el padding (último byte indica cuántos bytes se agregaron)
        padding = datos_padded[-1]
        datos_originales = datos_padded[:-padding]

        # Restaurar el nombre del archivo original
        ruta_original = ruta_cifrada[:-4]  # Elimina la extensión ".enc"
        with open(ruta_original, "wb") as f:
            f.write(datos_originales)

        print(f"✅ Archivo descifrado: {ruta_original}")

        # 🚨 Eliminar el archivo cifrado después de descifrarlo
        os.remove(ruta_cifrada)
        print(f"🗑 Archivo cifrado eliminado: {ruta_cifrada}")

    except Exception as e:
        print(f"❌ Error descifrando {ruta_cifrada}: {e}")

def recorrer_y_descifrar(directorio: str, clave: bytes):
    """Recorre el directorio y descifra los archivos con extensión .enc"""
    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith(".enc"):  
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                descifrar_archivo(ruta_completa, clave)

# 1️⃣ Solicitar la ruta de la clave
clave = cargar_clave_personalizada()

# 2️⃣ Solicitar el directorio de los archivos cifrados
directorio_raiz = input("📂 Ingresa la ruta del directorio con los archivos cifrados: ").strip()

if not os.path.exists(directorio_raiz):
    print("❌ Error: El directorio no existe.")
    exit(1)

# 3️⃣ Ejecutar descifrado
recorrer_y_descifrar(directorio_raiz, clave)
