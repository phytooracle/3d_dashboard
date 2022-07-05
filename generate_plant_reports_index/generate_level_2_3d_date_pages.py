import sys, glob, os, pdb
from itertools import groupby
from operator import itemgetter
from pathlib import Path
import numpy as np
import pandas as pd
import altair as alt
import re
import subprocess
import pickle

from config import Config
import altair_figures
import dashboard_html
import file_inspector
import data_inspector

"""

USEAGE:

You have to run `generate_level_2_3d_homepage.py` first so that
`date_data_objects.pickle` is created, which is used by this script.

"""

season = "season_11_sorghum_yr_2020"
level  = "level_2"
sensor = "scanner3DTop"
#date = '2020-07-17'

MIN_OBS = 5
BASE_URL = f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/scanner3DTop"

data_category_strings = {
        'good_data' : "Valid useable data",
        #'double_lettuce' : "Double lettuces",
        'low_observations' : "Low frequency plants*",
}

if __name__ == "__main__":

    fs = file_inspector.FileInspector(
                season=season,
                level=level,
                sensor=sensor
         )

    conf = Config(season=11) # This contains command line arguments,
                             # and phytooracle_data classes.
    conf.BASE_URL = BASE_URL
    conf.handle_command_line_aruments()
    date = conf.args.date

    #########################################################
    # Get all of our RGB plant data squared away and in `df`
    #########################################################

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

    #df = df.astype({ "double_lettuce" : bool })

    df['mean_lat'] = df[['med_nw_lat', 'med_se_lat']].mean(axis=1)
    df['mean_lon'] = df[['med_nw_lon', 'med_se_lon']].mean(axis=1)
    print()

    _o=[]
    with (open("date_data_objects.pickle", "rb")) as openfile:
        _o.append(pickle.load(openfile))
    date_data_objects           = _o[0]['date_data_objects']
    date_data_objects_timestamp = _o[0]['timestamp']

    ##########################################
    # Get a list of 3D plants for this date.
    ##########################################

    #path = f"/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/dashboard/{conf.args.date}/plant_reports"
    #print(f"getting directory list from: {path}")
    #run_result = subprocess.run(["ils", path], stdout=subprocess.PIPE).stdout
    #ils_lines = run_result.decode('utf-8').splitlines()
    #print(f"   ... got {len(ils_lines)} lines from ils")
    #files_in_directory = [x.split("/")[-1] for x in ils_lines if "  C- " in x]
    #plant_dirs = [x for x in files_in_directory if re.search(r'.+_\d+$', x)]

    _, date_dir, ddo = [x for x in date_data_objects if x[0] == date][0]
    plant_dirs = [x.rstrip("/") for x in ddo.plant_reports['contents']]
    print(f"   ... found {len(plant_dirs)} plant directories")

    ######################
    # Loop through plants 
    ######################
    # We're going to figure out what groups of good, double, and rarely observed plants
    # we have for each genotype by looping through all of the plants and doing our
    # bean counting in genotype_dict

    genotype_dict = {}
    all_valid_plants = []

    data_counts = {
            'good_data' : 0,
            'low_observations' : 0,
            #'double_lettuce' : 0
    }
    #for t in df.treatment.unique():
        #data_counts[t] = 0

    for count, plant_id in enumerate(plant_dirs):
        count += 1
        print(f"({count}/{len(plant_dirs)}) : {plant_id}")

#        if plant_id[0:3] == "PI_":
#            print("here")
#            genotype = "".join(plant_id.split("_")[0:2])
#        elif plant_id[0:2] == "PI":
#            print("and here?")
#            genotype = plant_id.split("_")[0]
#        else:
#            genotype = "_".join(plant_id.split("_")[0:2])

        plant_data = df.loc[plant_id]   # fails if plant isn't in df.  We like that.

        # additional sanity check
