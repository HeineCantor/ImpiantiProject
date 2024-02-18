from os import listdir
FOLDER_PATH = "/home/heinecantor/Dropbox/UNI/Impianti/Esercitazioni/Homework_FFDA/ffdatoolset/tupling_BGLErrorLog-230/"
#FOLDER_PATH = "/home/heinecantor/Dropbox/UNI/Impianti/Esercitazioni/Homework_FFDA/ffdatoolset/tupling_MercuryErrorLog-200/"

currentTuple, nextTuple = None, None

tupleFileList = [f for f in listdir(FOLDER_PATH) if "tuple" in str(f)]
tupleFileList.sort(key=lambda fileName: int(fileName.split('_')[1]))

currentTuple = open(FOLDER_PATH + tupleFileList[0]).read().split('\n')
nextTuple = open(FOLDER_PATH + tupleFileList[1]).read().split('\n')

numberOfTrunactions = 0

dictNodeCount = {}

for i in range(1, len(tupleFileList)):
    lastNodeOfCurrent = currentTuple[-2].split(' ')[1]
    firstNodeOfNext = nextTuple[0].split(' ')[1]

    if(lastNodeOfCurrent == firstNodeOfNext):
        print(f"TRUNCATION: {i} VS. {i+1} --- Node: {firstNodeOfNext}")
        numberOfTrunactions += 1
        if(firstNodeOfNext in dictNodeCount):
            dictNodeCount[firstNodeOfNext] += 1
        else:
            dictNodeCount[firstNodeOfNext] = 1

    currentTuple = nextTuple
    if(i+1 < len(tupleFileList)):
        nextTuple = open(FOLDER_PATH + tupleFileList[i+1]).read().split('\n')

dictNodeCount = sorted(dictNodeCount.items(), key=lambda x:x[1])
print(dictNodeCount)
print(f"\nTotal number of truncations: {numberOfTrunactions}")