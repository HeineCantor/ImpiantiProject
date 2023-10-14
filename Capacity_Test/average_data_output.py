import pandas as pd
import matplotlib.pyplot as plt
import math

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

AverageVMStats_AXIS_LIST = {
    "r" : [],
    "b" : [],
    "swpd" : [],
    "free" : [],
    "buff" : [],
    "cache" : [],
    "si" : [],
    "so" : [],
    "bi" : [],
    "bo" : [],
    "in" : [],
    "cs" : [],
    "us" : [],
    "sy" : [],
    "id" : [],
    "wa" : [],
    "st" : []
}

BASE_PATH = "~/Desktop/git/ImpiantiProject/Capacity_Test/Reports/"
SUMMARY_REPORT_PREFIX = "Summary_Report_Test_"
VMSTAT_REPORT_PREFIX = "VMSTAT_"

MASK_LIST_COLUMNS = ["timeStamp", "threadName", "label", "bytes", "Latency", "elapsed"]

X_AXIS_LIST = [1000, 2000, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 10000, 15000, 17000, 19000, 20000]

THROUGHPUT_AXIS_LIST = []
RESPONSE_TIME_AXIS_LIST = []

averageThroughput = 0
averageResponseTime = 0
averageStandardDeviaton = 0

for load in X_AXIS_LIST:
    for key, value in AverageVMStats.items():
        AverageVMStats[key] = 0

    averageThroughput = 0
    averageResponseTime = 0
    try:
        dataFrameReports = pd.read_csv(BASE_PATH + SUMMARY_REPORT_PREFIX + str(load) + ".csv")
        dataFrameStats = pd.read_csv(BASE_PATH + VMSTAT_REPORT_PREFIX + str(load) + ".txt", delim_whitespace=True)

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
            AverageVMStats_AXIS_LIST[stat].append(AverageVMStats[stat])

        averageThroughputOnMinute = averageThroughput * 60

        THROUGHPUT_AXIS_LIST.append(averageThroughput)
        RESPONSE_TIME_AXIS_LIST.append(averageResponseTime)

        averageThroughputOnMinute = averageThroughput * 60

        #printResults(averageThroughput, averageResponseTime, averageStandardDeviaton)
        #printVMStat(AverageVMStats)
    except Exception as exc:
        print(f"File error: {load}. Cause: {str(exc)}")
        THROUGHPUT_AXIS_LIST.append(1)
        RESPONSE_TIME_AXIS_LIST.append(1)
        for stat in AverageVMStats.keys():
            AverageVMStats_AXIS_LIST[stat].append(1)


figure, axis = plt.subplots(3, 1)

figure.set_figheight(10)

axis[0].plot(X_AXIS_LIST, THROUGHPUT_AXIS_LIST, color='b', marker='o')
axis[0].set_title("Throughput")
axis[0].set_ylabel("req/s")

axis[1].plot(X_AXIS_LIST, RESPONSE_TIME_AXIS_LIST, color='r', marker='o')
axis[1].set_title("Response Time")
axis[1].set_ylabel("ms")

axis[2].plot(X_AXIS_LIST, getPower(THROUGHPUT_AXIS_LIST, RESPONSE_TIME_AXIS_LIST), color='g', marker='o')
axis[2].set_title("Power")

figure.tight_layout()

#plt.show()

figure, axis = plt.subplots(3, 2)

axis[0, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["b"], marker='o', label="Waiting processes")
#axis[0, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["r"])
axis[0, 0].legend()

axis[0, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["swpd"], marker='o', label="Virtual Memory")
axis[0, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["free"], marker='o', label="Free Memory")
axis[0, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["buff"], marker='o', label="Buffer Memory")
axis[0, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["cache"], marker='o', label="Cache Memory")
axis[0, 1].set_ylabel("kB")
axis[0, 1].legend()

axis[1, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["si"], marker='o', label="Virtual Memory Swapped-in")
axis[1, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["so"], marker='o', label="Virtual Memory Swapped-out")
axis[1, 0].set_ylabel("kB/s")
axis[1, 0].legend()

axis[1, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["bi"], marker='o', label="Memory blocks read")
axis[1, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["bo"], marker='o', label="Memory blocks written")
axis[1, 1].set_ylabel("blocks/s")
axis[1, 1].legend()

axis[2, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["in"], marker='o', label="Interrupt per second")
axis[2, 0].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["cs"], marker='o', label="Context-switches per second")
axis[2, 0].legend()

axis[2, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["us"], marker='o', label="User Time")
axis[2, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["sy"], marker='o', label="Kernel Time")
axis[2, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["id"], marker='o', label="Idle Time")
axis[2, 1].plot(X_AXIS_LIST, AverageVMStats_AXIS_LIST["wa"], marker='o', label="I/O Waiting Time")
axis[2, 1].set_ylabel("%")
axis[2, 1].legend()

figure.set_figwidth(10)
figure.set_figheight(10)

figure.tight_layout()

plt.show()