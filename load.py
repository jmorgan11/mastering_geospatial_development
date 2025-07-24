"""
Read the shapefiles and tables from a zip file.
Create a table in the database for each shapefile.
Load the contents of that shapefile into the database table.

Author: Jesse Morgan
Date: 7/3/2025
"""

import os
import zipfile
import psycopg2
from sqlalchemy import create_engine
import geopandas_example as gpd

# Connect to the database
# TODO: Store credentials in a file
# TODO: Create the Database if it doesn't exists

user = input("Enter user name: ")
password = input("Enter password: ")
host = "localhost"
port = 5432
database = "24003C"

conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)

# TODO: Query the user for the zip file
ZIP_FILE = "anne_arundel_county.zip"

# Get a list of the names in the zip file
name_list = zipfile.ZipFile(ZIP_FILE).namelist()

# Create a list of shapefiles in the zip file
shapefiles = [name for name in name_list if name.lower().endswith(".shp")]

# Create a list of tables in the zip file if the table name doesn't have an associated shapefile name
tables = [name for name in name_list if name.lower().endswith(".dbf") and name[:-4] + ".shp" not in shapefiles]

# Load the shapefiles into the database
for shapefile in shapefiles:
    gdf = gpd.read_file(os.path.join("anne_arundel_county", shapefile))
    gdf.columns = gdf.columns.str.lower()
    gdf.to_postgis(name=shapefile[:-4].lower(), con=engine, schema="public")

# Load the tables into the database
for table in tables:
    gdf = gpd.read_file(os.path.join("anne_arundel_county", table))
    gdf.columns = gdf.columns.str.lower()
    gdf.to_sql(table[:-4].lower(), con=engine, schema="public")
