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

class FileInspectorClient(object):
    def human_filesize(self, filesize):
        try:
            _f = int(filesize)
        except TypeError:
            return filesize

        for x in ['B', 'KB', 'MB', 'GB', 'TB']:
            if _f < 1024:
                return f"{_f:.2f}{x}"
            _f = _f / 1024
        return f"{_f:.2f}{x}" # Whatever TB.


class WebDavClient(FileInspectorClient):
    def __init__(self, client_options=None):
        #super().__init__(client_options=client_options)
        if client_options is None:
            self.options = {
             'webdav_hostname': "https://data.cyverse.org/dav/iplant/projects/phytooracle/",
             'webdav_login':    webdav_credentials.webdav_login,
             'webdav_password': webdav_credentials.webdav_password
            }
        self.client = Client(self.options)

    def check_file_exists(self, path):
        print(f"Checking to see if path exists: {path}")
        r = self.client.check(path)
        return r

    def get_file_list(self, path):
        # [1:] because first entry is parent dir...
        try:
            files = self.client.list(path)[1:]
            return files
        except webdav3.exceptions.RemoteResourceNotFound:
            return []

    def get_file_info(self, path):
        print(f"Getting info for {path}")
        try:
            res = self.client.resource(path)
            info = res.info()
            info['size'] = self.human_filesize(info['size'])
            return info
        except webdav3.exceptions.RemoteResourceNotFound:
            return None



class FTPClient(FileInspectorClient):
    def __init__(self, client_options=None):
        pass
        #super().__init__(season, level, sensor)
        #ftp = ftplib.FTP('sdf.org', user=username, passwd=password)
        #self.server = server
        #self.ftp = ftp


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

    def __init__(self, season=None, level='level_0', sensor=None, client=WebDavClient, client_options=None):
        self.season = season
        self.level  = level
        self.sensor = sensor
        self.client = client(client_options=client_options)

    @season_level_sensor_arg_handler
    def sensor_path(self, season=None, level=None, sensor=None):
        return os.path.join(season, level, sensor)

    @season_level_sensor_arg_handler
    def files(self, season=None, level=None, sensor=None, relative_path=None, path=None):
        if path is None:
            spth = self.sensor_path(season=season, level=level, sensor=sensor)
            path = os.path.join(spth, relative_path)
        print(f"Looking for files in: {path}")
        files = self.client.get_file_list(path)
        return files

    @season_level_sensor_arg_handler
    def file_exists(self, season=None, level=None, sensor=None, relative_path=None, path=None):
        if path is None:
            spth = self.sensor_path(season=season, level=level, sensor=sensor)
            path = os.path.join(spth, relative_path)
        return self.client.check_file_exists(path)

    @season_level_sensor_arg_handler
    def date_files(self, season=None, level=None, sensor=None, filter_test_dates=True):
        """
        returns a list : ('path_to_date_file/', 'date')
        return example:
            [
                ['2020-07-28/', '2020-07-28'],
                ['2020-07-30/', '2020-07-30'],
                ['SuperDuper_2020-07-30.tgz', '2020-07-30'],
                ['2020-08-03/', '2020-08-03']
            ]
        """

        pth = self.sensor_path(season=season, level=level, sensor=sensor)
        print(f"Looking for dates in: {pth}")
        all_files = self.client.get_file_list(pth)
        breakpoint()
        p = re.compile(".*(\d\d\d\d-\d\d-\d\d).*")
        #ds is list of tuples: ('path_to_date_file/', 'date')
        ds = [[os.path.join(pth,x), p.match(x).group(1)] for x in all_files if p.match(x)]

        if filter_test_dates:
            p = re.compile(r"^2222-")
            ds = [x for x in ds if not p.match(x[1])]

        return ds

    @season_level_sensor_arg_handler
    def file_info(self, season=None, level=None, sensor=None, relative_path=None, filter_test_dates=True):
        base_path = self.sensor_path(season=season, level=level, sensor=sensor)
        path = os.path.join(base_path, relative_path) 
        info = self.client.get_file_info(path)
#        #res = self.client.resource(path)
#        #info = res.info()
        return info


