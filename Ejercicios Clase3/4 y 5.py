#Calcular el promedio de una lista de números usando args y un operador ternario
#Imprimir un mensaje de error si no se pasan suficientes argumentos



def promedio(*args):
    #contador=len(args)
    contador=0
    suma=0
    for arg in args:
            suma+=int(arg)
            contador+=1
    print(f"{suma/contador}" if contador>0  else print("Se necesita minimo un valor para promediar: ")) #valida que la lista no este vacia
    

numeros= input("ingrese numeros a promediar separados por espacios: ").split()
promedio(*numeros) #cambiar numero de prueba  