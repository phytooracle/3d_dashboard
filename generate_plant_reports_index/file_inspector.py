import sys, os, pdb
import ftplib
import webdav3
from webdav3.client import Client
import webdav_credentials
import re

"""
Example usage:

import file_inspector
fs = file_inspector.WebDav(
            season="season_11_sorghum_yr_2020",
            level="level_2",
            sensor="scanner3DTop"
     )
fs.date_files()

"""

def season_level_sensor_arg_handler(f):
    """
    Essentially, this decorator is a way to implement this...
       my_class_function(self, arg1=self.arg1)
    ... which isn't allowed in python.
    """
    def replace_none_with_self_default(self, *args, **kwargs):
        if 'season' not in kwargs:
            kwargs['season'] = self.season
        if 'level' not in kwargs:
            kwargs['level'] = self.level
        if 'sensor' not in kwargs:
            kwargs['sensor'] = self.sensor
        #breakpoint()
        return f(self, *args, **kwargs)
    return replace_none_with_self_default


class FileInspector(object):

    def __init__(self, season=None, level=None, sensor=None):
        self.season = season
        self.level  = level
        self.sensor = sensor
        pass


    def get_file_list(self, path):
        pass

    def get_file_info(self, path):
        pass

    def connect(self):
        pass

    @season_level_sensor_arg_handler
    def sensor_path(self, season=None, level=None, sensor=None):
        return os.path.join(season, level, sensor)

    @season_level_sensor_arg_handler
    def files(self, season=None, level=None, sensor=None):

        p = self.sensor_path(season=season, level=level, sensor=sensor)
        print(f"Looking for files in: {p}")
        files = self.get_file_list(p)
        return files

    @season_level_sensor_arg_handler
    def date_files(self, season=None, level=None, sensor=None, filter_test_dates=True):
        """
        returns a list of tuples: ('path_to_date_file/', 'date')
        return example:
            [
                ('2020-07-28/', '2020-07-28'),
                ('2020-07-30/', '2020-07-30'),
                ('SuperDuper_2020-07-30.tgz', '2020-07-30'),
                ('2020-08-03/', '2020-08-03')
            ]
        """

        pth = self.sensor_path(season=season, level=level, sensor=sensor)
        print(f"Looking for dates in: {pth}")
        all_files = self.get_file_list(pth)
        p = re.compile(".*(\d\d\d\d-\d\d-\d\d).*\/")
        #ds is list of tuples: ('path_to_date_file/', 'date')
        ds = [(os.path.join(pth,x), p.match(x).group(1)) for x in all_files if p.match(x)]

        if filter_test_dates:
            p = re.compile(r"^2222-")
            ds = [x for x in ds if not p.match(x[1])]

        return ds

    @season_level_sensor_arg_handler
    def file_info(self, relative_path, season=None, level=None, sensor=None, filter_test_dates=True):
        base_path = self.sensor_path(season=season, level=level, sensor=sensor)
        path = os.path.join(base_path, relative_path) 
        info = self.get_file_info(path)
#        #res = self.client.resource(path)
#        #info = res.info()
        return info


class WebDav(FileInspector):
    def __init__(self, season=None, level=None, sensor=None, webdav_options=None):
        super().__init__(season, level, sensor)
        if webdav_options is None:
            self.options = {
             'webdav_hostname': "https://data.cyverse.org/dav/iplant/projects/phytooracle/",
             'webdav_login':    webdav_credentials.webdav_login,
             'webdav_password': webdav_credentials.webdav_password
            }
        self.client = Client(self.options)

    def get_file_list(self, path):
        # [1:] because first entry is parent dir...
        files = self.client.list(path)[1:]
        return files

    def get_file_info(self, path):
        print(f"Getting info for {path}")
        try:
            res = self.client.resource(path)
            info = res.info()
            return info
        except webdav3.exceptions.RemoteResourceNotFound:
            return None



class FTP(FileInspector):
    def __init__(self, server=None, username=None, password=None):
        super().__init__(season, level, sensor)
        ftp = ftplib.FTP('sdf.org', user=username, passwd=password)
        self.server = server
        self.ftp = ftp

