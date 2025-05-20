from datetime import date, datetime
from abc import ABC , abstractmethod


"""
Práctica.. Práctica.. Práctica Se debe modificar la clase CuentaBancaria para que sea abstracta , 
ademas los metodos extraer y depositar deben volverse abstractos, tambien se debecrear una clase 
CuentaAhorro que herede de CuentaBancaria y se le agregue un atributo privado de tasa de interes, 
el cual tendra un valor establecido de 0.001 y un metodo que nos calcule el interes

"""




class CuentaBancaria(ABC):
    def __init__(self,nombre_titular,dni_titular, fecha_nacimiento, saldo=0):
        self._nombre_titular = nombre_titular       #atributo privado
        self._dni_titular = dni_titular             #atributo privado
        self._fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y/%m/%d').date()
        self._saldo = saldo                         #atributo privado

    def obtener_saldo(self):
        return self._saldo
    
    def _caclular_edad(self):
        fecha_actual = date.today()
        edad = fecha_actual - self._fecha_nacimiento
        return edad.days // 365
    
    def obtener_edad(self):
        return self._caclular_edad()
    
    """
    def depositar(self,monto):
        if monto > 0:
            self._saldo += monto
            print(f"Se ha depositado {monto} a la cuenta de {self._nombre_titular}, su saldo es de: {self.obtener_saldo()}")
        else:
            print("El monto a depositar debeser mayor a 0")
            
    def extraer(self,monto):
        if monto <= self.obtener_saldo():
            self._saldo -= monto
            print(f"Se ha extraido {monto} de la cuenta de {self._nombre_titular}, su saldo acutal es de: {self.obtener_saldo()}")
        else:
            print("No posee saldo suficiente para esta operación")
    """
    @classmethod
    @abstractmethod
    def depositar(self, monto):
        pass
    
    @classmethod
    @abstractmethod
    def extraer(self,monto):
        pass