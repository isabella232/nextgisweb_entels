# -*- coding: utf-8 -*-
import geojson
from osgeo import ogr, osr
from nextgisweb.geometry import geom_from_wkb, geom_from_wkt
from nextgisweb.postgis import PostgisLayer

OSM_RESOLUTIONS = [
    1.40625,
    0.703125,
    0.3515625,
    0.17578125,
    0.087890625,
    0.0439453125,
    0.02197265625,
    0.010986328125,
    0.0054931640625,
    0.00274658203125,
    0.00137329101562,
    0.000686645507812,
    0.000343322753906,
    0.000171661376953,
    8.58306884766e-05,
    4.29153442383e-05,
    2.14576721191e-05,
    1.07288360596e-05,
    5.36441802979e-06
]


class ComplexEncoder(geojson.GeoJSONEncoder):
    def default(self, obj):
        try:
            return geojson.GeoJSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def geometry_transform(geometry, source_srs, target_srs):
    source_osr = osr.SpatialReference()
    target_osr = osr.SpatialReference()

    source_osr.ImportFromEPSG(source_srs)
    target_osr.ImportFromEPSG(target_srs)

    if not source_osr.IsSame(target_osr):
        transform = osr.CoordinateTransformation(source_osr, target_osr)
        geom = ogr.CreateGeometryFromWkb(geometry.to_wkb())
        geom.Transform(transform)
        geometry = geom_from_wkb(geom.ExportToWkb())

    return geometry


def calculate_bbox(zoom, center, tolerance):
    ptolerance = OSM_RESOLUTIONS[zoom]*tolerance
    x = center[0]
    y = center[1]
    xmin = x - ptolerance
    ymin = y - ptolerance
    xmax = x + ptolerance
    ymax = y + ptolerance
    return [xmin, ymin, xmax, ymax]


def tabfqn(layer):
    return '"{layer.schema}"."{layer.table}"'.\
        format(layer=layer)


def stripguid(guid):
    return str(guid).translate(None, "{}")
