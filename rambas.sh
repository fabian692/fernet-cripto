#!/bin/bash

# Ruta del directorio a recorrer (cámbialo según tus necesidades)
RUTA="/home/parrot/Documentos"

# Genera una clave AES-256 aleatoria (32 bytes = 256 bits, codificada en base64)
CLAVE=$(openssl rand -base64 32)
echo "Clave generada: $CLAVE"
echo "Guarda esta clave en un lugar seguro, la necesitarás para descifrar."

# Pregunta al usuario si quiere cifrar o descifrar
echo "¿Qué deseas hacer?"
echo "1) Cifrar archivos"
echo "2) Descifrar archivos"
read -p "Elige una opción (1 o 2): " OPCION

# Función para cifrar archivos
cifrar_archivos() {
    for archivo in "$RUTA"/*; do
        if [ -f "$archivo" ]; then
            echo "Cifrando: $archivo"
            openssl enc -aes-256-cbc -salt -in "$archivo" -out "$archivo.enc" -k "$CLAVE"
            # Opcional: elimina el archivo original (descomenta si lo deseas)
             rm "$archivo"
            echo "Archivo cifrado: $archivo.enc"
        fi
    done
    echo "Cifrado completado."
}

# Función para descifrar archivos
descifrar_archivos() {
    for archivo in "$RUTA"/*.enc; do
        if [ -f "$archivo" ]; then
            # Genera el nombre del archivo descifrado quitando la extensión .enc
            archivo_salida="${archivo%.enc}"
            echo "Descifrando: $archivo"
            openssl enc -aes-256-cbc -d -in "$archivo" -out "$archivo_salida" -k "$CLAVE"
            # Opcional: elimina el archivo cifrado (descomenta si lo deseas)
             rm "$archivo"
            echo "Archivo descifrado: $archivo_salida"
        fi
    done
    echo "Descifrado completado."
}

# Ejecuta la opción elegida
case $OPCION in
    1)
        cifrar_archivos
        ;;
    2)
        # Si elige descifrar, pide la clave manualmente
        read -s -p "Ingresa la clave para descifrar: " CLAVE
        echo
        descifrar_archivos
        ;;
    *)
        echo "Opción no válida. Elige 1 o 2."
        exit 1
        ;;
esac
