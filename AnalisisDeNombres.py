#Nota: Espero que la documentacion no este demasiado improlija, no suelo hacerlo mucho aun debo hacerla un habito jajaja


#Librerias necesarias para el trabajo:
import glob
import numpy as np #No llegue a utilizar numpy
import pandas as pd
import matplotlib.pyplot as plt
import re #Lo nececito para .str.contains(), es un modulo empleado por pandas para metodos str con patrones complejos


"""Esta función se encarga de encontrar todos los archivos CSV y unirlos en un solo Dataframe"""

def dataframeNom():
    
    #Defino la ruta y el patron para encontrar todos los archivos CSV que empiezan con "nombres-"
    rutaArchivo = "PYTHON/Materia Python Avanzado/Proyecto matplotlib/Data/nombres-*.csv"
    
    listaRutas = glob.glob(rutaArchivo) #Glob devuevle una lista con todas las rutas  
    listaDataframes = []
    
    for ruta in listaRutas:
        listaDataframes.append(pd.read_csv(ruta))
        
    #Una vez que tengo todos los DataFrames en la lista, los uno en uno solo
    dataframeUnif = pd.concat(listaDataframes, ignore_index=True) 
    
    return dataframeUnif

"""Funcion encargada de limpiar la columna nombre, luego calcula y muestra: El año con mayor cantidad de personas registradas,
el nombre mas popular en todo el rango de años y el nombre más largo.
    """

def analizarDatos(dataframe):
    if dataframe is None:
        return
    
#Filtro el dataframe para quitar cosas raras como anotaciones o simbolos
#Uso una expresión regular que solo acepta letras (incluyendo acentos y ñ) y espacios
    dataframe = dataframe[dataframe['nombre'].str.contains(r'^[a-záéíóúüñ\s]+$', case=False, na=False)].copy() 
#Nota: Me veo obligado a usar .copy() porque pandas me manda un aviso de que el dataframe filtrado es solo una vista, ni sobreescribiendo el original me quita el aviso
#Nota2: Si considere poner el filtrado cuando unifico los csv para hacerlo mas versatil, sin embargo lo dejare aqui como registro del proceso
    
    sumAnioMayorCantPersn =  dataframe.groupby("anio")["cantidad"].sum() #Agrupo por año y sumo la cantidad de personas para ver el total de cada año.
    anioMayorCantPersn = sumAnioMayorCantPersn.idxmax() #extraigo el indice
    sumNombreMasPopular = dataframe.groupby("nombre")["cantidad"].sum()
    nombreMasPopular = sumNombreMasPopular.idxmax()
    
#creo una columna temporal "longitud".
#Le quito los espacios al nombre para que no influyan en el largo real.
    dataframe["longitud"] = dataframe["nombre"].str.replace(" ", "").str.len() #Se usa str porque la columna "nombre" es una serie, no se pueden aplicar metodos del string si no le especificas que lo trate como tal
    indiceLargoNombre = dataframe["longitud"].max()
    dataframemascaraLargoNombre = dataframe[dataframe["longitud"] == indiceLargoNombre] #Meto la mascara booleana dentro del dataframe para que seleccione las filas donde el resultado fue TRUE
    largoNombre = dataframemascaraLargoNombre["nombre"].iloc[0] #Pueden haber varios nombres de misma longitud, por lo que uso iloc[0] para tomar solo el primero
    print(f"\nEL año con mayor cantidad de personas registradas es: {anioMayorCantPersn}")
    print(f"\nEl nombre mas popular en todo el rango de años es: {nombreMasPopular}")
    print(f"\nEl nombre más largo registrado es: {largoNombre}")

    dataframe.drop(columns=["longitud"], inplace=True) #Como ya no se usara la columna longitud para nada en el resto del codigo decidi removerla
    return dataframe


"""Agregar información al dataset considerando lo siguiente:
• Una columna con el número de palabras del nombre;
• Una columna con el porcentaje de registro que ese nombre representa en ese
año."""

def agregarInfoDataframe(dataframe):
    if dataframe is None:
        return
    
    #Creo la columna "cantPalabras", divido el nombre por espacios y cuento los elementos
    dataframe["cantPalabras"] = dataframe["nombre"].str.split().str.len() #Lo mismo que para use para el nombre mas largo pero en lugar de separar por caracteres, separa por palabras
    dataframe["totalAnual"] = dataframe.groupby("anio")["cantidad"].transform("sum") #groupby("anio") y transform("sum") crea una columna con la suma total del año repetida en cada fila de ese año
   
    dataframe["porcentajeAnio"] = (dataframe["cantidad"] / dataframe["totalAnual"]) * 100 #(cantidad del nombre / total del año) * 100
    dataframe["porcentajeAnio"] = "% " + dataframe["porcentajeAnio"].round(2).astype(str)
    
    dataframe.drop(columns=["totalAnual"], inplace=True) #Elimino la columna totalAnual como ya no la necesito
    
    #Prueba: Imprimo las 5 primeras filas para verificar que las nuevas columnas se crearon bien.
    print("-----------------------------------------------------")
    print(dataframe[["nombre", "cantidad", "anio", "cantPalabras", "porcentajeAnio"]].head(5))

    return dataframe


