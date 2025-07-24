"""Iterate over features using OGR"""
from osgeo import ogr, osr
import os

shapefile = r"data/anne_arundel_county/S_FIRM_PAN.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")

data_source = ogr.Open(shapefile, 0)
layer = data_source.GetLayer()

for feature in layer:
    print(feature.GetField("FIRM_PAN"))
    geom = feature.GetGeometryRef()
    print(f"\t{geom.Centroid().ExportToWkt()}")

# Feature count
feature_count = layer.GetFeatureCount()
print("-" * 50)
print(f"Number of features in {os.path.basename(shapefile)}: {feature_count}")

# CRS
print("-" * 50)
spatial_reference = layer.GetSpatialRef()
print(spatial_reference)
