import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Ruta donde se guardó la clave AES
KEY_FILE = "/home/parrot/Desktop/aes_key.bin"

# Cargar la clave AES
def load_key():
    if not os.path.exists(KEY_FILE):
        print("❌ ERROR: No se encontró la clave AES.")
        exit(1)
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Función para descifrar archivos
def decrypt_file(encrypted_path, key):
    try:
        with open(encrypted_path, "rb") as f:
            data = f.read()
        
        iv, ciphertext = data[:16], data[16:]  # Extrae IV y datos cifrados
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Quitar el padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        original_path = encrypted_path.replace(".enc", "")
        with open(original_path, "wb") as f:
            f.write(decrypted)

        os.remove(encrypted_path)  # Elimina el archivo cifrado
        print(f"Descifrado: {original_path}")

    except Exception as e:
        print(f"Error descifrando {encrypted_path}: {e}")

# Buscar y descifrar archivos
def decrypt_system():
    key = load_key()
    for root, _, files in os.walk("/"):
        for file in files:
            if file.endswith(".enc"):
                decrypt_file(os.path.join(root, file), key)

# Ejecutar descifrado
if __name__ == "__main__":
    decrypt_system()

