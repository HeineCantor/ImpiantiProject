import pandas as pd
import matplotlib.pyplot as plt

def buildDictionary():
    for i in range(len(LIST_SUMMARY_REPORT)):
        dictReportStats[LIST_SUMMARY_REPORT[i]] = LIST_SUMMARY_STATS[i]

def printResults(avgThrough, avgTime, dataFrameStats):
    print(f"=== REPORT {report} ===")
    print(f"\tTHROUGHPUT: {avgThrough}")
    print(f"\tRESPONSE TIME: {avgTime}")
    print("\t========= PROCS")
    print(f"\tPROCESSES NUMBER: {dataFrameStats['r'].mean()}")
    print(f"\tPROCESSES NO SLEEP NUMBER: {dataFrameStats['b'].mean()}")
    print("\t========= MEMORY")
    print(f"\tVIRTUAL MEMORY: {dataFrameStats['swpd'].mean()} kB")
    print(f"\tIDLE MEMORY: {dataFrameStats['free'].mean()} kB")
    print(f"\tBUFFER MEMORY: {dataFrameStats['buff'].mean()} kB")
    print(f"\tCACHE MEMORY: {dataFrameStats['cache'].mean()} kB")
    #print(f"\tINACTIVE MEMORY: {dataFrameStats['inact'].mean()} kB")
    #print(f"\tACTIVE MEMORY: {dataFrameStats['active'].mean()} kB")
    print("\t========= SWAP")
    print(f"\tSWAPPED FROM DISK: {dataFrameStats['si'].mean()} kB/s")
    print(f"\tSWAPPED TO DISK: {dataFrameStats['so'].mean()} kB/s")
    print("\t========= IO")
    print(f"\tBLOCKS FROM DISK: {dataFrameStats['bi'].mean()} blocks/s")
    print(f"\tBLOCKS TO DISK: {dataFrameStats['bo'].mean()} blocks/s")
    print("\t========= SYSTEM")
    print(f"\tINTERRUPTS PER SECOND: {dataFrameStats['in'].mean()}")
    print(f"\tCONTEXT SWITCH PER SECOND: {dataFrameStats['cs'].mean()}")
    print("\t========= CPU")
    print(f"\tUSER TIME: {dataFrameStats['us'].mean()} %")
    print(f"\tKERNEL TIME: {dataFrameStats['sy'].mean()} %")
    print(f"\tIDLE TIME: {dataFrameStats['id'].mean()} %")
    print(f"\tIO TIME: {dataFrameStats['wa'].mean()} %")
    print(f"\tVM TIME: {dataFrameStats['st'].mean()} %")
    print("===========")

def getPower(throughputVector, responseTimeVector):
    powerList = []
    for i in range(len(throughputVector)):
        powerList.append(throughputVector[i] / responseTimeVector[i])

    return powerList

BASE_PATH = "~/Desktop/Progetto Impianti/ImpiantiProject/Reports/"

LIST_SUMMARY_REPORT = [ "Summary_Report_Test_1000_",
                        "Summary_Report_Test_3000_",
                        "Summary_Report_Test_5000_",
                        "Summary_Report_Test_7000_"]
MASK_LIST_COLUMNS = ["timeStamp", "threadName", "label", "bytes", "Latency", "elapsed"]

LIST_SUMMARY_STATS = ["VMSTAT_1000_",
                      "VMSTAT_3000_",
                      "VMSTAT_5000_",
                      "VMSTAT_7000_"]

X_AXIS_LIST = [1000, 3000, 5000, 7000]
THROUGHPUT_AXIS_LIST = []
RESPONSE_TIME_AXIS_LIST = []

dictReportStats = {}

buildDictionary()

NUM_OF_MEASURES = 3

averageThroughput = 0
averageResponseTime = 0

for report in LIST_SUMMARY_REPORT:
    averageThroughput = 0
    averageResponseTime = 0
    try:
        for i in range(NUM_OF_MEASURES):
            dataFrameReports = pd.read_csv(BASE_PATH + report + str(i+1) + ".csv")
            dataFrameStats = pd.read_csv(BASE_PATH + dictReportStats[report] + str(i+1) + ".txt", delim_whitespace=True)

            maxTimestamp = dataFrameReports.max()["timeStamp"]
            minTimestamp = dataFrameReports.min()["timeStamp"]
            duration = (maxTimestamp - minTimestamp)/1000

            totalOfRequests = dataFrameReports.count()["timeStamp"]

            throughput = totalOfRequests / duration
            
            averageResponseTime += dataFrameReports["elapsed"].mean()
            averageThroughput += throughput

        averageThroughput /= NUM_OF_MEASURES
        averageThroughputOnMinute = averageThroughput * 60
        averageResponseTime /= NUM_OF_MEASURES

        THROUGHPUT_AXIS_LIST.append(averageThroughputOnMinute)
        RESPONSE_TIME_AXIS_LIST.append(averageResponseTime)

        averageThroughputOnMinute = averageThroughput * 60

        printResults(averageThroughputOnMinute, averageResponseTime, dataFrameStats)
    except Exception as exc:
        print(f"File error: {report}. Cause: {str(exc)}")
        THROUGHPUT_AXIS_LIST.append(1)
        RESPONSE_TIME_AXIS_LIST.append(1)


plt.plot(X_AXIS_LIST, THROUGHPUT_AXIS_LIST)
plt.plot(X_AXIS_LIST, RESPONSE_TIME_AXIS_LIST)
plt.plot(X_AXIS_LIST, getPower(THROUGHPUT_AXIS_LIST, RESPONSE_TIME_AXIS_LIST))
plt.show()