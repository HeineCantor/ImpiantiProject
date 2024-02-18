from os import listdir

FOLDER_PATH = "/home/heinecantor/Dropbox/UNI/Impianti/Esercitazioni/Homework_FFDA/ffdatoolset/tupling_BGLErrorLog-230/"
#FOLDER_PATH = "/home/heinecantor/Dropbox/UNI/Impianti/Esercitazioni/Homework_FFDA/ffdatoolset/tupling_MercuryErrorLog-200/"

tupleFileList = [f for f in listdir(FOLDER_PATH) if "tuple" in str(f)]

numberOfCollisions = 0

for i in range(len(tupleFileList)):
    tupleContent = open(FOLDER_PATH + tupleFileList[i]).read().split('\n')

    nodesList = list(set([x.split(' ')[1] for x in tupleContent[:-1]]))

    if(len(nodesList) > 1):
        print(f"COLLISION: on tuple {i}")
        numberOfCollisions += 1

print(f"\nTotal number of collisions: {numberOfCollisions}")