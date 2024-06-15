from django.shortcuts import render
from django.http import HttpResponse
from ..myresponse import SetLocateAddress, DiscoJsonResponse
from ..models import Person, LastVisit
import datetime

class PersonController:
    # /userLogin -> email, uid, password

    def userLogin(request):
        PERSON_TUPLE             = Person.objects.get_or_create(email=request.GET.get('email'), uid=request.GET.get('uid'))
        if PERSON_TUPLE[0].password == None:
           PERSON_TUPLE[0].password = request.GET.get('password')
           PERSON_TUPLE[0].lat      = '43.3099809'
           PERSON_TUPLE[0].lng      = '-3.853442199999999'
           PERSON_TUPLE[0].country  = 'España'
           PERSON_TUPLE[0].region   = 'Cantabria'
           PERSON_TUPLE[0].city     = 'Santa Maria de Cayon'
           PERSON_TUPLE[0].save()

        VISIT_TUPLE     = LastVisit.objects.get_or_create(user_id=PERSON_TUPLE[0].id)
        VISIT_OBJ       = VISIT_TUPLE[0]
        VISIT_OBJ.time  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if VISIT_OBJ.visit: VISIT_OBJ.visit += 1 
        else: VISIT_OBJ.visit = 1
        VISIT_OBJ.save()
        
        response_data = {}
        response_data['user_id'] = PERSON_TUPLE[0].id
        response_data['email']   = PERSON_TUPLE[0].email
        response_data['country'] = PERSON_TUPLE[0].country
        response_data['region']  = PERSON_TUPLE[0].region
        response_data['city']    = PERSON_TUPLE[0].city
        response_data['time']    = VISIT_OBJ.time
        response_data['visit']   = VISIT_OBJ.visit

        return DiscoJsonResponse(response_data)
    

    def save_user_location(request):
        try:
            personA = Person.objects.get(id=request.POST.get("user_id"), uid=request.POST.get("uid"), email=request.POST.get("email"))
            personA.country = request.POST.get("country", "España")
            personA.region  = request.POST.get("region", "Cantabria")
            personA.city    = request.POST.get("city","Santa Maria de Cayon")
            personA.save()
            response_data = {}
            response_data['country'] = personA.country
            response_data['region']  = personA.region
            response_data['city']    = personA.city 
            SetLocateAddress(personA)
            return DiscoJsonResponse(response_data)
        except:
            pass