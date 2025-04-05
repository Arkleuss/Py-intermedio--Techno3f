'''
Escribe un programa que intente dividir dos números. Si el segundo número es cero,
captura la excepción ZeroDivisionError y muestra un mensaje de error al usuario
'''




valor1= int(input("ingrese dividendo:"))
valor2= int(input("ingrese divisor: "))
try:
    resultado= valor1/valor2
except ZeroDivisionError:
    print("no se puede dividir por 0")
else:
    print(resultado)
finally:
    print("Fin")