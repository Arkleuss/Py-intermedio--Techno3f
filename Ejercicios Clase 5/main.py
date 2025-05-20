from cc import CuentaCorriente, CuentaAhorro
# descomentar las pruebas de cuenta corriente o cuenta ahorro y correr

cc1= CuentaCorriente("Gabriel", "11111", "1988/01/01")
ca1=CuentaAhorro("Leandro", "22222", "1988/10/04")


""" 
#PRUEBA CUENTA CORRIENTE 

print(f"Se esta usando la cuenta corriente de {cc1._nombre_titular}")
print(cc1.obtener_saldo())
cc1.extraer(1000) #extraer encima del limite
cc1.extraer(500) #extraer sin saldo suficiente
cc1.depositar(1000)
print(cc1.obtener_saldo())
cc1.extraer(500)

"""

"""
#PRUEBA CUENTA AHORRO

print(f"Se esta usando la cuenta ahorro de {ca1._nombre_titular}")
print(ca1.obtener_saldo())
ca1.extraer(1000) #extraer encima del limite
ca1.depositar(1000)
print(ca1.obtener_saldo())
ca1.extraer(500)

"""