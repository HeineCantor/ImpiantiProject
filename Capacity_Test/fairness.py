import pandas as pd

def getFairnessIndex(throughputList : list):
    numerator = sum(throughputList)**2
    denominator = len(throughputList) * sum([x**2 for x in throughputList])

    return numerator/denominator

BASE_PATH = "~/Desktop/git/ImpiantiProject/Capacity_Test/FairnessReports/Fair/Summary_Report_Test"

nominalThroughputs = [1100, 800, 500]
dataFrameReports = []

dataFrameReports.append(pd.read_csv(BASE_PATH + "_Low" + ".csv"))
dataFrameReports.append(pd.read_csv(BASE_PATH + "_Mid" + ".csv"))
dataFrameReports.append(pd.read_csv(BASE_PATH + "_High" + ".csv"))

throughputs = []

for index, dataframe in enumerate(dataFrameReports):
    maxTimestamp = dataframe.max()["timeStamp"]
    minTimestamp = dataframe.min()["timeStamp"]
    duration = (maxTimestamp - minTimestamp)/1000

    totalOfRequests = dataframe.count()["timeStamp"]

    throughput = totalOfRequests / duration * 60

    throughput /= nominalThroughputs[index]

    throughputs.append(throughput)

throughputs = [0.8635, 0.6916, 0.3732]
print(throughputs)
print(getFairnessIndex(throughputs))