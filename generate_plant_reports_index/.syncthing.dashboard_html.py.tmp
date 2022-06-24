import numpy as np

def plant_data_row(plant_data, BASE_URL, conf):

    return f"""
    <tr>
    <td>
        <a href='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/index.html'>{plant_data.name}</a><br>
        <small>
<pre>
{plant_data[['treatment', 'n_obs', 'double_lettuce']]}
<a href='http://www.google.com/maps/place/{plant_data['mean_lat']},{plant_data['mean_lon']}/@{plant_data['mean_lat']},{plant_data['mean_lon']},20z/data=!3m1!1e3'>{plant_data['mean_lat']},{plant_data['mean_lon']}</a>
</pre>
        </small>
        
    </td>
    <td><a href='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/index.html'><img style="max-width: 300; max-height: 300px" src='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/combined_heatmap.png'></a></td>
    <td><a href='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/index.html'><img style="max-width: 300; max-height: 300px" src='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/combined_multiway_registered.gif'></a><input type="checkbox" name="crop" onchange="do_crop_checkbox()"/></td>
    <td><a href='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/index.html'><img style="max-width: 300; max-height: 300px" src='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/combined_multiway_registered_soil_segmentation.gif'></a><input type="checkbox" name="ground" onchange="do_ground_checkbox()" /></td>
    <td><a href='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/index.html'><img style="max-width: 300; max-height: 300px" src='{BASE_URL}/{conf.args.date}/plant_reports/{plant_data.name}/combined_multiway_registered_soil_segmentation_cluster.gif'></a><input type="checkbox" name="segmentation" onchange="do_segmentation_checkbox()" /></td>
    """






def create_random_plants_page(plants, conf, n=50, filename="random.html"):

    html = f"""
        <html>
        <body>
        <h1>{n} Random Valid Plants : {conf.args.date}</h1>
        <table>

        <tr><th></th><th></th><th>Geocorection<th>Soil<br>Identification</th><th>Plant<br>Segmentation</th></tr>
    """

    if len(plants) < n:
        n = len(plants)

    # Because random.choice doesn't like multidimensional things,
    # we have to do it this way...
    indices = np.random.choice(len(plants), n, replace=False)
    for i in indices:
        plant_data = plants[i]
        html += plant_data_row(plant_data, conf.BASE_URL, conf)

    html += """
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td><center><label id="cropCount">Flagged: 0</label></center></td>
            <td><center><label id="groundCount">Flagged: 0</label></center></td>
            <td><center><label id="segmentationCount">Flagged: 0</label></center></td>
        </tr>
        </table>
<p>
		<script>
			function do_crop_checkbox() {
			  let total = document.querySelectorAll('input[name="crop"]:checked').length;
			  let perc = total / document.querySelectorAll('input[name="crop"]').length * 100;
			  document.getElementById("cropCount").innerHTML = "Flags: " + total + " (" + perc.toFixed(2) + "%)";
			}
			function do_ground_checkbox() {
			  let total = document.querySelectorAll('input[name="ground"]:checked').length;
			  let perc = total / document.querySelectorAll('input[name="ground"]').length * 100;
			  document.getElementById("groundCount").innerHTML = "Flags: " + total + " (" + perc.toFixed(2) + "%)";
			}
			function do_segmentation_checkbox() {
			  let total = document.querySelectorAll('input[name="segmentation"]:checked').length;
			  let perc = total / document.querySelectorAll('input[name="segmentation"]').length * 100;
			  document.getElementById("segmentationCount").innerHTML = "Flags: " + total + " (" + perc.toFixed(2) + "%)";
			}
		</script>
<p>
		<hr>
		<p><a href="index.html">Scan Home</a></p>
        <br>
        <hr>
        <p>
		</body>
        </html>
    """

    with open(filename, "w") as html_file:
        html_file.write(html);
