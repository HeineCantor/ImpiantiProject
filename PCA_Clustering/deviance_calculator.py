import pandas as pd
import numpy as np

DATA_PATH = "~/Desktop/git/ImpiantiProject/PCA_Clustering/Data/"
PCA_CLUSTERING_DATA = "dati_Grezzi.csv"
CLUSTERING_CENTROIDS = "medie.csv"

LOSS_PCA = 0.84

pcaClusteringDataFrame = pd.read_csv(DATA_PATH + PCA_CLUSTERING_DATA, decimal=',')
clusteringCentroidsDataFrame = pd.read_csv(DATA_PATH + CLUSTERING_CENTROIDS, decimal=',')

clusterNumber = pcaClusteringDataFrame["Cluster"].max()
numberOfElementsInCluster = {}
clusterArrays = {}
clusterMeans = {}
overallAverage = 0

for clusterId in range(1, clusterNumber + 1):
    subDataFrame = pcaClusteringDataFrame[pcaClusteringDataFrame["Cluster"] == clusterId]
    numberOfElementsInCluster[clusterId] = subDataFrame["Cluster"].count()
    components = [col for col in subDataFrame if col.startswith('Principale')]
    clusterArrays[clusterId] = []
    vectorDataFrame = pcaClusteringDataFrame[components].transpose()
    for i in vectorDataFrame.columns:
        clusterArrays[clusterId].append(np.array(vectorDataFrame[i], dtype="float"))

centroidsDataFrame = clusteringCentroidsDataFrame[components].transpose()
for i in centroidsDataFrame.columns:
    clusterMeans[i+1] = (np.array(centroidsDataFrame[i], dtype="float"))

intraClusterDeviance = 0
interClusterDeviance = 0

for i in range(clusterNumber):
    for j in range(numberOfElementsInCluster[i+1]):
        intraClusterDeviance += np.linalg.norm(clusterArrays[i+1][j] - clusterMeans[i+1])

for i in range(clusterNumber):
    interClusterDeviance += numberOfElementsInCluster[i+1] * np.linalg.norm(clusterMeans[i+1])**2

#print(intraClusterDeviance)
#print(interClusterDeviance)

intraClusterVariance = intraClusterDeviance / (intraClusterDeviance + interClusterDeviance)
interClusterVariance = interClusterDeviance / (intraClusterDeviance + interClusterDeviance)

print(f"Intra-cluster variance: {intraClusterVariance}")
print(f"Inter-cluster variance: {interClusterVariance}")

totalDevianceLoss = (1 - LOSS_PCA) + intraClusterVariance * LOSS_PCA
totalDevianceLoss2 = 1 - interClusterVariance * LOSS_PCA

print(f"Total Deviance Loss (1): {totalDevianceLoss}")
print(f"Total Deviance Loss (2): {totalDevianceLoss2}")

#print(numberOfElementsInCluster)

#print(pcaClusteringDataFrame[pcaClusteringDataFrame["Cluster"] == 1])
