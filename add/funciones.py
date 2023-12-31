import pandas as pd
from datetime import datetime

url = "https://www.datos.gov.co/resource/x783-krje.csv"

def importar_data():
    '''
    Importa la información de una URL https://www.datos.gov.co/resource/x783-krje.csv
    '''
    
    return pd.read_csv(url)

def filtrar_a_10(data, lista):
    '''
    Corta a 10 caracteres cada uno de los strings de varios atributos (columnas)
    puestos en una 'lista' que se ingresa como parametro de un dataframe.
    '''
    for item in lista:
        data[item] = data[item].str[:10]
    
    return data
        
def dar_formato_a_info(data, lista):
    '''
    Cambia caracteres para dar formato
        cambia "-" por "/"
        cambia "-" por "/" 
        cambia "." por "/" 
        
    '''
    info = filtrar_a_10(data, lista)
    info[lista[0]] = info[lista[0]].str.replace("-","/")  
    info[lista[1]] = info[lista[1]].str.replace("-","/")  
    info[lista[1]] = info[lista[1]].str.replace(".","/")  
    
    return info

def convertir_a_fecha(valor):
    
    if  len(valor)==10 and valor[:5] == "2022/":
        
        return datetime.strptime(valor, '%Y/%m/%d').date() 
        
    elif len(valor)==10 and valor[-5:] == "/2022":
        
        return datetime.strptime(valor, '%d/%m/%Y').date()  
        
    elif len(valor)<=8 and valor[-3:] == "/21":
        
        return datetime.strptime(valor, '%m/%d/%y').date()  
    
    elif len(valor)<=8 and valor[-3:] == "/22":
        
        return datetime.strptime(valor, '%m/%d/%y').date()  
        
    elif len(valor)<=8 and valor[-3:] == "/20":
        
        return datetime.strptime(valor, '%m/%d/%y').date()  
    
    else:
        return "no aplica"