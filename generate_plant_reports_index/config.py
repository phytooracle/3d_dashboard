import sys
import argparse

#import phytooracle_data.rgb as rgb

class Config(object):

    MIN_OBS = 5
    BASE_URL = "https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/dashboard"

    data_category_strings = {
            'good_data' : "Valid useable data",
            'double_lettuce' : "Double lettuces",
            'low_observations' : "Low frequency plants*",
    }

    def __init__(self, season=10):
        pass
        #self.handle_command_line_aruments()
        #self.rgb = rgb.RGB_Data(season=season)

    def handle_command_line_aruments(self):
        parser = argparse.ArgumentParser(
            description='GUI for 3d manual goecorrection.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-d',
                            '--date',
                            help='The 3D scan date for processing',
                            default = "2020-07-08",
                            metavar='date',
                            required=False)

        parser.add_argument('-S',
                            '--season',
                            help='The season (e.g. 10)',
                            metavar='season',
                            default=11,
                            type=int,
                            required=False)

        self.args = parser.parse_args()
