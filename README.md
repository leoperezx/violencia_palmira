# Analisis de datos de Violencia Intrafamiliar en el Municipio de Palmira

Para el siguiente caso se realiza la importación de los datos desde el punto de conexión de API:
`https://www.datos.gov.co/resource/x783-krje.csv`

## Comandos útiles y que siempre debo recordar

_Activar entorno virtual en Python_
` $ source .env/bin/activate`

_Desactivar entorno virtual en python_
` $ deactivate`

_verificar rama en git
` $ git branch`


## Explorando los datos

El siguiente ejercicio es una practica para el dominio en la acción de limpiesa y manipulación de datos mediante el uso de _Python_ y su librería _Pandas_ para lo cual inicialmente imprimo los atributos (nombre de las columnas) del DataFrame.

```text
 #   Column                          Non-Null Count  Dtype 
---  ------                          --------------  ----- 
 0   fecha_de_apertura               1000 non-null   object
 1   dia_de_apertura                 1000 non-null   object
 2   fecha_ocurrencia_hechos         1000 non-null   object
 3   dia_ocurrencia                  1000 non-null   object
 4   hora_militar_ocurrencia_hechos  1000 non-null   object
 5   conforman_unidad_domestica      1000 non-null   object
 6   fisica                          1000 non-null   object
 7   verbal                          1000 non-null   object
 8   economica                       1000 non-null   object
 9   psicologica                     1000 non-null   object
 10  sexual                          1000 non-null   object
 11  genero_m_f_victima              1000 non-null   object
 12  edad_victima                    999 non-null    object
 13  victima_conflicto_armado        1000 non-null   object
 14  etnia_victima                   1000 non-null   object
 15  estado_civil_victima            1000 non-null   object
 16  escolaridad_victima             1000 non-null   object
 17  corregimiento_victima           998 non-null    object
 18  comuna_de_la_victima            1000 non-null   object
 19  barrio_victima                  1000 non-null   object
 20  ocupacion_victima               1000 non-null   object
 21  no_hijos_victima                1000 non-null   object
 22  vivienda_victima                1000 non-null   object
 23  nucleo_familiar_victima         1000 non-null   object
 24  numero_hermanos_victima         1000 non-null   object
 25  genero_agresor_m_f              1000 non-null   object
 26  parentesco_frente_a_la_victima  1000 non-null   object
 27  no_de_hijos_agresor             1000 non-null   object
 28  edad_agresor                    1000 non-null   object
 29  estado_civil_agresor            1000 non-null   object
 30  escolaridad_agresor             1000 non-null   object
 31  ocupacion_agresor               1000 non-null   object
 32  corregimiento_agresor           1000 non-null   object
 33  comuna_agresor                  1000 non-null   object
 34  barrio                          1000 non-null   object
 35  tipo_vivienda                   1000 non-null   object
dtypes: object(36)
```

Alcanzo a notar que parece muy completa con pocos campos "no nulos". Esto en apariencia me parece bien, sin embargo falta explorar el contenido y ver como es exactamente la información contenida en el dataframe. Para ello imprimo sus primeras 20 filas para iniciar la exploración y ver a que me enfrento.