#        if plant_data.genotype != genotype:
#            raise Exception(f"Unexpected genotype: {plant_data.genotype} != {genotype}")

        if plant_data.genotype not in genotype_dict.keys():
            # We haven't seen this genotype yet, so initialize our dictionary.
            genotype_dict[plant_data.genotype]                     = {}
            genotype_dict[plant_data.genotype]['count']            = 0
            genotype_dict[plant_data.genotype]['good_data']        = []
            genotype_dict[plant_data.genotype]['low_observations'] = []
            #genotype_dict[plant_data.genotype]['double_lettuce']   = []

        genotype_dict[plant_data.genotype]['count'] += 1
        # Let's determine which bin this plant goes into...

        #if plant_data.double_lettuce:
            #genotype_dict[plant_data.genotype]['double_lettuce'].append(plant_data)
            #data_counts['double_lettuce'] += 1
        if (plant_data.n_obs < MIN_OBS):
            genotype_dict[plant_data.genotype]['low_observations'].append(plant_data)
            data_counts['low_observations'] += 1
        else:
            genotype_dict[plant_data.genotype]['good_data'].append(plant_data)
            data_counts['good_data'] += 1

        #data_counts[plant_data.treatment] += 1

    ##################################################
    #           Create and save HTML files           #
    ##################################################

    meta_html = f"""
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
        <link href="https://codepen.io/chriddyp/pen/bWLwgP.css" rel="stylesheet">
        <body>
        <h1>{date}</h1>
        <table>
        <tr>
        <td>
            <ul>
            <li>{len(plant_dirs)} Plants
                 <ul>
                 <li> Valid plants: {data_counts['good_data']}
                 <li> Low number of observations: {data_counts['low_observations']}
                 <li> Double lettuce:
                 </ul>
            <li>{len(genotype_dict.keys())} Genotypes
            </ul>
        <td>
            <ul>
    """

    #for t in df.treatment.unique():
        #meta_html += f"<li>{t}: {data_counts[t]}"

    meta_html += f"""
            </ul>
        </td>
        </tr>
        </table>
        </pre>
        <a href="random.html">Some Random (Valid) Plants</a><br>
        <a href="random2.html">Some More Random (Valid) Plants</a><br>
        <a href="random3.html">Some Even More Random (Valid) Plants</a><br>
        <a href="random4.html">Some Even More More Random (Valid) Plants</a><br>
        <table>
    """

    # Make our cool alphabetical index...
    for letter, genotypes in groupby(sorted(genotype_dict.keys()), key=itemgetter(0)):
        print(letter)

        meta_html += f"<hr><b>{letter}</b>\n"

        for g in genotypes:
            all_valid_plants += genotype_dict[g]['good_data']
            genotype_index_file = f"{g}.html"
            meta_html += f"<li><a href='{genotype_index_file}'>{g}</a> ({genotype_dict[g]['count']} plants)\n"

            genotype_html = f"""
                <html>
                <body>
                <h1>{g} : {date}</h1>
                <ul>
            """
            for category in ['good_data', 'low_observations']:
                genotype_html += f"<li>{data_category_strings[category]}: {len(genotype_dict[g][category])} plants"

            genotype_html += "</ul>"

            for category in ['good_data', 'low_observations']:

                if len(genotype_dict[g]) == 0:
                    continue


                genotype_html += f"""
                    <h2><a id="{category}">{data_category_strings[category]} ({len(genotype_dict[g][category])} plants)</h2>
                    <table>
                """

                #genotype_html += f"<tr><th></th><th></th><th>Geocorection<th>Soil<br>Identification</th><th>Plant<br>Segmentation</th></tr>"
                genotype_html += f"<tr><th></th><th></th><th>Plant Crop</th></tr>"


                for plant_data in genotype_dict[g][category]:
                    genotype_html += dashboard_html.plant_data_row(plant_data, BASE_URL, conf)

                genotype_html += f"""
                    </tr>
                    </table>
                """

            genotype_html += f"""
                </table>
                <footnote>*{data_category_strings['low_observations']} plants are defined as plants with less than {MIN_OBS} RGB observations.</footnote>
                </body>
                </html>
            """
            with open(f"outputs/{genotype_index_file}", "w") as genotype_html_fh:
                genotype_html_fh.write(genotype_html);

meta_html += f"""
    </table>
	<hr>
	<p><a href="../index.html">Dashboard Home</a></p>
    <footnote>*{data_category_strings['low_observations']} plants are defined as plants with less than {MIN_OBS} RGB observations.</footnote>
    </body>
    </html>
"""
with open("outputs/index.html", "w") as meta_html_file:
    meta_html_file.write(meta_html);


dashboard_html.create_random_plants_page(all_valid_plants, conf, filename="outputs/random.html")
dashboard_html.create_random_plants_page(all_valid_plants, conf, filename="outputs/random2.html")
dashboard_html.create_random_plants_page(all_valid_plants, conf, filename="outputs/random3.html")
dashboard_html.create_random_plants_page(all_valid_plants, conf, filename="outputs/random4.html")
