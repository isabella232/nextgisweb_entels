# -*- coding: utf-8 -*-

from datetime import datetime

import geojson
from nextgisweb.feature_layer import IFeatureLayer
from nextgisweb.geometry import box
from nextgisweb.models import DBSession
from nextgisweb.pyramid.util import viewargs
from nextgisweb.resource import DataScope
from nextgisweb.vector_layer import VectorLayer
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from sqlalchemy.sql.operators import ilike_op

from GeoJsonFeatureList import GeoJsonFeatureList
from helpers import (
    geometry_transform,
    ComplexEncoder
)

PD_READ = DataScope.read
PD_WRITE = DataScope.write


@viewargs(context=IFeatureLayer)
def store(request):
    request.resource_permission(PD_READ)
    query = request.context.feature_query()

    features = GeoJsonFeatureList()

    try:
        filters = []
        for field in request.POST:
            if not request.POST[field]:
                continue
            filters.append((field, ilike_op, '%' + request.POST[field] + '%'))
        query.filter(filters)
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
