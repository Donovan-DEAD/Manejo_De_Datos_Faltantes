import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt

seaborn.set_style("darkgrid")
seaborn.set_palette("viridis")
seaborn.set_context("paper",font_scale=1.2)


class CorrelacionDatosFaltantes:
    
    def __init__(self, dataFrame: pandas.DataFrame) -> None:
        self.dataFrame = dataFrame
        shadowMask = self.dataFrame.notnull().add_suffix("_Shadow")

        Data = {}

        for Columnas in shadowMask.columns:
            if False in list(shadowMask[Columnas]):
                self.dataFrame[Columnas] = shadowMask[Columnas]

    def __ReemplazarNaN (self,Element):
        global Value
        if pandas.isna(Element) == True:
            return Value
        else:
            return Element

    def __ReplaceNanForScatterPlot (self,column: str = "", proportion_below_minimun: float = 0.10)->pandas.Series:
        global Value
        Value = self.dataFrame[column].min()-self.dataFrame[column].min()*proportion_below_minimun
        return self.dataFrame[column].map(self.__ReemplazarNaN)

    def BoxenPlot(self, missing_data_column: str = "", complete_data_column: str = ""):
        try:
            Grafica  = seaborn.boxenplot(self.dataFrame, y=complete_data_column, x=missing_data_column+"_Shadow")
        except:
            return print(f"El nombre de alguna de las columnas es incorrecto. Estas son algunas de las columnas: \n {self.dataFrame.columns}")
        plt.show()

    def ScatterPlot (self, first_data_column: str = "", second_data_column: str = ""):
        try:
            Graphic = seaborn.scatterplot(x=self.__ReplaceNanForScatterPlot(column=first_data_column), y= self.__ReplaceNanForScatterPlot(column=second_data_column))
            Graphic2 = seaborn.rugplot(x=self.__ReplaceNanForScatterPlot(column=first_data_column), y= self.__ReplaceNanForScatterPlot(column=second_data_column))
        except:
            return print("El nombre de alguna de las columnas es incorrecto.")
        
        plt.show()

    def NullityCorrelation(self):
        ListColumns = []
        DataCount = self.dataFrame.count()

        for column in DataCount.index :

            if DataCount[column] != self.dataFrame.shape[0]:

                ListColumns.append(column)

        Data_Frame = self.dataFrame[ListColumns].notnull()

        ListIndexs=[]

        for index in list(Data_Frame.index):

            if False in list(Data_Frame.loc[index]):

                ListIndexs.append(index)

        Data_Frame = Data_Frame.loc[ListIndexs].corr()

        grafica = seaborn.heatmap(Data_Frame, cmap="viridis", annot=True)
        plt.show()