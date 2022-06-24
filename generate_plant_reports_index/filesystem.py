import sys, os
from webdav3.client import Client
import webdav_credentials
options = {
 'webdav_hostname': "https://data.cyverse.org/dav/iplant/projects/phytooracle/",
 'webdav_login':    webdav_credentials.webdav_login,
 'webdav_password': webdav_credentials.webdav_password
}
client = Client(options)

sensor_path = os.path.join("season_11_sorghum_yr_2020",
                           "level_2",
                           "scanner3DTop")
level_2_files = client.list(sensor_path)[1:]   # [1:] because first entry is parent dir.

status_report_dict = { "report_tars" : {}, "report_dirs" : {} }

for date_dir in level_2_files:

    # First, do some pretty lazy error checking...

    date = date_dir[0:-1]
    if date[0] != '2':
        continue
    if len(date) != 10:
        continue

    print(f"Looking in {date}...")

    plant_reports_tar_path = os.path.join(sensor_path,
                                          date_dir,
                                          "individual_plants_out",
                                          f"{date}_plant_reports.tar",
                                     )
    plant_reports_dir_path = os.path.join(sensor_path,
                                          date_dir,
                                          "individual_plants_out",
                                          f"plant_reports",
                                     )
    try:
        tar_scan = client.list(plant_reports_tar_path)
        status_report_dict['report_tars'][date] = tar_scan[0]
    except webdav3.exceptions.RemoteResourceNotFound:
        # Didn't find it
        print(f"    ... no tar file")
        pass

    try:
        dir_scan = client.list(plant_reports_dir_path)
        status_report_dict['report_dirs'][date] = tar_scan[0]
    except webdav3.exceptions.RemoteResourceNotFound:
        # Didn't find it
        print(f"    ... no plant_reports dir")
        pass

