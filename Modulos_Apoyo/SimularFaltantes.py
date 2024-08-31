import pandas
import numpy

# Datasets\Datastes_incompletes

def createIncompleteDataset(Dataset: str = "", name_to_save: str = "", percentage_data_preserved: float = 1):
    if Dataset != "":
        try:
            DataFrame = pandas.read_csv(f"Datasets\{Dataset}.csv")
            DataSize = DataFrame.shape[0]*DataFrame.shape[1]
            Mask = numpy.random.choice(numpy.linspace(start=1, stop=DataSize,num=DataSize), size=(DataFrame.shape[0],DataFrame.shape[1]),replace=False)

            DataFrame[Mask>(DataSize*percentage_data_preserved)] = numpy.nan
            DataFrame.to_csv(f"Datasets\Datasets_incompletes\{name_to_save}.csv")
        except:
            return print("El nombre del dataset no es correcto o la ruta donde se iba a guardar fue eliminada.")

        return print(f"Terminado. El archivo se ha guardado en la ruta: \n Datasets\Datasets_incompletes\{name_to_save}.csv",)
    
    return print("No se proporciono un Dataset.")