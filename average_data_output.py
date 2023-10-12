import pandas as pd
import matplotlib.pyplot as plt
import math

def buildDictionary():
    for i in range(len(LIST_SUMMARY_REPORT)):
        dictReportStats[LIST_SUMMARY_REPORT[i]] = LIST_SUMMARY_STATS[i]

def printVMStat(dataFrameStats):
    print("\t========= PROCS")
    print(f"\tPROCESSES NUMBER: {dataFrameStats['r']}")
    print(f"\tPROCESSES NO SLEEP NUMBER: {dataFrameStats['b']}")
    print("\t========= MEMORY")
    print(f"\tVIRTUAL MEMORY: {dataFrameStats['swpd']} kB")
    print(f"\tIDLE MEMORY: {dataFrameStats['free']} kB")
    print(f"\tBUFFER MEMORY: {dataFrameStats['buff']} kB")
    print(f"\tCACHE MEMORY: {dataFrameStats['cache']} kB")
    #print(f"\tINACTIVE MEMORY: {dataFrameStats['inact'].mean()} kB")
    #print(f"\tACTIVE MEMORY: {dataFrameStats['active'].mean()} kB")
    print("\t========= SWAP")
    print(f"\tSWAPPED FROM DISK: {dataFrameStats['si']} kB/s")
    print(f"\tSWAPPED TO DISK: {dataFrameStats['so']} kB/s")
    print("\t========= IO")
    print(f"\tBLOCKS FROM DISK: {dataFrameStats['bi']} blocks/s")
    print(f"\tBLOCKS TO DISK: {dataFrameStats['bo']} blocks/s")
    print("\t========= SYSTEM")
    print(f"\tINTERRUPTS PER SECOND: {dataFrameStats['in']}")
    print(f"\tCONTEXT SWITCH PER SECOND: {dataFrameStats['cs']}")
    print("\t========= CPU")
    print(f"\tUSER TIME: {dataFrameStats['us']} %")
    print(f"\tKERNEL TIME: {dataFrameStats['sy']} %")
    print(f"\tIDLE TIME: {dataFrameStats['id']} %")
    print(f"\tIO TIME: {dataFrameStats['wa']} %")
    print(f"\tVM TIME: {dataFrameStats['st']} %")
    print("===========")

def printResults(avgThrough, avgTime, stdDeviation):
    print(f"=== REPORT {report} ===")
    print(f"\tTHROUGHPUT: {avgThrough}")
    print(f"\tRESPONSE TIME: {avgTime}")
    print(f"\tSTANDARD DEVIATION: {stdDeviation}")

def getPower(throughputVector, responseTimeVector):
    powerList = []
    for i in range(len(throughputVector)):
        powerList.append(throughputVector[i] / responseTimeVector[i])

    return powerList

AverageVMStats = {
    "r" : 0,
    "b" : 0,
    "swpd" : 0,
    "free" : 0,
    "buff" : 0,
    "cache" : 0,
    "si" : 0,
    "so" : 0,
    "bi" : 0,
    "bo" : 0,
    "in" : 0,
    "cs" : 0,
    "us" : 0,
    "sy" : 0,
    "id" : 0,
    "wa" : 0,
    "st" : 0
}

BASE_PATH = "~/Desktop/git/ImpiantiProject/Reports/"

LIST_SUMMARY_REPORT = [ "Summary_Report_Test_1000_",
                        "Summary_Report_Test_2000_",
                        "Summary_Report_Test_3000_",
                        "Summary_Report_Test_3500_",
                        "Summary_Report_Test_4000_",
                        "Summary_Report_Test_4500_",
                        "Summary_Report_Test_5000_",
                        "Summary_Report_Test_6000_",
                        "Summary_Report_Test_6500_",
                        "Summary_Report_Test_7000_"]
MASK_LIST_COLUMNS = ["timeStamp", "threadName", "label", "bytes", "Latency", "elapsed"]

LIST_SUMMARY_STATS = ["VMSTAT_1000_",
                      "VMSTAT_2000_",
                      "VMSTAT_3000_",
                      "VMSTAT_3500_",
                      "VMSTAT_4000_",
                      "VMSTAT_4500_",
                      "VMSTAT_5000_",
                      "VMSTAT_6000_",
                      "VMSTAT_6500_",
                      "VMSTAT_7000_"]

X_AXIS_LIST = [1000, 2000, 3000, 3500, 4000, 4500, 5000, 6000, 6500, 7000]
THROUGHPUT_AXIS_LIST = []
RESPONSE_TIME_AXIS_LIST = []

dictReportStats = {}

buildDictionary()

NUM_OF_MEASURES = 3

averageThroughput = 0
averageResponseTime = 0
averageStandardDeviaton = 0

for report in LIST_SUMMARY_REPORT:
    for key, value in AverageVMStats.items():
        AverageVMStats[key] = 0

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

            for responseTime in dataFrameReports["elapsed"]:
                averageStandardDeviaton += (responseTime - averageResponseTime)**2

            averageStandardDeviaton /= dataFrameReports.count()["elapsed"]
            averageStandardDeviaton = math.sqrt(averageStandardDeviaton)

            for stat in dataFrameStats:
                AverageVMStats[stat] += dataFrameStats[stat].mean()

        averageThroughput /= NUM_OF_MEASURES
        averageThroughputOnMinute = averageThroughput * 60
        averageResponseTime /= NUM_OF_MEASURES

        averageStandardDeviaton /= NUM_OF_MEASURES

        for key, value in AverageVMStats.items():
            AverageVMStats[key] /= NUM_OF_MEASURES

        THROUGHPUT_AXIS_LIST.append(averageThroughput)
        RESPONSE_TIME_AXIS_LIST.append(averageResponseTime)

        averageThroughputOnMinute = averageThroughput * 60

        printResults(averageThroughput, averageResponseTime, averageStandardDeviaton)
        printVMStat(AverageVMStats)
    except Exception as exc:
        print(f"File error: {report}. Cause: {str(exc)}")
        THROUGHPUT_AXIS_LIST.append(1)
        RESPONSE_TIME_AXIS_LIST.append(1)


figure, axis = plt.subplots(3, 1)

figure.set_figheight(10)

axis[0].plot(X_AXIS_LIST, THROUGHPUT_AXIS_LIST, color='b', marker='o')
axis[0].set_title("Throughput")
axis[0].set_ylabel("req/min")

axis[1].plot(X_AXIS_LIST, RESPONSE_TIME_AXIS_LIST, color='r', marker='o')
axis[1].set_title("Response Time")
axis[1].set_ylabel("ms")

axis[2].plot(X_AXIS_LIST, getPower(THROUGHPUT_AXIS_LIST, RESPONSE_TIME_AXIS_LIST), color='g', marker='o')
axis[2].set_title("Power")

figure.tight_layout()

plt.show()