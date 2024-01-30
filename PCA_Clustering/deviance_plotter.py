import pandas as pd
import matplotlib.pyplot as plt

devianceDataframe = pd.read_csv("./devianceLosses.csv")

X_AXIS = [15, 10, 5, 3]

lines = []

for index, row in devianceDataframe.iterrows():
    lines.append(row.tolist())

for line in lines:
    plt.plot(X_AXIS, line[1:], label=f"{int(line[0])} PCA")

plt.title("Deviance loss PCA + Clustering")

plt.xlabel("# Cluster")
plt.ylabel("Deviance loss")

plt.xticks(X_AXIS)
plt.legend()
plt.gca().invert_xaxis()
plt.grid()
plt.show()