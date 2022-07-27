import sys, os, pdb
import numpy as np
import pickle
import datetime

# Local modules
import webdav_credentials
from config import Config
import file_inspector
import data_inspector

print("Starting.")
USE_PICKLE = True

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

##################################################
#    Get dataframe from RGB cluster csv file     #
##################################################


conf = Config(season=11) # This contains command line arguments, and phytooracle_data classes.
rgb_df = conf.rgb.df

if USE_PICKLE:
    print(f"Loading info from pickle")
    objects = []
    with (open("date_data_objects.pickle", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    date_data_objects = objects[0]['date_data_objects']
    timestamp         = objects[0]['timestamp']
else:
    timestamp = datetime.datetime.now()
    date_dirs = fs.date_files()
    date_data_objects = []
    for date_dir, date in date_dirs:
        print(f"Fetching {date}")
        ddo = data_inspector.Level2_3D_Stats(date, date_dir=date_dir, file_inspector=fs)
        date_data_objects.append([date, date_dir, ddo])


##################################################
#                   Make HTML                    #
##################################################

index_html = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    <link href="https://codepen.io/chriddyp/pen/bWLwgP.css" rel="stylesheet">
    <body>
    <h1><a href="../..">{season}</a>/<a href="..">{level}</a>/{sensor}</h1>
    <hr>
    <p>Report Run: {timestamp}</p>
    <a href="dashboard/pipeline_data_products.html">Cool interactive pipeline dataproducts progress chart</a>
    <hr>
    <table>
    <tr>
        <th>Date</th>
        <th>reports tar size</th>
        <th>pointclouds tar size</th>
        <th># Plants in Reports</th>
        <!--<th># Plants in RGB csv</th>-->
"""

##################################################
#               LOOP THROUGH DATES               #
##################################################

for date, date_dir, ddo in date_data_objects:
    ##################################################
    #             plant_reports.tar size             #
    ##################################################
    if list(ddo.file_info.values())[0] is None:
        plant_reports_size = "None"
    else:
        plant_reports_size = list(ddo.file_info.values())[0]['size']

    ##################################################
    #       segmentation_pointclouds.tar size        #
    ##################################################
    if list(ddo.file_info.values())[1] is None:
        segmentation_pointclouds_tar_size = "None"
    else:
        segmentation_pointclouds_tar_size = list(ddo.file_info.values())[1]['size']

    ##################################################
    #                   date link                    #
    # aka link to plant_reports
    ##################################################
    #date_html = f"{date}" # Default, no link.
    date_dir_link = f"<a href='{date}/individual_plants_out/', title='Link to individual_plants_out directory'>{date}</a>"
    dashboard_link = f"(please ibun plant_reports)"
    if ddo.plant_reports['exists']:
        if 'index.html' in ddo.plant_reports['contents']:
            dashboard_link = f"<a href='{date}/individual_plants_out/plant_reports/index.html', title='Link to dashboard index.html'>{date} Dashboard</a>"
        else:
            dashboard_link = f"No Dashboard. <a href='{date}/individual_plants_out/plant_reports/', title='Dashboard not generated for this date, link to reports dir.'>(reports dir)</a>"

    ##################################################
    #       Number of plants in plant reports        #
    ##################################################
    n_plants_in_plant_reports = len(ddo.plant_reports['contents'])
    ##################################################
    #          Number of plants in rgb csv           #
    ##################################################
    n_plants_in_rgb_csv = rgb_df[ rgb_df.date == date ].shape[0]
    ##################################################
    #                 Processing Log                 #
    ##################################################
    pr_log_coi_1 = [
        #'Scan Date',
        'Pre-processing Status',
        'Individual',
        'Finish Date',
        #'Benchmark log',
    ]
    pr_log_coi_2 = [
        'Landmark Selection Status',
        'Individual.1',
        'Finish Date.1',
        'Notes.1',
    ]
    pr_log_coi_3 = [
        #'Scan Date',
        'Post-processing Status',
        'Individual.2',
        'Finish Date.2',
        'Notes.1',
        #'Plant reports dir stashed',
        'Server environment',
        #'Ibunning Complete',
        #'Volume & TDA Extraction - full volume & 0.09 voxel size Status ',
        #'Individual.3',
        #'Finish Date.3'
    ]

    index_html += f"""

    <tr>
        <td>
        <h3>{date_dir_link}</h3>
        <li>{dashboard_link}
        </td>
        <td>{plant_reports_size}</td>
        <td>{segmentation_pointclouds_tar_size}</td>
        <td>{n_plants_in_plant_reports}</td>
        <!--<td>{n_plants_in_rgb_csv}</td>-->
    </tr>
    <!--
    <tr>
        <td colspan=4>
            {dashboard_link}
            <small>
                Changes to google sheets broke this.  Will return later
            </small>
        </td>
    </tr>
    -->
    """
        #<small><pre>{ddo.pr_log.set_index('Scan Date')[pr_log_coi_1].to_markdown(tablefmt="grid")}</pre></small>
        #<small><pre>{ddo.pr_log.set_index('Scan Date')[pr_log_coi_2].to_markdown(tablefmt="grid")}</pre></small>
        #<small><pre>{ddo.pr_log.set_index('Scan Date')[pr_log_coi_3].to_markdown(tablefmt="grid")}</pre></small>

index_html += f"""
    </table>
	<hr>
	<!--<p><a href="../index.html">Dashboard Home</a></p>-->
    </body>
    </html>
"""

with open("outputs/index.html", "w") as index_html_file:
    index_html_file.write(index_html);

with open('date_data_objects.pickle', 'wb') as f:
    pickle.dump({'date_data_objects' : date_data_objects, 'timestamp':timestamp}, f)
with open('outputs/date_data_objects.pickle', 'wb') as f:
    pickle.dump({'date_data_objects' : date_data_objects, 'timestamp':timestamp}, f)
