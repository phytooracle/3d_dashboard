import pandas as pd


BASE_URL = f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle"

def fetch_processing_log_entry(date,
                     sheet_id = "19QS5MpVzw7gv-SPHe1HQO7iJ2x6njFEMskNMCjZF84k",
                     sheet_name = "Season_11"
):
    print("GETTING SHEET!")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    return df[ df['Scan Date'] == date ]


def find_dates_to_unbin(scan_df, file_inspector=None):
    """
    scan_df is from figure_sensor_dates.py

    import data_inspector
    season = "season_11_sorghum_yr_2020"
    level  = "level_2"
    sensor = "scanner3DTop"

    fs = file_inspector.FileInspector(
                season=season,
                level=level,
                sensor=sensor
         )

    data_inspector.find_dates_to_unbin(scan_df, file_inspector=fs)

    """
    dates_to_check = scan_df[ scan_df['level'] == '3d_level_2' ]['date'].values
    dates_to_unbin = []
    for d in dates_to_check:
        ddo = Date_3D(d, file_inspector=file_inspector)
        if ddo.pipeline_step_completed('plant_reports'):
            continue
        dates_to_unbin.append(d)
    return dates_to_unbin

class BaseLevel(object):
    pass

class Level2(BaseLevel):
    pass

class BaseSensor(object):
    pass

class Sensor3D(BaseSensor):
    def get_processing_log_entry(self):
        self.pr_log = fetch_processing_log_entry(self.date)




class Level2_3D_Stats(Level2, Sensor3D):

    def __init__(self, date, file_inspector=None, date_dir=None, level="season_11_sorghum_yr_2020"):
        self.date = date
        self.fs = file_inspector
        if date_dir is None:
            self.date_dir = date + "/"
        else:
            self.date_dir = date_dir
        self.level = level
        self.get_processing_log_entry()
        self.file_info = {}
        self.get_file_info()
        self.get_plant_reports_summary()

    def get_file_info(self):
        print(f"Getting info for tarballs")
        for f in [f'{self.date}/individual_plants_out/{self.date}_plant_reports.tar',
                  f'{self.date}/individual_plants_out/{self.date}_segmentation_pointclouds.tar']:
            self.file_info[f] = self.fs.file_info(relative_path=f)

    def get_plant_reports_summary(self):
        print(f"Getting contents of plant_reports/")
        self.plant_reports = dict()
        self.plant_reports['exists'] = False
        self.plant_reports['contents'] = self.fs.files(relative_path=f"{self.date}/individual_plants_out/plant_reports/")
        if len(self.plant_reports['contents']) > 1:
            self.plant_reports['exists'] = True


class Date_3D(Sensor3D):

    def __init__(self, date, file_inspector=None, date_dir=None, season="season_11_sorghum_yr_2020"):
        self.date = date
        self.fs = file_inspector
        if date_dir is None:
            self.date_dir = date + "/"
        else:
            self.date_dir = date_dir
        self.season = season

        # marker files are files that mark an important step in the pipeline.
        self.marker_files = {
            'level_1'            : f'{season}/level_1/scanner3DTop/{self.date}/alignment/{self.date}_merged.tar',
            'landmark_selection' : f'{season}/level_1/scanner3DTop/{self.date}/alignment/transfromation.json',
            'level_2'            : f'{season}/level_2/scanner3DTop/{self.date}/individual_plants_out/{self.date}_segmentation_pointclouds.tar',
            'plant_reports'      : f'{season}/level_2/scanner3DTop/{self.date}/individual_plants_out/plant_reports/'
        }


        # marker files are files that mark an important step in the pipeline.
    def pipeline_step_completed(self, step_name):
        return self.fs.file_exists(path=self.marker_files[step_name])


    def get_file_info(self):
        print(f"Getting info for tarballs")
        for f in [f'{self.date}/individual_plants_out/{self.date}_plant_reports.tar',
                  f'{self.date}/individual_plants_out/{self.date}_segmentation_pointclouds.tar']:
            self.file_info[f] = self.fs.file_info(relative_path=f)

    def get_plant_reports_summary(self):
        print(f"Getting contents of plant_reports/")
        self.plant_reports = dict()
        self.plant_reports['exists'] = False
        self.plant_reports['contents'] = self.fs.files(relative_path=f"{self.date}/individual_plants_out/plant_reports/")
        #self.plant_reports['plants'] = 
        if len(self.plant_reports['contents']) > 1:
            self.plant_reports['exists'] = True



