import sys, glob, os, pdb
from itertools import groupby
from operator import itemgetter
import pandas as pd
import numpy as np
import subprocess
from config import Config
import re
from operator import itemgetter
import dashboard_html

#sys.path.append("./phytooracle_data")
#import phytooracle_data.scanner3dTop as scanner3dTop
#import phytooracle_data.stereoTop as stereoTop
#import phytooracle_data.rgb as rgb


conf = Config(season=11) # This contains command line arguments, and phytooracle_data classes.


print("Grouping and summarizing plant data.  This can take a few seconds...")
df = conf.rgb.df.groupby(by="plant_name").agg(
        #plant_name=('plant_name', max),
        #treatment=('treatment', max),
        n_obs=('date', len),
        genotype=('genotype', max),
        #double_lettuce=('double_lettuce', max),
        med_nw_lat=('nw_lat', np.median),
        med_nw_lon=('nw_lon', np.median),
        med_se_lat=('se_lat', np.median),
        med_se_lon=('se_lon', np.median),
)

df['mean_lat'] = df[['med_nw_lat', 'med_se_lat']].mean(axis=1)
df['mean_lon'] = df[['med_nw_lon', 'med_se_lon']].mean(axis=1)
print()

    ##########################################
    # Get a list of 3D plants for this date.
    ##########################################

    import credentials
    import file_inspector

    remote_base_path = os.path.join("public_html", conf.rgb.season.name())
    fs = file_inspector.FTP(server='sdf.org', username=credentials.username, password=credentials.password)
    fs.ftp.cwd(remote_base_path)
    dir_contents = []
    fs.ftp.dir(dir_contents.append)

#    path = f"/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/dashboard/{conf.args.date}/plant_reports"
#    print(f"getting directory list from: {path}")
#    run_result = subprocess.run(["ils", path], stdout=subprocess.PIPE).stdout
#    ils_lines = run_result.decode('utf-8').splitlines()
#    print(f"   ... got {len(ils_lines)} lines from ils")
#    files_in_directory = [x.split("/")[-1] for x in ils_lines if "  C- " in x]
#    plant_dirs = [x for x in files_in_directory if re.search(r'.+_\d+$', x)]
#    print(f"   ... found {len(plant_dirs)} plant directories")

