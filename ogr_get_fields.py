"""Get field names from a shapefile using OGR"""
from osgeo import ogr
from pprint import pprint

source = ogr.Open("data/anne_arundel_county/S_FIRM_PAN.shp")

layer = source.GetLayer()

schema = []

ldefn = layer.GetLayerDefn()

for n in range(ldefn.GetFieldCount()):
    fdefn = ldefn.GetFieldDefn(n)
    schema.append(fdefn.name)

pprint(schema)