```text
          fecha_de_apertura dia_de_apertura  fecha_ocurrencia_hechos  ... comuna_agresor              barrio tipo_vivienda
0   2022-06-01T00:00:00.000          jueves               29/12/2021  ...       comuna10                  no      familiar
1   2022-07-01T00:00:00.000         viernes  2022-07-01T00:00:00.000  ...        comuna5           san pedro     alquilada
2   2022-11-01T00:00:00.000          martes  2022-06-01T00:00:00.000  ...        comuna1                  no     alquilada
3                13/01/2022          jueves               13/01/2022  ...        comuna1                  no      familiar
4                19/01/2022       miércoles  2022-12-01T00:00:00.000  ...        comuna4        san cayetano      familiar
5                19/01/2022       miércoles               18/01/2022  ...        comuna3           la emilia     alquilada
6                21/01/2022         viernes  2022-09-01T00:00:00.000  ...        comuna3           la emilia     alquilada
7                21/01/2022         viernes  2022-04-01T00:00:00.000  ...        comuna3        el triángulo      familiar
8                24/01/2022           lunes               19/01/2022  ...        comuna1            zamorano     alquilada
9                25/01/2022          martes               25/01/2022  ...       comuna12                  no      familiar
10               26/01/2022       miércoles               26/01/2022  ...        comuna6        la colombina      familiar
11               27/01/2022          jueves               27/01/2022  ...        comuna6             pradera      familiar
12               26/01/2022       miércoles               25/01/2022  ...        comuna2  alameda palo verde     alquilada
13               28/01/2022         viernes               23/12/2022  ...        comuna5     primero de mayo      familiar
14               29/01/2022          sábado               29/01/2022  ...        comuna1     urb. los mangos      familiar
15               31/01/2022           lunes               31/12/2022  ...        comuna5     siete de agosto     alquilada
16  2022-02-01T00:00:00.000         domingo                no aplica  ...        comuna1           no aplica        propia
17  2022-03-01T00:00:00.000           lunes                no aplica  ...       comuna16           no aplica     no aplica
18  2022-03-01T00:00:00.000           lunes                no aplica  ...        comuna1           carbonera     alquilada
19  2022-03-01T00:00:00.000           lunes                no aplica  ...        comuna6              fatima      familiar
```

Noto que no hay un formato claro en las columnas que tienen fecha. La inforamción contenida en estas columnas tienen diferentes formatos pero vamos a ver mas de cerca estas columnas.

Además de ser diferentes en tamaño de caracteres, existen diferentes formatos donde las fechas están separada por guiones o fecha separada por barra inclinada, fecha y formato de hora, o solo fechas.

Pero, la información indispensable respecto a las fechas, son los **10 primeros caractéres** en ambas columnas o atributos, por lo que busco la forma de mantener solo esa información para cada una de las columnas que manejan fechas.

Realizo el filtro y escribo el resultado en un dataframe interno llamado info para explorar el resultado.

La información de las fechas contiene diferentes separadores para las fehas por lo que se reemplaza `"-"` y `"."` por `"/"` en toda las fechas. Sin embargo, tenemos formatos mm/dd/aa, dd/mm/aaaa y aaaa/mm/dd para lo cual se construye una función que transforma el _string_ a _objeto fecha_ utilizando la libreira _datetime_ de acuerdo a cada caso.

El antes y después se muestra a continuación:

**Antes:**

```text
   fecha_de_apertura dia_de_apertura fecha_ocurrencia_hechos dia_ocurrencia  ... corregimiento_agresor comuna_agresor              barrio tipo_vivienda
0         2022/06/01          jueves              29/12/2021      miércoles  ...             juanchito       comuna10                  no      familiar
1         2022/07/01         viernes              2022/07/01        viernes  ...               ninguno        comuna5           san pedro     alquilada
2         2022/11/01          martes              2022/06/01      miércoles  ...               ninguno        comuna1                  no     alquilada
3         13/01/2022          jueves              13/01/2022         jueves  ...               ninguno        comuna1                  no      familiar
4         19/01/2022       miércoles              2022/12/01      miércoles  ...               ninguno        comuna4        san cayetano      familiar
5         19/01/2022       miércoles              18/01/2022         martes  ...               ninguno        comuna3           la emilia     alquilada
6         21/01/2022         viernes              2022/09/01        domingo  ...               ninguno        comuna3           la emilia     alquilada
7         21/01/2022         viernes              2022/04/01         martes  ...               ninguno        comuna3        el triángulo      familiar
8         24/01/2022           lunes              19/01/2022      miércoles  ...               ninguno        comuna1            zamorano     alquilada
9         25/01/2022          martes              25/01/2022         martes  ...                boyaca       comuna12                  no      familiar
10        26/01/2022       miércoles              26/01/2022      miércoles  ...               ninguno        comuna6        la colombina      familiar
11        27/01/2022          jueves              27/01/2022         jueves  ...               ninguno        comuna6             pradera      familiar
12        26/01/2022       miércoles              25/01/2022         martes  ...               ninguno        comuna2  alameda palo verde     alquilada
13        28/01/2022         viernes              23/12/2022        viernes  ...               ninguno        comuna5     primero de mayo      familiar
14        29/01/2022          sábado              29/01/2022         sábado  ...               ninguno        comuna1     urb. los mangos      familiar
15        31/01/2022           lunes              31/12/2022         sábado  ...               ninguno        comuna5     siete de agosto     alquilada
16        2022/02/01         domingo               no aplica      no aplica  ...               ninguno        comuna1           no aplica        propia
17        2022/03/01           lunes               no aplica      no aplica  ...                 tenjo       comuna16           no aplica     no aplica
18        2022/03/01           lunes               no aplica      no aplica  ...               ninguno        comuna1           carbonera     alquilada
19        2022/03/01           lunes               no aplica      no aplica  ...               ninguno        comuna6              fatima      familiar
```

