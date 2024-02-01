import pandas as pd
import numpy as np
from tqdm import tqdm

DATA_PATH = "~/Desktop/git/ImpiantiProject/PCA_Clustering/WorkloadClustering/HL/old/"
PCA_CLUSTERING_DATA = "report6cluster.csv"
CLUSTERING_CENTROIDS = "medie6cluster.csv"

LOSS_PCA = 0.9400
#LOSS_PCA = 0.8967
enablePCA = True

pcaClusteringDataFrame = pd.read_csv(DATA_PATH + PCA_CLUSTERING_DATA, decimal=',')
clusteringCentroidsDataFrame = pd.read_csv(DATA_PATH + CLUSTERING_CENTROIDS, decimal=',')

clusterNumber = pcaClusteringDataFrame["Cluster"].max()
numberOfElementsInCluster = {}
clusterArrays = {}
clusterMeans = {}
overallAverage = 0

for clusterId in tqdm(range(1, clusterNumber + 1)):
    subDataFrame = pcaClusteringDataFrame[pcaClusteringDataFrame["Cluster"] == clusterId]
    numberOfElementsInCluster[clusterId] = subDataFrame["Cluster"].count()
    if enablePCA:
        components = [col for col in subDataFrame if col.startswith('Principale')]
    else:
        components = [col for col in subDataFrame]
    clusterArrays[clusterId] = []
    vectorDataFrame = pcaClusteringDataFrame[components].transpose()
    for i in vectorDataFrame.columns:
        clusterArrays[clusterId].append(np.array(vectorDataFrame[i], dtype="float"))

centroidsDataFrame = clusteringCentroidsDataFrame[components].transpose()
for i in tqdm(centroidsDataFrame.columns):
    clusterMeans[i+1] = (np.array(centroidsDataFrame[i], dtype="float"))

intraClusterDeviance = 0
interClusterDeviance = 0

for i in tqdm(range(clusterNumber)):
    for j in range(numberOfElementsInCluster[i+1]):
        intraClusterDeviance += np.linalg.norm(clusterArrays[i+1][j] - clusterMeans[i+1])

for i in tqdm(range(clusterNumber)):
    interClusterDeviance += numberOfElementsInCluster[i+1] * np.linalg.norm(clusterMeans[i+1])**2

intraClusterVariance = intraClusterDeviance / (intraClusterDeviance + interClusterDeviance)
interClusterVariance = interClusterDeviance / (intraClusterDeviance + interClusterDeviance)

print(f"Intra-cluster variance: {intraClusterVariance}")
print(f"Inter-cluster variance: {interClusterVariance}")

totalDevianceLoss = (1 - LOSS_PCA) + intraClusterVariance * LOSS_PCA

print(f"Total Deviance Loss: {totalDevianceLoss}")

#print(numberOfElementsInCluster)

#print(pcaClusteringDataFrame[pcaClusteringDataFrame["Cluster"] == 1])
