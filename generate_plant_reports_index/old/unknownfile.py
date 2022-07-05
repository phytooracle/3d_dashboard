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


class PipelineSensorProgress(object):

    def __init__(season=None, level=None, sensor=None, use_saved_info=True, save_info=True):
        '''
        use_saved_info=True   ->  load dataframe from csv downloaded from cyverse.
        use_saved_info=False  ->  Create dataframe
        '''
        from urllib.error import HTTPError

        saved_info_found = False

        if use_saved_info:
            try:
                scan_df = pd.read_csv(BASE_URL + f"/{season}/{level}/{sensor}/pipeline_sensor_progress.csv")
                saved_info_found = True
            except HTTPError:
                saved_info_found = False


        fs = file_inspector.FileInspector(
                    season=season,
                    level=level,
                    sensor=sensor
        )

    #    def create_df(season, level, sensor, force_overwrite=False):
    #
    #        if not force_overwrite:
    #            if os.path.isfile("outputs/pipeline_data_products.csv") :
    #                scan_df = pd.read_csv("outputs/pipeline_data_products.csv")
    #                return scan_df
    #
    #
    #        dates = []
    #        dataproduct_labels = []
    #        urls = []
    #
    #        # Level 0
    #        # - We confirm the existance of level_0 data just from the date file
    #        level_0_dates = sorted([x[1] for x in fs.date_files(level='level_0')])
    #        dates += level_0_dates
    #        dataproduct_labels += [f"3d_level_0"] * len(level_0_dates)
    #        urls += make_urls_for_dates(level_0_dates, season=season, level='level_0', sensor=sensor)
    #
    #        # Beyond Level 0
    #        # - we have to check certain files to see if certain pipeline steps have completed.
    #        # - we use the Date_3D.pipeline_step_completed() to check 
    #        for l in ['level_1', 'landmark_selection', 'level_2', 'plant_reports']:
    #
    #            d = [x for x in level_0_dates if data_inspector.Date_3D(x, file_inspector=fs).pipeline_step_completed(l)]
    #            dates += d
    #            dataproduct_labels += [f"3d_{l}"] * len(d)
    #            urls += make_urls_for_dates(d, season=season, level=l, sensor=sensor)
    #            #urls += 
    #            # [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}/{x}/
    #
    #        rgb_dates = sorted([x[1] for x in fs.date_files(level='level_0', sensor="stereoTop")])
    #        rgb_labels     = ["rgb_level_0"] * len(rgb_dates)
    #        rgb_urls = [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/level_0/stereoTop/"] * len(rgb_dates)
    #
    #        dates += rgb_dates
    #        dataproduct_labels += rgb_labels
    #        urls += rgb_urls
    #
    #        scan_df = pd.DataFrame(list(zip(dates, dataproduct_labels, urls)), columns=['date', 'level', 'url'])
    #        scan_df.to_csv("outputs/pipeline_data_products.csv")
    #        return scan_df


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
        if len(self.plant_reports['contents']) > 1:
            self.plant_reports['exists'] = True



