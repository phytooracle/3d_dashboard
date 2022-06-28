import sys, os, pdb
import numpy as np

# Local modules
import webdav_credentials
from config import Config
import file_inspector
import data_inspector

##################################################
#  Get directories from cyverse that are dates   #
##################################################

fs = file_inspector.WebDav(
            season="season_11_sorghum_yr_2020",
            level="level_2",
            sensor="scanner3DTop"
     )
date_dirs = fs.date_files()

##################################################
#    Get dataframe from RGB cluster csv file     #
##################################################

conf = Config(season=11) # This contains command line arguments, and phytooracle_data classes.
print("Grouping and summarizing plant data.  This can take a few seconds...")
rgb_df = conf.rgb.df

#rgb_df = conf.rgb.df.groupby(by="plant_name").agg(
#        #plant_name=('plant_name', max),
#        #treatment=('treatment', max),
#        n_obs=('date', len),
#        genotype=('genotype', max),
#        #double_lettuce=('double_lettuce', max),
#        med_nw_lat=('nw_lat', np.median),
#        med_nw_lon=('nw_lon', np.median),
#        med_se_lat=('se_lat', np.median),
#        med_se_lon=('se_lon', np.median),
#)
#rgb_df['mean_lat'] = rgb_df[['med_nw_lat', 'med_se_lat']].mean(axis=1)
#rgb_df['mean_lon'] = rgb_df[['med_nw_lon', 'med_se_lon']].mean(axis=1)

##################################################
#                Do some looping                 #
##################################################

date_data_objects = []

for date_dir, date in date_dirs:
    print(date)
    ddo = data_inspector.Level2_3D_Stats(date, date_dir=date_dir, file_inspector=fs)
    if ddo.file_info.values()[0] is not None:
        break
        # int(list(ddo.file_info.values())[0]['size'])/1024/1024
