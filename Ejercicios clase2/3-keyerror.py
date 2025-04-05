'''
Escribe un programa que intente acceder a una clave que no existe en un
diccionario. Si se produce una excepción KeyError, captura la excepción y muestra
'''


diccionario= {
    "Nombre": "Leandro",
    "Apellido": "Figliolia"
    }
try:
    clave="DNI"
    res= diccionario[clave]
except KeyError:
    print(" No existe valor para la clave ingresada.")
else:
    print(res)
finally:
    print("Fin.")
    