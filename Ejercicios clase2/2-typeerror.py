'''
Escribe un programa que intente sumar un número y una cadena. Si se produce un error
de tipo, captura la excepción TypeError y muestra un mensaje de error al usuario.

'''



valor1= 2
valor2= "3"
try:
    resultado= valor1 + valor2
except TypeError:
    print("Ambos valores deben ser numericos. ")
else:
    print(resultado)
finally:
    print("Fin.")
    