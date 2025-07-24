#!/usr/bin/env python
# coding: utf-8
"""Examples of working with GeoPandas"""

# Reading and writing vector data with GeoPandas
import geopandas as gpd
import os

data_folder = r'data/Natural_Earth_quick_start'

# Read the ne_10m_admin_0_boundary_lines_land.shp and display the first 5 rows
df = gpd.read_file(os.path.join(data_folder, '10m_cultural/ne_10m_admin_0_boundary_lines_land.shp'))
df.head()

# Show the geometry type
print(df.geom_type.head())

# Show the coordinate system
print(df.crs)

# Convert the dataframe to json
df.to_json()

# Write the dataframe to a json file
df.to_file(driver='GeoJSON', filename=r'data/world.geojson')
