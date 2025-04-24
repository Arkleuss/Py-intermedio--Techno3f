#Buscar una palabra en una lista ingresada por teclado usando args y un operador ternario



def busqueda(*frutas, fruta_buscada):
    fruta_existe=0 #contador de coincidencias en la busqueda
    for fruta in frutas:
        if fruta==fruta_buscada:
            fruta_existe+=1  
        else:
            pass
        
        
    print(f"la fruta {fruta_buscada}no existe" if fruta_existe ==0 else f"la fruta {fruta_buscada} existe")
    
    

frutas = input("Escribi las frutas que existen separadas por un espacios: ").split()
fruta_buscada= input("Escribi la fruta a buscar: ").strip()


busqueda(*frutas, fruta_buscada=fruta_buscada)