**Después:**

```text
   fecha_de_apertura dia_de_apertura fecha_ocurrencia_hechos dia_ocurrencia  ... corregimiento_agresor comuna_agresor              barrio tipo_vivienda
0         2022-06-01          jueves               no aplica      miércoles  ...             juanchito       comuna10                  no      familiar
1         2022-07-01         viernes              2022-07-01        viernes  ...               ninguno        comuna5           san pedro     alquilada
2         2022-11-01          martes              2022-06-01      miércoles  ...               ninguno        comuna1                  no     alquilada
3         2022-01-13          jueves              2022-01-13         jueves  ...               ninguno        comuna1                  no      familiar
4         2022-01-19       miércoles              2022-12-01      miércoles  ...               ninguno        comuna4        san cayetano      familiar
5         2022-01-19       miércoles              2022-01-18         martes  ...               ninguno        comuna3           la emilia     alquilada
6         2022-01-21         viernes              2022-09-01        domingo  ...               ninguno        comuna3           la emilia     alquilada
7         2022-01-21         viernes              2022-04-01         martes  ...               ninguno        comuna3        el triángulo      familiar
8         2022-01-24           lunes              2022-01-19      miércoles  ...               ninguno        comuna1            zamorano     alquilada
9         2022-01-25          martes              2022-01-25         martes  ...                boyaca       comuna12                  no      familiar
10        2022-01-26       miércoles              2022-01-26      miércoles  ...               ninguno        comuna6        la colombina      familiar
11        2022-01-27          jueves              2022-01-27         jueves  ...               ninguno        comuna6             pradera      familiar
12        2022-01-26       miércoles              2022-01-25         martes  ...               ninguno        comuna2  alameda palo verde     alquilada
13        2022-01-28         viernes              2022-12-23        viernes  ...               ninguno        comuna5     primero de mayo      familiar
14        2022-01-29          sábado              2022-01-29         sábado  ...               ninguno        comuna1     urb. los mangos      familiar
15        2022-01-31           lunes              2022-12-31         sábado  ...               ninguno        comuna5     siete de agosto     alquilada
16        2022-02-01         domingo               no aplica      no aplica  ...               ninguno        comuna1           no aplica        propia
17        2022-03-01           lunes               no aplica      no aplica  ...                 tenjo       comuna16           no aplica     no aplica
18        2022-03-01           lunes               no aplica      no aplica  ...               ninguno        comuna1           carbonera     alquilada
19        2022-03-01           lunes               no aplica      no aplica  ...               ninguno        comuna6              fatima      familiar
```

Hay que notar que toda las fechas están separadas por guiones `"-"` y que solo contienen fechas. No contienen formato de horas. Se conservan las etiquetas _"no aplica"_ para cada entrada.

Con esta configuración doy por terminada la preaparación de los datos de fecha incluidos en los atributos **"fecha_de_apertura"** y  **"fecha_ocurrencia_hechos"**.

Con esta operación inicial pretendo _limpiar_ la base de datos.

---

> &copy; 2023 | [leoperezx](https://linkr.bio/2op3pq)