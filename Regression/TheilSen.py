from scipy.stats import theilslopes
import pandas as pd

FILE_PATH = "/home/heinecantor/Dropbox/UNI/Impianti/Esercitazioni/HomeWork_Regression.xls"

regressionDf = pd.read_excel(FILE_PATH, sheet_name="EXP2")

x = regressionDf["observation"].to_list()
y = regressionDf["nmail"].to_list()

slope, intercept, low_slope, high_slope = theilslopes(y, x)

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"Low slope: {low_slope}")
print(f"High slope: {high_slope}")