#
import add.funciones as fn


if __name__ == '__main__':
    #importar información desde la pagina www.datos.gov.co
    data = fn.importar_data()
    atributos_con_fecha = ["fecha_de_apertura","fecha_ocurrencia_hechos"]
    
    df = fn.dar_formato_a_info(data, atributos_con_fecha)
    
    #df = fn.convertir_a_objeto_fecha(df,atributos_con_fecha[0])
    for item in atributos_con_fecha:
        df[item]=df[item].apply(lambda x: fn.convertir_a_fecha(x))
    
    df.to_csv("dataFrame.csv",index=False)
        
    print("\nInformación del dataframe.......")
    print("\ndimension del datafreme es: {}".format(df.shape))
    # print("\nValores del datafreme: {}".format(df.info()))
