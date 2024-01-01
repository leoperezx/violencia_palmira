#
import add.funciones as fn


if __name__ == '__main__':
    # Importar información desde la pagina www.datos.gov.co
    data = fn.importar_data()
    
    # Selecciona los atributos que contienen información con fechas 
    atributos_con_fecha = ["fecha_de_apertura","fecha_ocurrencia_hechos"]
    
    # Realiza una corte de cada una de las entradas en los atributos 
    # de interés para iniciar a dar formato.
    df = fn.dar_formato_a_info(data, atributos_con_fecha)
        
    #convierte cada entrada en las columnas de string a obejtos fecha
    for item in atributos_con_fecha:
        df[item]=df[item].apply(lambda x: fn.convertir_a_fecha(x))
    
    df.to_csv("dataFrame.csv",index=False)
        
    print("\nInformación del dataframe.......")
    print("\ndimension del datafreme es: {}".format(df.shape))
    # print("\nValores del datafreme: {}".format(df.info()))
