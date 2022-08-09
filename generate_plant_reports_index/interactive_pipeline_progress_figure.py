import sys, os, pdb
import numpy as np
import pickle
import pandas as pd
import altair as alt

# Local modules
import webdav_credentials
from config import Config
import file_inspector
import data_inspector

season = "season_11_sorghum_yr_2020"
level  = "level_2"
sensor = "scanner3DTop"

def make_urls_for_dates(dates, season=season, level=level, sensor=sensor):
    if level == 'plant_reports':
        return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/level_2/{sensor}/{x}/individual_plants_out/plant_reports/index.html" for x in dates]
    if level == 'level_0':
        return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}" for x in dates]
    if level == 'landmark_selection':
        level = 'level_2'

    return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}/{x}/" for x in dates]


def create_df(season, level, sensor, force_overwrite=False):

    if not force_overwrite:
        if os.path.isfile("outputs/pipeline_data_products.csv") :
            scan_df = pd.read_csv("outputs/pipeline_data_products.csv")
            return scan_df

    fs = file_inspector.FileInspector(
                season=season,
                level=level,
                sensor=sensor
         )

    dates = []
    dataproduct_labels = []
    urls = []

    # Level 0
    # - We confirm the existance of level_0 data just from the date file
    level_0_dates = sorted([x[1] for x in fs.date_files(level='level_0')])
    dates += level_0_dates
    dataproduct_labels += [f"3d_level_0"] * len(level_0_dates)
    urls += make_urls_for_dates(level_0_dates, season=season, level='level_0', sensor=sensor)

    # Beyond Level 0
    # - we have to check certain files to see if certain pipeline steps have completed.
    # - we use the Date_3D.pipeline_step_completed() to check 
    for l in ['level_1', 'landmark_selection', 'level_2', 'plant_reports']:

        d = [x for x in level_0_dates if data_inspector.Date_3D(x, file_inspector=fs).pipeline_step_completed(l)]
        dates += d
        dataproduct_labels += [f"3d_{l}"] * len(d)
        urls += make_urls_for_dates(d, season=season, level=l, sensor=sensor)
        #urls += 
        # [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}/{x}/

    rgb_dates = sorted([x[1] for x in fs.date_files(level='level_0', sensor="stereoTop")])
    rgb_labels     = ["rgb_level_0"] * len(rgb_dates)
    rgb_urls = [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/level_0/stereoTop/"] * len(rgb_dates)

    dates += rgb_dates
    dataproduct_labels += rgb_labels
    urls += rgb_urls

    scan_df = pd.DataFrame(list(zip(dates, dataproduct_labels, urls)), columns=['date', 'level', 'url'])
    scan_df.to_csv("outputs/pipeline_data_products.csv")
    return scan_df


def create_chart(scan_df):

    chart = alt.Chart(scan_df).mark_point(
            filled=True,
            size=90
    ).encode(
            alt.X('date:T', axis=alt.Axis(title="Date")),
            alt.Y('level:N', axis=alt.Axis(title="Data Product"),
            sort=['rgb_level_0', '3d_level_0', '3d_level_1', '3d_landmark_selection', '3d_level_2', '3d_plant_reports']),
            href='url:N',
            tooltip=['date:T'],
    ).properties(
            title='Pipeline 3D Data Products',
            width=800,
            height=100
    )

    # Doesn't seem to work.
    chart.configure_title(
            fontSize=20,
            font='Courier',
            anchor='start',
            color='gray'
    )

    chart.save("outputs/pipeline_data_products.html", scale_factor=2)


# MAIN

scan_df = create_df(season, level, sensor, force_overwrite=False)
create_chart(scan_df)
