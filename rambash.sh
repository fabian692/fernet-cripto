#!/bin/bash

# Ruta del directorio a recorrer (cámbialo según tus necesidades)
RUTA="/home/parrot/Documentos"

# Archivo donde se guardará la clave (cifrado)
ARCHIVO_CLAVE="$HOME/clave.txt.enc"

# Función para obtener la clave maestra del usuario
obtener_clave_maestra() {
    read -s -p "Ingresa la contraseña maestra: " CLAVE_MAESTRA
    echo
}

# Genera o lee la clave AES-256
if [ ! -f "$ARCHIVO_CLAVE" ]; then
    # Genera una clave AES-256 aleatoria
    CLAVE=$(openssl rand -base64 32)
    echo "Clave generada: $CLAVE"
    echo "Guardando la clave en $ARCHIVO_CLAVE (cifrada con contraseña maestra)"
    
    # Pide la clave maestra para cifrar el archivo de la clave
    obtener_clave_maestra
    echo "$CLAVE" | openssl enc -aes-256-cbc -salt -out "$ARCHIVO_CLAVE" -k "$CLAVE_MAESTRA"
    
    # Restringe permisos del archivo cifrado
    chmod 600 "$ARCHIVO_CLAVE"
else
    # Si el archivo existe, pide la clave maestra para descifrarlo
    obtener_clave_maestra
    CLAVE=$(openssl enc -aes-256-cbc -d -in "$ARCHIVO_CLAVE" -k "$CLAVE_MAESTRA" 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "Error: Contraseña maestra incorrecta o archivo de clave corrupto."
        exit 1
    fi
    echo "Clave cargada desde $ARCHIVO_CLAVE"
fi

# Pregunta al usuario si quiere cifrar o descifrar
echo "¿Qué deseas hacer?"
echo "1) Cifrar archivos"
echo "2) Descifrar archivos"
read -p "Elige una opción (1 o 2): " OPCION

# Función para cifrar archivos
cifrar_archivos() {
    for archivo in "$RUTA"/*; do
        if [ -f "$archivo" ] && [[ "$archivo" != *.enc ]]; then
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
        if [ -f "$ARCHIVO_CLAVE" ]; then
            descifrar_archivos
        else
            echo "No se encontró el archivo de clave ($ARCHIVO_CLAVE). No puedo descifrar."
            exit 1
        fi
        ;;
    *)
        echo "Opción no válida. Elige 1 o 2."
        exit 1
        ;;
esac
