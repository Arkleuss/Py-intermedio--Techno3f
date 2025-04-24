#Calcular el mayor de dos números ingresados por teclado usando un operador ternario


num1= int(input("ingrese primer valor: "))
num2= int(input("ingrese segundo valor: "))
#*****************************evalua si son iguales*************************************evalua el mas alto**********
print("los numeros son iguales" if num1==num2 else  f"el numero mas alto es {num1}"     if num1>num2 else     f"el numero mas alto es {num2}") 