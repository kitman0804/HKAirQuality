import os
import re
import pandas as pd


# All downloaded csv
fileName = os.listdir("rawdata")
station = [re.sub("AIR_[0-9]{4}_(.*)\.csv", "\\1", x) for x in fileName]
station = pd.unique(station)


# Read downloaded csv
def read_raw(x):
    file = pd.read_csv(os.path.join("rawdata", x), 
                       skiprows=11, na_values="N.A.")
    file["DATE"] = pd.to_datetime(file.DATE, format="%d/%m/%Y")
    print("%s was read." % (x))
    return file


def group_raw(station, rawFolder="rawdata", dataFolder="data"):
    fileName = os.listdir(rawFolder)
    files = [read_raw(x) for x in fileName if re.sub("AIR_[0-9]{4}_(.*)\.csv", "\\1", x) == s]
    airQuality = pd.concat(files, axis=0)
    airQuality = airQuality.sort_values(by=["STATION", "DATE", "HOUR"])
    path = os.path.join(dataFolder, "air_quality_%s.tsv" % s)
    airQuality.to_csv(path, sep="\t", index=False)
    print("Data of %s station was saved." % s)


# Combine data by station
for s in station:
    group_raw(station=s)




#air_quality.to_csv("data/air_quality.tsv", sep="\t")
#air_quality.to_pickle("data/air_quality.pkl")



