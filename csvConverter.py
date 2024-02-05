import pandas as pd

toConvert = pd.read_csv("./outputfile.csv", delim_whitespace=True)

toConvert.to_csv("./nonconverted.csv")
