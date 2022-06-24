import sys, os, pdb
import ftplib
from webdav3.client import Client
import webdav_credentials
import re

def season_level_sensor_arg_handler(f):
    """
    Essentially, this decorator is a way to implement this...
       my_class_function(self, arg1=self.arg1)
    ... which isn't allowed in python.
    """
    def replace_none_with_self_default(self, **kwargs):
        if 'season' not in kwargs:
            kwargs['season'] = self.season
        if 'level' not in kwargs:
            kwargs['level'] = self.level
        if 'sensor' not in kwargs:
            kwargs['sensor'] = self.sensor
        return f(self, **kwargs)
    return replace_none_with_self_default


class FileInspector(object):

    def __init__(self, season=None, level=None, sensor=None):
        self.season = season
        self.level  = level
        self.sensor = sensor
        pass


    def get_file_list(self, path):
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
        print(files)

    @season_level_sensor_arg_handler
    def dates(self, season=None, level=None, sensor=None, filter_test_dates=True):

        p = self.sensor_path(season=season, level=level, sensor=sensor)
        print(f"Looking for dates in: {p}")
        files = self.get_file_list(p)

#
#        breakpoint()
#        #date = date_dir[0:-1]
#
#        """
#        if date[0] != '2':
#            continue
#        if len(date) != 10:
#            continue
#        """


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


class FTP(FileInspector):
    def __init__(self, server=None, username=None, password=None):
        super().__init__(season, level, sensor)
        ftp = ftplib.FTP('sdf.org', user=username, passwd=password)
        self.server = server
        self.ftp = ftp

