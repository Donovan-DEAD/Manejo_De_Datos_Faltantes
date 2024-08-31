import pandas
import statsmodels.formula.api
from Modulos_Apoyo.ConocerDatosFaltantes import ConocerDatosFaltantes, ComprobarDatosFaltantes
from Modulos_Apoyo.CorrelacionDatosFaltantes import CorrelacionDatosFaltantes
from Modulos_Apoyo.SimularFaltantes import *
import numpy

import matplotlib.pyplot as plt
import seaborn

#Un ejemplo de lo que las funciones son capaces de hacer

DataRaw = pandas.read_csv("Datasets/Datasets_incompletes/Prosperity_Index_Incomplete.csv")

CorrelacionDataset = ConocerDatosFaltantes(DataRaw)

CorrelacionDataset.InformacionGeneral()
