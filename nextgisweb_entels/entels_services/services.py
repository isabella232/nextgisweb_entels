# -*- coding: utf-8 -*-

import json
import geojson

from datetime import datetime

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response

from nextgisweb.feature_layer import IFeatureLayer
from nextgisweb.resource import DataScope
from nextgisweb.pyramid.util import viewargs
from nextgisweb.models import DBSession
from nextgisweb.geometry import box
from nextgisweb.postgis import PostgisLayer
from nextgisweb.vector_layer import VectorLayer

from GeoJsonFeatureList import GeoJsonFeatureList

from helpers import (
    calculate_bbox,
    geometry_transform,
    geom_from_wkt,
    stripguid,
    ComplexEncoder
)

PD_READ = DataScope.read
PD_WRITE = DataScope.write


@viewargs(context=IFeatureLayer)
def store(request):
    request.resource_permission(PD_READ)
    query = request.context.feature_query()

    if not ('geometry' in request.GET or 'guids' in request.GET):
        raise HTTPBadRequest()

    features = GeoJsonFeatureList()
    try:
        if 'guids' in request.GET:
            guids = str(request.GET['guids']).lower()
            if guids == 'true':
                query.fields('uniq_uid')
        if 'geometry' in request.GET:
            geometry = str(request.GET['geometry']).lower()
            if geometry == 'true': query.geom()
        for f in query():
            if f.geom:
                f._geom = geometry_transform(f.geom, f.layer.srs_id, 4326)
            features.append(f)
    except Exception as e:
        raise HTTPBadRequest(e.message)

    return Response(geojson.dumps(features, cls=ComplexEncoder), content_type='application/json')


def geocollection(request):
    try:
        date = str(request.GET.get('datetime', datetime.now()))
        if 'layers' in request.GET:
            qlayers = map(int, request.GET['layers'].split(','))
            print qlayers
            layers = DBSession.query(VectorLayer)\
                .filter(VectorLayer.id.in_(qlayers))\
                .all()
        else:
            layers = DBSession.query(VectorLayer)\
                .all()
        layers = filter(lambda layer: layer.has_permission(PD_READ, request.user), layers)
        print layers
    except Exception as e:
        raise HTTPBadRequest(e.message)

    features = GeoJsonFeatureList()

    # Запрос коллекции GeoJSON объектов, попадающих в заданную область видимости
    if 'bbox' in request.GET:
        try:
            bbox = map(float, request.GET['bbox'].split(','))
            print bbox
            geometry = box(*bbox, srid=3857)
            for layer in layers:
                query = layer.feature_query()
                query.geom()
                query.intersects(geometry)
                for feature in query():
                    print feature
                    feature.fields['__layer__'] = feature.layer.id
                    features.append(feature)
        except Exception as e:
            print e
            raise HTTPBadRequest(e.message)
    else:
        raise HTTPBadRequest()
    print len(features)

    for f in features:
        f._geom = geometry_transform(f.geom, f.layer.srs_id, 4326)
    result = geojson.dumps(features, cls=ComplexEncoder)

    return Response(result, content_type='application/json')
