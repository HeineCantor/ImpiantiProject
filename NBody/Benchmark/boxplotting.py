import matplotlib.pyplot as plt
import pandas as pd

PATH = "./valori_confronto.csv"

dataFrame = pd.read_csv(PATH,decimal=',')

dataFrame = dataFrame[["Laptop 10000", "Desktop 10000"]]

# laptop = [float(x.replace(',', '.')) for x in dataFrame["Laptop 10000"].to_list()]
# desktop = [float(x.replace(',', '.')) for x in dataFrame["Desktop 10000"].to_list()]

dataFrame.boxplot(return_type='axes')
plt.show()