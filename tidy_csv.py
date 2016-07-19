import os
import pandas as pd

# All downloaded csv
csv = os.listdir("rawdata")

# Read all downloaded csv
csv = [pd.read_csv(os.path.join("rawdata", x), 
                   skiprows=11, na_values="N.A.") 
       for x in csv]

# Concatenate all csv
air_quality = pd.concat(csv).reset_index(drop=True)

# Convert the data type of DATE to datetime
air_quality["DATE"] = pd.to_datetime(air_quality.DATE, format="%d/%m/%Y")

# Sort the data by STATION, DATE and HOUR
air_quality.sort(["STATION", "DATE", "HOUR"])

# Save air_quality
air_quality.to_csv("data/air_quality.tsv", sep="\t")
#air_quality.to_pickle("data/air_quality.pkl")



