# dashboard
Generates a static website to display diagnostic figures and info for Phytooracle pipeline


## How to run this...

### 3D

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


