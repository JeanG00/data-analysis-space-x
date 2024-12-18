from flask import Blueprint, render_template
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from markupsafe import Markup
from src.utils import version, util

bp = Blueprint('home', __name__)

v = version.get_version()


@bp.route('/', methods=['GET'])
def indx():
    """Landing page."""
    welcome = "Hello World!"
    return render_template(
        'index.html',
        version=v,
        content=Markup(welcome))


@bp.route('/folium', methods=['GET'])
def map():
    """Simple example of a fullscreen map."""
    df = pd.read_csv("assets/spacex_launch_geo.csv")
    launch_sites_df = df[['Launch Site', 'Lat', 'Long', 'class']].groupby(
        ['Launch Site'], as_index=False).first()
    launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
    nasa_coordinate = [29.559684888503615, -95.0830971930759]
    m = folium.Map(location=nasa_coordinate, zoom_start=5)
    for idx, record in launch_sites_df.iterrows():
        circle = folium.Circle(
            location=[
                record['Lat'],
                record['Long']],
            radius=1000,
            color='#000000',
            fill=True)
        marker = folium.Marker(
            location=[
                record['Lat'], record['Long']], icon=DivIcon(
                icon_size=(
                    20, 20), icon_anchor=(
                    0, 0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' %
                record['Launch Site']))
        m.add_child(circle)
        m.add_child(marker)

    def marker_color_by_class(x):
        if x == 0:
            return 'red'
        else:
            return 'green'
    df['marker_color'] = df['class'].apply(marker_color_by_class)
    marker_cluster = MarkerCluster()
    # Add marker_cluster to current site_map
    m.add_child(marker_cluster)
    for index, record in df.iterrows():
        # Create and add a Marker cluster to the site map
        icon = folium.Icon(color='white', icon_color=record['marker_color'])
        popup = folium.Popup(html=f"{record['Lat']},{record['Long']}")
        marker = folium.Marker(
            location=[
                record['Lat'],
                record['Long']],
            icon=icon,
            popup=popup)
        marker_cluster.add_child(marker)

    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = MousePosition(
        position='topright',
        separator=' Long: ',
        empty_string='NaN',
        lng_first=False,
        num_digits=20,
        prefix='Lat:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    )
    m.add_child(mouse_position)
    coordinates = [
        # [28.56230197,-80.57735648]
        [28.56230, -80.57735],  # launch site
        [28.56272, -80.56787],  # costline
    ]
    # distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
    distance_coastline = util.calculate_distance(
        coordinates[0][0],
        coordinates[0][1],
        coordinates[1][0],
        coordinates[1][1])
    distance_marker = folium.Marker(
        coordinates[1],
        icon=DivIcon(
            icon_size=(
                20,
                20),
            icon_anchor=(
                0,
                0),
            html='<div style="font-size: 12; color:#d35400;">Nearst costline<b>%s</b></div>' %
            "{:10.2f} KM".format(distance_coastline),
        ))
    m.add_child(distance_marker)
    # Create a `folium.PolyLine` object using the coastline coordinates and
    # launch site coordinate
    lines = folium.PolyLine(locations=coordinates, weight=1)
    m.add_child(lines)
    coordinates_to_city = [
        # [28.56230197,-80.57735648]
        [28.56230, -80.57735],  # launch site
        [28.54627, -81.33147],  # Orlando
    ]

    distance_city = util.calculate_distance(
        coordinates_to_city[0][0],
        coordinates_to_city[0][1],
        coordinates_to_city[1][0],
        coordinates_to_city[1][1])
    distance_marker = folium.Marker(
        coordinates_to_city[1],
        icon=DivIcon(
            icon_size=(
                20,
                20),
            icon_anchor=(
                0,
                0),
            html='<div style="font-size: 12; color:#d35400;">Nearst city<b>%s</b></div>' %
            "{:10.2f} KM".format(distance_city),
        ))
    m.add_child(distance_marker)
    lines = folium.PolyLine(locations=coordinates_to_city, weight=1)
    m.add_child(lines)
    return m.get_root().render()
