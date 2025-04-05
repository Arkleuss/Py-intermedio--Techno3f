'''
Escribe un programa que intente dividir dos números. Si el segundo número es cero,
captura la excepción ZeroDivisionError. Si el primer número es un número no válido,
captura la excepción ValueError. En cualquier caso, muestra un mensaje de error al usuario.
'''


valor1=input("ingrese el dividendo: ")
valor2=input("ingrese el divisor: ")

try:
    resultado =int(valor1) / int(valor2)
except ValueError:
    print("Ambos valores deben ser numericos.")
except ZeroDivisionError:
    print("No se puede dividir por 0.")    
else:
    print(resultado)
finally:
    print("Fin")
    