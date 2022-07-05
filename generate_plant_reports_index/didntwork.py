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

fs = file_inspector.FileInspector(
            season=season,
            level=level,
            sensor=sensor
     )

level_0_dates = sorted([x[1] for x in fs.date_files(level='level_0')])
level_1_dates = sorted([x[1] for x in fs.date_files(level='level_1')])
level_2_dates = sorted([x[1] for x in fs.date_files()])

season_date_range = pd.date_range(start=level_0_dates[0], end=level_0_dates[-1])
scan_df = pd.DataFrame(index=season_date_range, columns=['3D_level_0', '3D_level_1', '3D_level_2',])
scan_df.index.name = 'date'

scan_df.loc[level_0_dates, '3D_level_0'] = 1
scan_df.loc[level_1_dates, '3D_level_1'] = 1
scan_df.loc[level_2_dates, '3D_level_2'] = 1

#############################

#alt.renderers.enable('html')
import altair as alt
alt.renderers.enable('altair_viewer')

cal_chart = alt.Chart(scan_df).mark_rect().encode(
        #x = alt.X(field='date', type='temporal', title='Scan Date'),
        #y = alt.Y(field='level', type='nominal', title='Level')
)

#nulls = cal_chart.transform_filter(
#  "!isValid(datum.level)"
#).mark_rect(opacity=0.5).encode(
#  alt.Color('level:N', scale=alt.Scale(scheme='greys'))
#)
#chart = cal_chart + nulls

cal_chart.show()
