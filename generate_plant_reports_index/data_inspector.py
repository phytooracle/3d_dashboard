import pandas as pd

def fetch_processing_log_entry(date,
                     sheet_id = "19QS5MpVzw7gv-SPHe1HQO7iJ2x6njFEMskNMCjZF84k",
                     sheet_name = "Season_11"
):
    print("GETTING SHEET!")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    return df[ df['Scan Date'] == date ]


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

    def get_file_info(self):
        for f in [f'{self.date}/individual_plants_out/{self.date}_plant_reports.tar',
                  f'{self.date}/individual_plants_out/{self.date}_segmentation_pointclouds.tar']:
            self.file_info[f] = self.fs.file_info(f)
