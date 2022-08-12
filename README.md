# dashboard
Generates a static website to display diagnostic figures and info for Phytooracle pipeline


## How to run this interactively on hpc for Season 11.

### First time...
```
git clone git@github.com:phytooracle/3d_dashboard.git
salloc --nodes=1 --mem-per-cpu=4GB --ntasks=1 --time=16:00:00 --job-name=dashboard  --account=dukepauli --partition=high_priority --qos user_qos_dukepauli
module load anaconda/2022.05
conda create --name dashboard
conda activate dashboard
conda install pip
pip install python-dotenv
pip install numpy
pip install pandas
pip install matplotlib
pip install pyyaml
```

### Then...
```
cd 3d_dashboard
git checkout s11
cd generate_plant_reports_index
```

The first step is to run
`generate_plant_reports_index/generate_level_2_3d_homepage.py`.  This scrapes
several sources (google sheets, and cyverse).  It is very expensive (in time)
to walk around the cyverse data store, so this can take a while.  The results
are stored in `date_data_objects.pickle`, so make sure that `USE_PICKLE=False`
in `generate_level_2_3d_homepage.py`.  Setting it to `TRUE` is useful for
developing the output (generation of html, etc) so that you don't have to keep
scraping cyverse.

```
generate_level_2_3d_homepage.py
```


