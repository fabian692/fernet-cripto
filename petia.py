from cryptography.fernet import Fernet
import os

def generate_key():
    """Genera y guarda una clave en un archivo."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Clave secreta generada y guardada en 'secret.key'.")

def load_key():
    """Carga la clave desde el archivo."""
    return open("secret.key", "rb").read()

def encrypt_file(file_path, fernet):
    """Cifra el contenido de un archivo y elimina el original."""
    with open(file_path, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    # Crea el archivo cifrado
    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    print(f"Archivo cifrado: {encrypted_file_path}")

    # Elimina el archivo original
    os.remove(file_path)
    print(f"Archivo original eliminado: {file_path}")

def encrypt_files_in_directory(directory):
    """Cifra todos los archivos en el directorio que no están cifrados y elimina los originales."""
    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Verifica que sea un archivo y no un directorio
        if os.path.isfile(file_path):
            # Cifra solo si no termina en .encrypted
            if not filename.endswith('.encrypted'):
                encrypt_file(file_path, fernet)

def decrypt_file(encrypted_file_path, fernet):
    """Descifra el contenido de un archivo cifrado."""
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    # Crea el archivo descifrado
    decrypted_file_path = encrypted_file_path.replace(".encrypted", "")
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)

    print(f"Archivo descifrado: {decrypted_file_path}")

def decrypt_files_in_directory(directory):
    """Descifra todos los archivos cifrados en el directorio."""
    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Verifica que sea un archivo y no un directorio
        if os.path.isfile(file_path):
            # Descifra solo si termina en .encrypted
            if filename.endswith('.encrypted'):
                decrypt_file(file_path, fernet)

def main():
    action = input("¿Deseas (g)enerar una clave, (e)ncriptar o (d)esencriptar archivos? (g/e/d): ")
    
    if action.lower() == 'g':
        generate_key()
    elif action.lower() == 'e':
        directory = input("Introduce la ruta del directorio a cifrar: ")
        if os.path.isdir(directory):
            encrypt_files_in_directory(directory)
            print("Proceso de cifrado completado.")
        else:
            print("La ruta no es un directorio válido.")
    elif action.lower() == 'd':
        directory = input("Introduce la ruta del directorio a descifrar: ")
        if os.path.isdir(directory):
            decrypt_files_in_directory(directory)
            print("Proceso de descifrado completado.")
        else:
            print("La ruta no es un directorio válido.")
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
