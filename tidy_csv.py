import os
import re
import pandas as pd

# All downloaded csv
fileName = os.listdir("rawdata")
station = [re.sub("AIR_[0-9]{4}_(.*)\.csv", "\\1", x) for x in fileName]
station = pd.unique(station)

# Read downloaded csv
def read_air_quality(x):
    file = pd.read_csv(os.path.join("rawdata", x), 
                       skiprows=11, na_values="N.A.")
    file["DATE"] = pd.to_datetime(file.DATE, format="%d/%m/%Y")
    print("%s was read." % (x))
    return file

# Combine data by station
for s in station:
    files = [x for x in fileName if re.sub("AIR_[0-9]{4}_(.*)\.csv", "\\1", x) == s]
    files = [read_air_quality(x) for x in files]
    air_quality = pd.concat(files, axis=0)
    air_quality = air_quality.sort_values(by=["STATION", "DATE", "HOUR"])
    path = "data/air_quality_%s.tsv" % s
    air_quality.to_csv(path, index=False)
    print("Data of %s station was saved." % s)
    del files, air_quality, path




#air_quality.to_csv("data/air_quality.tsv", sep="\t")
#air_quality.to_pickle("data/air_quality.pkl")



