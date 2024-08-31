import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt
import os

seaborn.set_style("darkgrid")
seaborn.set_palette("viridis")
seaborn.set_context("paper",font_scale=1.2)

def ReemplazarNaN (Elemento):
    if pandas.isna(Elemento) == True:
        return 0
    else:
        return Elemento

def ComprobarDatosFaltantes(dir: str):
    try:
        Directories = os.listdir(dir)
    except:
        return print("El directorio no existe.")
    
    try:
        for Directory in Directories:

            if Directory.endswith(".csv"):
                DataFrame = pandas.read_csv(f"{dir}\{Directory}", low_memory=False)

                Data = {}

                for Columnas in DataFrame.columns:
                    Col = DataFrame[Columnas].isna().value_counts()
                    Data.update({Columnas : Col})
                    
                frameValoresFaltantes = pandas.DataFrame(Data)
                
                DataTratada = frameValoresFaltantes.map(ReemplazarNaN).transpose().rename(columns={False: "Datos",True:"Faltantes"})
                try:
                    DataTratada["Faltantes"]
                    print(f"El archivo {Directory} POSEE datos faltantes. El cual se encuentra en la ruta relativa:\n {dir}\{Directory} \n \n")
                except:
                    print(f"El archivo {Directory} no posee datos faltantes. El cual se encuentra en la ruta relativa:\n {dir}\{Directory} \n \n")
    except:
        return print("El directorio se encuentra vacio.")

class ConocerDatosFaltantes:

    def __init__(self, dataFrame) -> None:
        
        self.dataFrame = dataFrame
        self.sizeDataFrame = self.dataFrame.shape[0] * self.dataFrame.shape[1]

        Data = {}

        for Columnas in self.dataFrame.columns:

            Col = self.dataFrame[Columnas].isna().value_counts()
            Data.update({Columnas : Col})
        
        frameValoresFaltantes = pandas.DataFrame(Data)
        
        self.DataTratada = frameValoresFaltantes.map(ReemplazarNaN).transpose().rename(columns={False: "Datos",True:"Faltantes"})
        self.DataTratada["Porcentaje_Faltante"] = self.DataTratada["Faltantes"]/self.DataTratada.agg("sum",axis="columns")*100
        self.DataTratada["Porcentaje_Presente"] = self.DataTratada["Datos"]/self.DataTratada.agg("sum",axis="columns")*100
        
        Data.clear()

        dataFrameTranspose = self.dataFrame.transpose()
        
        for Columnas in dataFrameTranspose.columns:
            Col = dataFrameTranspose[Columnas].isna().value_counts()
            Data.update({Columnas : Col})

        frameValoresFaltantes =pandas.DataFrame(Data)

        self.DataTratadaFilas = frameValoresFaltantes.map(ReemplazarNaN).transpose().rename(columns={True:"Faltantes", False: "Datos"})
        self.DataTratadaFilas["Porcentaje_Faltante"] = self.DataTratadaFilas["Faltantes"]/self.DataTratadaFilas.agg("sum",axis="columns")*100
        self.DataTratadaFilas["Porcentaje_Presente"] = self.DataTratadaFilas["Datos"]/self.DataTratadaFilas.agg("sum",axis="columns")*100

    def GraficaInfoPorColumna (self, dato: str = "Faltantes"):
        Grafica = seaborn.barplot(data=self.DataTratada, y=dato, x=self.DataTratada.index)
        plt.show()
    
    def GraficaFaltantesPorFilas (self, ancho: int = 1):
        Grafica = seaborn.histplot(data=self.DataTratadaFilas, y="Faltantes", binwidth= ancho)
        plt.show()

    def TablaValoresFaltantes (self):
        print(self.DataTratada)

    def InformacionGeneral (self):
        self.TablaDatosTotal = self.DataTratada.sum(axis="index")
        self.faltantesTotal = self.TablaDatosTotal["Faltantes"]
        self.datosTotal = self.TablaDatosTotal["Datos"]

        self.TablaDatosTotal["Porcentaje_Faltante"] = self.faltantesTotal/self.sizeDataFrame*100
        self.TablaDatosTotal["Porcentaje_Presente"] = self.datosTotal/self.sizeDataFrame*100

        self.porcentajeFaltantesTotal = self.TablaDatosTotal["Porcentaje_Faltante"]
        self.porcentajeDatosTotal = self.TablaDatosTotal["Porcentaje_Presente"]

        print("------------------------------------------")
        print("Size of data frame: \n", self.sizeDataFrame)
        print("------------------------------------------")
        print("Datos y faltantes totales:\n ")
        print(self.TablaDatosTotal)
        print("------------------------------------------")
        print("Datos totales: \n", self.datosTotal)
        print("------------------------------------------")
        print("Faltantes totales: \n", self.faltantesTotal)
        print("------------------------------------------")
        print("Porcentaje de Datos:\n ", self.porcentajeDatosTotal)
        print("------------------------------------------")
        print("Porcentaje de Faltantes: ", self.porcentajeFaltantesTotal)
        print("------------------------------------------")
        print("Total por columna: \n", self.DataTratada)
        print("------------------------------------------")
    
    def ErroresPorSubgrupo (self, columna: str = "" , division:int = 50):

        columnaAnalizar = self.dataFrame[columna].to_numpy()
        Grupos = numpy.array_split(columnaAnalizar, ( (columnaAnalizar.size - columnaAnalizar.size % division) / division ))

        Data = {}
        for Indice, Elemento in enumerate(Grupos):
            Elemento = pandas.Series(Elemento).isna().value_counts()
            Data.update({Indice: Elemento})

        FrameErroresGrupo = pandas.DataFrame(Data).map(ReemplazarNaN).transpose().rename(columns={True:"Faltantes", False: "Datos"}).transpose()

        print("------------------------------------------")
        print(FrameErroresGrupo)
        print("------------------------------------------")
    
    def EspacioEntreErrores (self, columna: str = ""):
        CuentaEspacio = 0
        Data = {}
        ColumnaAnalizar = self.dataFrame[columna].isna().to_numpy()

        for count, x in enumerate(numpy.nditer(ColumnaAnalizar)):
            if x == True:
                Data.update({f"{len(Data)}.Faltante": [1] })
                CuentaEspacio = 0
            else:
                CuentaEspacio += 1
                if count == len(ColumnaAnalizar)-1:
                    Data.update({f"{len(Data)+1}.Datos":[CuentaEspacio]})
                elif ColumnaAnalizar[count] == True:
                    Data.update({f"{len(Data)+1}.Datos":[CuentaEspacio]})

        self.TablaIntervaloErrores = pandas.DataFrame(data=Data).transpose().rename({0:"Distancia"})

        print("--------------------------------------")
        print(self.TablaIntervaloErrores)
        print("--------------------------------------")

    def MatrizDatosFaltantes(self, ordenar: str=""):

        if ordenar != "":
            self.dataFrame.sort_values(ordenar, inplace = True)
        
        colorMatrix = self.dataFrame.notnull().replace({True:0, False:255}).to_numpy()
        colorMatrix = numpy.dstack((colorMatrix,colorMatrix,colorMatrix))
        
        plt.figure(figsize=(23,10))
        gs = plt.GridSpec(1, 1)
        missingValuesPlot = plt.subplot(gs[0])

        missingValuesPlot.imshow(colorMatrix, interpolation='none')

        missingValuesPlot.set_aspect('auto')
        missingValuesPlot.grid(visible=False)
        missingValuesPlot.set_xticks(list(range(0, colorMatrix.shape[1])))
        missingValuesPlot.set_xticklabels(list(self.dataFrame.columns), fontsize=12)

        plt.show()