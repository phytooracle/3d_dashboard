import os
from pathlib import Path
import altair as alt
import altair_ally as aly
import pandas as pd

def scatter_matrix(df, save_path):
    #tooltip_columns = ['ply_file'] + columns_of_interest   # altair wants this wierd format
    chart = alt.Chart(downsample_stats_df).mark_circle().encode(
                alt.X(alt.repeat("column"), type='quantitative'),
                alt.Y(alt.repeat("row"),    type='quantitative'),
                color='Origin:N',
                #href='growth_curve_plot_url:N',
                #tooltip=tooltip_columns
            ).properties(
                width=150,
                height=150
            ).repeat(
                row=columns_of_interest,
                column=list(reversed(columns_of_interest))
            ).interactive()
    plot_filename = f"altair-pairplot-downsample_stats"
    chart.save(os.path.join(f"{plot_filename}.html"))



def generate_eda(df, df_name, path):
    output_path = os.path.join(path, df_name)
    Path(output_path).mkdir(parents=True, exist_ok=True)

    chart = aly.heatmap(df)
    #chart.encoding.tooltip = alt.Tooltip(["plant_name", "amplitude_persistence_image_2"])
    #chart.encoding.tooltip = alt.Tooltip("plant_name:N")
    #chart.save('foo.html')
    #chart.encoding.tooltip = alt.Tooltip("value:Q")
    chart.save(os.path.join(output_path, f"heatmap.html"))

    chart = aly.corr(df)
    chart.save(os.path.join(output_path, f"corr.html"))

    chart = aly.dist(df)
    chart.save(os.path.join(output_path, f"dist.html"))

