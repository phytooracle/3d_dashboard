import pandas as pd
from urllib.error import HTTPError  # For failed pd.read_csv (404 errors)

#import webdav_credentials
import file_inspector
#import data_inspector

BASE_URL = f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle"

class PipelineSensorProgress(object):
    """
    This is a base class.  Use a class that inherits from this class.
    i.e. PipelineScanner3DTopProgress()
    """

    def __init__(self, season=None, sensor=None, use_saved_info=True, save_info=True):
        '''
        use_saved_info=True   ->  load dataframe from csv downloaded from cyverse.
        use_saved_info=False  ->  Create dataframe
        '''
        saved_info_found = False

        if use_saved_info:
            try:
                self.scan_df = pd.read_csv(BASE_URL + f"/{season}/level_0/{sensor}/pipeline_sensor_progress.csv")
                saved_info_found = True
            except HTTPError:
                saved_info_found = False

        self.fs = file_inspector.FileInspector(
                    season=season,
                    sensor=sensor
        )

        if (not use_saved_info) or (not saved_info_found):
            self.scrape_info_and_build_df()

    def make_urls_for_dates(dates, season=None, level=None, sensor=None):
        pass

    def scrape_info_and_build_df(self):
        dates = []
        dataproduct_labels = []
        urls = []

        breakpoint()
        # Level 0
        # - We confirm the existance of level_0 data just from the date file
        level_0_dates = sorted([x[1] for x in self.fs.date_files(level='level_0')])
        dates += level_0_dates
        dataproduct_labels += [f"3d_level_0"] * len(level_0_dates)
        urls += make_urls_for_dates(level_0_dates, season=self.season, level='level_0', sensor=self.sensor)

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


class PipelineScanner3DTopProgress(PipelineSensorProgress):
    def __init__(self, season=None, use_saved_info=True, save_info=True):
        self.season = season
        super().__init__(sensor='Scanner3DTop', season=season)

    def make_urls_for_dates(dates, season=None, level=None, sensor=None):
        if level == 'plant_reports':
            return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/level_2/{sensor}/{x}/individual_plants_out/plant_reports/index.html" for x in dates]
        if level == 'level_0':
            return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}" for x in dates]
        if level == 'landmark_selection':
            level = 'level_2'

        return [f"https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/{season}/{level}/{sensor}/{x}/" for x in dates]
