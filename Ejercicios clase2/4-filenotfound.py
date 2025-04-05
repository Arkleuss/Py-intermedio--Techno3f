'''
Escribe un programa que intente abrir un archivo que no existe. si se produce una excepcion FileNotFoundError, 
captura la excepcion y muestra un mensaje de error al usuario. Sin embargo, tambien intenta crear el archivo si no existe.
'''

try:
    with open("archivo.txt", "r") as archivo:
        contenido = archivo.read()
        print(contenido)
except FileNotFoundError:
    print("El archivo 'archivo.txt' no existe.")
    try:
        with open("archivo.txt", "w") as archivo:
            archivo.write("HOLA MUNDO")
            print("Archivo creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el archivo: {e}")
else:
    pass
finally:
    pass