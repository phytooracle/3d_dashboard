import sys
import argparse


class Config(object):

    MIN_OBS = 5
    BASE_URL = "https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/dashboard"

    data_category_strings = {
            'good_data' : "Valid useable data",
            'double_lettuce' : "Double lettuces",
            'low_observations' : "Low frequency plants*",
    }

    def __init__(self, season=10):

        try:
            import dotenv
            env_file = dotenv.find_dotenv()
            dotenv.load_dotenv(env_file)
            parsed_dotenv = dotenv.dotenv_values()
            phytooracle_data_library_path  = parsed_dotenv["phytooracle_data_library_path"]
            # settings['result'] = parsed_dotenv["results_dir"]
        except ModuleNotFoundError:
            print("[FATAL]")
            print("You need to install dotenv")
            print("pip install python-dotenv")
            sys.exit(0)
        except KeyError:
            print("[FATAL]")
            print("We didn't find (or we didn't find what we expected in) your .env file")
            print("Please see README.md regarding .env")
            sys.exit(0)

       
        # Load phytooracle_data package
        try:
            sys.path.append(phytooracle_data_library_path)
            import phytooracle_data.scanner3dTop as scanner3dTop
            import phytooracle_data.stereoTop as stereoTop
            import phytooracle_data.rgb as rgb
        except ModuleNotFoundError:
            print("[FATAL]")
            print(phytooracle_data_library_path)
            print("You need to install phytooracle_data (and tell me where it is with .env)")
            print("https://github.com/phytooracle/phytooracle_data")
            sys.exit(0)

        self.handle_command_line_aruments()
    
        #self.ortho     = stereoTop.Ortho(season=self.args.season)
        #self.three_dee = scanner3dTop.Scanner3dTop(season=self.args.season)
        self.rgb = rgb.RGB_Data(season=self.args.season)


    def handle_command_line_aruments(self):
        parser = argparse.ArgumentParser(
            description='GUI for 3d manual goecorrection.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-d',
                            '--date',
                            help='The 3D scan date for processing',
                            default = "2020-01-22_50pct_clustered_segmented",
                            metavar='date',
                            required=False)

        parser.add_argument('-S',
                            '--season',
                            help='The season (e.g. 10)',
                            metavar='season',
                            default=10,
                            type=int,
                            required=False)

        self.args = parser.parse_args()
