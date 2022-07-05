import sys, os, pdb
import numpy as np
import pickle
import pandas as pd

# Local modules
import webdav_credentials
from config import Config
import file_inspector
import data_inspector

##################################################
#  Get directories from cyverse that are dates   #
##################################################

season = "season_11_sorghum_yr_2020"
level  = "level_2"
sensor = "scanner3DTop"

fs = file_inspector.FileInspector(
            season=season,
            level=level,
            sensor=sensor
     )

date_dirs = fs.date_files()

for date_dir, date in date_dirs:
    print()
    print(f"{date_dir}")

    ##################################################
    #         Are there a plant_reports dir?         #
    ##################################################
    plant_reports_dir = os.path.join(date_dir, "individual_plants_out", "plant_reports")
    if not fs.file_exists(path=plant_reports_dir):
        print("No plant_reports dir.  Skipping.")
        continue

    break
    print("Found plant_reports dir.")
    plants = fs.files(path=plant_reports_dir)

    print(f"Found {len(plants)} plants in plant_reports")
    if len(plants) < 2:
        print("Too few plants.  Skipping.")
        continue

    test_plant = plants[1]
    csv_path = os.path.join(plant_reports_dir, test_plant, "pointcloud_stats.csv")
    fs.file_exists(path=csv_path)

    df = pd.read_csv("https://data.cyverse.org/dav/iplant/projects/phytooracle/"+csv_path)
    break
    #print(fs.file_exists(path=os.path.join(date_dir,"summary_data")))
