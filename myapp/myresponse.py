import requests
import json
from math import sin, cos, sqrt, atan2, radians
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import CollectionLines, Person
from rbackend import settings

def DiscoJsonResponse(x):
    jsonResponse = JsonResponse(x)
    jsonResponse["Access-Control-Allow-Origin"] = "*"
    # jsonResponse["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    # jsonResponse["Access-Control-Max-Age"] = "1000"
    # jsonResponse["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return jsonResponse


def SuzdalShortJson(qeurySet):
    jsonResponse = serializers.serialize('json', qeurySet)
    mi_response = HttpResponse(jsonResponse, content_type="application/json")
    mi_response["Access-Control-Allow-Origin"] = "*"
    return mi_response

def UserLoginCorrectry(rq):
    try:
        user = Person.objects.get(id=rq.POST.get('user_id'), uid=rq.POST.get('uid'))
        print("User login correctly "+user.uid)
        return True
    except:
        print("ERROR User DON T login")
        return False
    

def SetLocateAddress(lineModel):
    address    = lineModel.country+'+'+lineModel.region+'+'+lineModel.city
    address    = address.strip().lower().replace(' ', '+').replace('++', '+')
    GOOGLE_KEY = 'AIzaSyBDKhqes2S-VlNPQmOi70qpJMkaCfhzyt4'
    url_path   = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+GOOGLE_KEY
    try:
        result        = requests.get(url_path)
        parsed        = json.loads(result.content)
        first         = parsed['results'][0]
        second        = first['geometry']['location']
        lineModel.lat = second['lat']
        lineModel.lng = second['lng']
        lineModel.save()
    except:
        pass


def OrderingPackagesByTruck(collection_id, track_num, user_id):
    # __gt, __gte, __lt, ___lte
    person = Person.objects.get(id=user_id)                                                                         
    CollectionLines.objects.filter(colection_id=collection_id, truck=track_num).update(by_order=None, meters=None)
    
    new_order_by = 0
    list_lines_all = CollectionLines.objects.filter(colection_id=collection_id, truck=track_num)                                                
    for l in list_lines_all:
        lines_without_order = CollectionLines.objects.filter(colection_id=collection_id, truck=track_num, by_order=None)                        
        # guardo metros comparando con localizacion USER
        for lin_without in lines_without_order:
            mi_location = { "lat": person.lat, "lng": person.lng }
            try:
                exist_location = CollectionLines.objects.filter(colection_id=collection_id, truck=track_num, by_order__gt=0).order_by("-by_order").first()
                mi_location = { "lat": exist_location.lat, "lng": exist_location.lng }
            except:
                pass
            lin_without.meters = measureDistance(mi_location, lin_without)
            lin_without.save()
        # busco la ubicacion mas cercana y le pongo orden 1
        try:
            nearest_order = CollectionLines.objects.filter(colection_id=collection_id, truck=track_num, by_order=None).order_by("meters").first()
            new_order_by += 1
            CollectionLines.objects.filter(id=nearest_order.id).update(by_order=new_order_by)
        except:
            pass    



def measureDistance(mi_location, line_location):
    R = 6373.0
    lat1 = radians(float(mi_location["lat"]))
    lon1 = radians(float(mi_location["lng"]))
    lat2 = radians(float(line_location.lat))
    lon2 = radians(float(line_location.lng))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = int( R * c * 1000)
    return distance


def get_current_file_directory(rq):
    if '127.0' in  rq.build_absolute_uri():
        return 'static/'
    else:
        return 'rbackend/static/'
    

def RecalculateThisRoute(collectionId, trackNum):
    firstLine = CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum).exclude(by_order=None).order_by("by_order").first()
    CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum).exclude(id=firstLine.id).update(by_order=None, meters=None)
    new_order_by = firstLine.by_order

    list_lines_all = CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum)                                                
    for l in list_lines_all:
        lines_without_order = CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum, by_order=None)                        
        # guardo metros comparando con localizacion USER
        for lin_without in lines_without_order:
            mi_location = { "lat": firstLine.lat, "lng": firstLine.lng }
            try:
                exist_location = CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum, by_order__gt=0).order_by("-by_order").first()
                mi_location = { "lat": exist_location.lat, "lng": exist_location.lng }
            except:
                pass
            lin_without.meters = measureDistance(mi_location, lin_without)
            lin_without.save()
        # busco la ubicacion mas cercana y le pongo orden 1
        try:
            nearest_order = CollectionLines.objects.filter(colection_id=collectionId, truck=trackNum, by_order=None).order_by("meters").first()
            new_order_by += 1
            CollectionLines.objects.filter(id=nearest_order.id).update(by_order=new_order_by)
        except:
            pass 