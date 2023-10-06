import pandas as pd

BASE_PATH = "~/Desktop/Progetto Impianti/ImpiantiProject/Reports/"
LIST_SUMMARY_REPORT = [ "Summary_Report_Test_1000_",
                        "Summary_Report_Test_3000_",
                        "Summary_Report_Test_5000_",
                        "Summary_Report_Test_7000_"]
MASK_LIST_COLUMNS = ["timeStamp", "threadName", "label", "bytes", "Latency", "elapsed"]

NUM_OF_MEASURES = 3

averageThroughput = 0
averageResponseTime = 0

for report in LIST_SUMMARY_REPORT:
    try:
        for i in range(NUM_OF_MEASURES):
            dataFrame = pd.read_csv(BASE_PATH + report + str(i+1) + ".csv")

            maxTimestamp = dataFrame.max()["timeStamp"]
            minTimestamp = dataFrame.min()["timeStamp"]
            duration = (maxTimestamp - minTimestamp)/1000

            totalOfRequests = dataFrame.count()["timeStamp"]

            throughput = totalOfRequests / duration
            
            averageResponseTime += dataFrame["elapsed"].mean()
            averageThroughput += throughput

        averageThroughput /= NUM_OF_MEASURES
        averageResponseTime /= NUM_OF_MEASURES

        averageThroughputOnMinute = averageThroughput * 60

        print(f"=== REPORT {report} ===")
        print(f"\tTHROUGHPUT: {averageThroughputOnMinute}")
        print(f"\tRESPONSE TIME: {averageResponseTime}")
        print("===========")
    except Exception as exc:
        print(f"File error: {report}. Cause: {exc}")