"""Represente de la mejor forma posible la siguiente información:
• Porcentaje de datos que cada año aportó al total de la información;
• Evolución del registro de los nombres 'Maria' y 'Juan' (solamente, sin primeros
ni segundos nombres, y sin tildes). Marcar cuál es el año donde más veces se
registraron;
• El nombre más popular en cada año."""

def generaReporteSimple(dataframe):
    if dataframe is None:
        return
        
    plt.style.use("seaborn-v0_8-deep") #Solo es un estilo para que los gráficos se vean lindos
    
    print("\n\t\t--- Creando graficos ---")
    print("\n Nota: Al menos en VS Code con W11 se genera en un entorno virtual, desconozco como funciona en otros IDEs")
    print("------------------------------------------------------------------------------------------------------")
    
    #Preparo los datos: agrupo por año, sumo las cantidades y lo convierto en un nuevo DataFrame.
    dataframeDistribucion = dataframe.groupby("anio")["cantidad"].sum().reset_index(name="totalAnual")
    totalGlobal = dataframeDistribucion["totalAnual"].sum()
    dataframeDistribucion["porcentaje"] = (dataframeDistribucion["totalAnual"] / totalGlobal) * 100 # Calculo el porcentaje de cada año.

    plt.figure(figsize=(18, 7))
    plt.bar(dataframeDistribucion["anio"].astype(str), dataframeDistribucion["porcentaje"], color="skyblue")
    
    plt.title("Porcentaje de registros aportado por cada año", fontsize=14)
    plt.xlabel("Año")
    plt.ylabel("Porcentaje del total global (%)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
    
    #Normalizo los nombres para la búsqueda: sin acentos, en minúsculas y sin espacios extra.
    dataframe["nombreSimple"] = dataframe["nombre"].str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("utf-8").str.lower().str.strip()
    dataframeFiltro = dataframe[dataframe["nombreSimple"].isin(["maria", "juan"])]
    # Preparo la tabla: agrupo por año y nombre, y uso unstack() para que "juan" y "maria" se vuelvan columnas.
    dataframeEvolucion = dataframeFiltro.groupby(["anio", "nombreSimple"])["cantidad"].sum().unstack(fill_value=0)
    
    plt.figure(figsize=(18, 7))
    
    if "juan" in dataframeEvolucion.columns:
        plt.plot(dataframeEvolucion.index, dataframeEvolucion["juan"], label="Juan", color="blue")
        maxJuanAnio = dataframeEvolucion["juan"].idxmax()
        maxJuanValor = dataframeEvolucion["juan"].max()
        plt.plot(maxJuanAnio, maxJuanValor, "o", color="blue", markersize=10, label=f"Maximo Juan: {maxJuanAnio}")

    if "maria" in dataframeEvolucion.columns:
        plt.plot(dataframeEvolucion.index, dataframeEvolucion["maria"], label="Maria", color="green")
        maxMariaAnio = dataframeEvolucion["maria"].idxmax()
        maxMariaValor = dataframeEvolucion["maria"].max()
        plt.plot(maxMariaAnio, maxMariaValor, "o", color="green", markersize=10, label=f"Maximo Maria: {maxMariaAnio}")

    plt.title("Evolución anual de registros para Juan y María", fontsize=14)
    plt.xlabel("Año")
    plt.ylabel("Cantidad de registros")
    plt.legend() #Muestra las etiquetas de las líneas.
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    
    idx_max_por_anio = dataframe.groupby("anio")["cantidad"].idxmax()  #Agrupo por año y encuentro el índice del valor maximo de "cantidad"
    dataframe_popular_anual = dataframe.loc[idx_max_por_anio, ["anio", "nombre", "cantidad"]].copy()
    
    plt.figure(figsize=(18, 7))
    anios = dataframe_popular_anual["anio"].astype(str)
    cantidades = dataframe_popular_anual["cantidad"]
    
    barras = plt.bar(anios, cantidades, color="salmon")
    plt.title("Nombre mas popular en cada año", fontsize=12)
    plt.xlabel("Año")
    plt.ylabel("Cantidad de registros")
    
    for i, bar in enumerate(barras): # Este bucle es para agregar el nombre encima de cada barra
        nombre = dataframe_popular_anual["nombre"].iloc[i]
        #Pongo el texto un poquito por encima de la barra
        plt.text(bar.get_x() + bar.get_width() / 2., 
                 bar.get_height() + 10, 
                 nombre, 
                 ha="center",
                 rotation=90,
                 fontsize=8, 
                 weight="bold")
            
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    dataframeUnif = dataframeNom() #Unifica los dataframe
    #Como el filtrado esta dentro del analizarDatos sobreescribire el dataframeUnif
    dataframeUnif = analizarDatos(dataframeUnif) 
    dataframeUnif = agregarInfoDataframe(dataframeUnif)
    generaReporteSimple(dataframeUnif)
    
    
    