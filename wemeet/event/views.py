import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http  import JsonResponse
from .util        import login_decorator
from wemeet.my_settings import WEMEET_SECRET
from user.models  import User
from group.models import Group
from .models      import Location, Event, EventUser
class EventCreate(View):

    @login_decorator
    def post(self, request):

        data = json.loads(request.body)

        host_user_id = request.user.id
        host_user_object = User.objects.get(id = host_user_id)

        group_id = request.GET.get('group')
        group_object = Group.objects.get(id = group_id)
        group_object_by_user = Group.objects.get(id = group_id).host.id

        try:
            if request.GET.get('group') is False:
                return JsonResponse({"message": "GROOUP_ID_NOT_EXIST"}, status = 404)

            elif Group.objects.get(id = group_id) is False:
                return JsonResponse({"message": "GROUP_NOT_EXIST"}, status = 401)

            elif host_user_id != group_object_by_user:
                return JsonResponse({"message": "NO_AUTH_HOST"}, status = 401)

            loc = Location.objects.get(name=data["loc_name"])
            event = Event.objects.create(
                title         = data["title"],
                mainimage     = data["mainimage"],
                introduction  = data["introduction"],
                findlocation  = data["findlocation"],
                start_date    = data["start_date"],
                end_date      = data["end_date"],
                limit_user    = data["limit_user"],
                group         = group_object,
                location      = loc,
            )
            EventUser.objects.create(
                user          = host_user_object,
                event         = event
                #host 추가해서 식별해주기
            )
            return JsonResponse({"event_id":event.id,"message":"SUCCESS"}, status=200)
        except Exception as e:
            return JsonResponse({"message": "FALSE"}, status = 500)
class AllEventListView(View):

    def get(self, request):
        event_all = list(Event.objects.values())        
        return JsonResponse({"data":event_all,"message":"SUCCESS"},status = 200)

class EventDetailView(View):

    def get(self, request):
        group_id = request.GET.get('group')
        group_now_id = Group.objects.get(id = group_id).host

        event_id = request.GET.get('event')
        event_now_id = Event.objects.filter(id = event_id)

        if  "Authorization" not in request.headers:
            participant = list(EventUser.objects.filter(id = event_id).values())
            page_detail = list(Event.objects.filter(id = event_id).values())
            return JsonResponse({"participant":participant,"error_code":"INVALID_LOGIN"}, status=200)
        try :
            encode_token = request.headers["Authorization"] 
            data = jwt.decode(encode_token, WEMEET_SECRET['secret'], algorithm='HS256')
            request.user = User.objects.get(id = data["user_id"])
            auth_id = request.user.id
            
            if group_now_id == auth_id :

                if event_now_id == group_now_id.host :

                    participant = list(EventUser.objects.filter(id = event_id).values())
                    page_detail = list(Event.objects.filter(id = event_id).values())
                    return JsonResponse({"participant":participant,"page_detail":page_detail,"who":"host","message":"SUCCESS"}, status=200)
               
                participant = list(EventUser.objects.filter(id = event_id).values())
                page_detail = list(Event.objects.filter(id = event_id).values())
                return JsonResponse({"participant":participant,"page_detail":page_detail,"who":"user","message":"SUCCESS"}, status=200)

            participant = list(EventUser.objects.filter(id = event_id).values())
            page_detail = list(Event.objects.filter(id = event_id).values())
            return JsonResponse({"participant":participant,"page_detail":page_detail,"who":"user","message":"SUCCESS"}, status=200)
        
        except jwt.DecodeError:
            participant = list(EventUser.objects.filter(id = event_id).values())
            page_detail = list(Event.objects.filter(id = event_id).values())
            return JsonResponse({"participant":participant,"page_detail":page_detail,"error_code" : "INVALID_TOKEN"}, status = 401) 

        except User.DoesNotExist:
            participant = list(EventUser.objects.filter(id = event_id).values())
            page_detail = list(Event.objects.filter(id = event_id).values())
            return JsonResponse({"participant" : participant,"page_detail":page_detail,"error_code" : "UNKNOWN_USER"}, status=200)