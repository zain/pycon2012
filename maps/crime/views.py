from crime.models import Crime
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse
from django.shortcuts import render
import json

def crime_map(request):
    return render(request, 'crime.html')

def crime_list(request):
    coords = request.GET['bbox'].split(',')
    bbox = Polygon.from_bbox(coords)
    
    crimes = Crime.objects.filter(pt__within=bbox)
    
    geojson_dict = {
        "type": "FeatureCollection",
        "features": [crime_to_geojson(crime) for crime in crimes[::4]]
    }
    
    return HttpResponse(json.dumps(geojson_dict), content_type='application/json')

def crime_to_geojson(crime):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [crime.pt.x, crime.pt.y]
        },
        "properties": {
            "description": crime.description
        }
    }
