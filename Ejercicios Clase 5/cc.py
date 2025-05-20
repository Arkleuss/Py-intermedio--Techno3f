from cb import CuentaBancaria

class CuentaCorriente(CuentaBancaria):
    def __init__(self, nombre_titular, dni_titular, fecha_nacimiento, saldo=0,limite_extraccion = 500):
        super().__init__(nombre_titular, dni_titular, fecha_nacimiento, saldo)
        self._limite_extraccion = limite_extraccion
    
    def extraer(self, monto):
        if monto <= self.obtener_saldo() and monto <= self._limite_extraccion:
            self._saldo -= monto
            print(f"Se ha extraido {monto} de la cuenta de {self._nombre_titular}, su saldo acutal es de: {self.obtener_saldo()}")
        else:
            if monto > self._limite_extraccion:
                print("Usted no puede extraer ese monto")
            else:
                print("Usted no posee saldo suficiente para realizar la operación")
    def depositar(self,monto):
        if monto > 0:
            self._saldo += monto
            print(f"Se ha depositado {monto} a la cuenta de {self._nombre_titular}, su saldo es de: {self.obtener_saldo()}")
        else:
            print("El monto a depositar debeser mayor a 0")



class CuentaAhorro(CuentaBancaria):
    def __init__(self, nombre_titular, dni_titular, fecha_nacimiento, saldo=0, tasa_interes= 0.001):
        super().__init__(nombre_titular, dni_titular, fecha_nacimiento, saldo)
        self._tasa_interes =tasa_interes
    
    def _interes(self):
        #saldo=CuentaAhorro.obtener_saldo()
        int= (float(self._saldo) * float(self._tasa_interes))
        self._saldo += int
        print(f"Se ha impactado la tasa de interes. Su nuevo saldo es: {self._saldo}")
        
        
    def depositar(self,monto):
        if monto > 0:
            self._saldo += monto
            print(f"Se ha depositado {monto} a la cuenta de {self._nombre_titular}, su saldo es de: {self.obtener_saldo()}")
            self._interes()
        else:
            print("El monto a depositar debeser mayor a 0")
    
    def extraer(self,monto):
        if monto <= self.obtener_saldo():
            self._saldo -= monto
            print(f"Se ha extraido {monto} de la cuenta de {self._nombre_titular}, su saldo acutal es de: {self.obtener_saldo()}")
            self._interes()
        else:
            print("No posee saldo suficiente para esta operación")
            
    