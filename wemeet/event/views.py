import json
import jwt
import bcrypt
import datetime

from django.views import View
from django.http  import JsonResponse

from .util              import login_decorator
from wemeet.my_settings import WEMEET_SECRET
from user.models        import User
from group.models       import Group
from .models            import Location, Event, EventUser

class Event(View):
    @login_decorator
    def post(self, request, group_id):
        data = json.loads(request.body)

        try:
            group = Group.objects.get(id = group_id)

            if group.host.id == request.user.id:
                return JsonResponse({"message": "NO_AUTH_HOST"}, status = 401)

            location = Location.objects.get(name = data["loc_name"])
            event    = Event.objects.create(
                title         = data["title"],
                mainimage     = data["mainimage"],
                introduction  = data["introduction"],
                findlocation  = data["findlocation"],
                start_date    = data["start_date"],
                end_date      = data["end_date"],
                limit_user    = data["limit_user"],
                group         = group_object,
                location      = location,
            )

            EventUser.objects.create(
                user  = request.user,
                event = event
            )

            return JsonResponse({"event_id":event.id,"message":"SUCCESS"}, status=200)
        except Group.DoesNotExist:
            return JsonResponse({"error": "INVALID_GROUP"}, status = 404)
        except KeyError:
            return JsonResponse({"message": "INVALID_INPUT"}, status = 404)

class AllEventListView(View):
    def get(self, request):
        return JsonResponse({"data": list(Event.objects.values())}, status = 200)

class EventDetailView(View):
    @check_login
    def get(self, request, event_id):
        event = Event.objects.get(id = event_id)
        user  = getattr(request, 'user', None)

        return JsonResponse({
            "participant": event.user,
            "page_detail": [{
                "title"    : event.title,
                "location" : event.name,
                # ...                
            }],
            "host"  : user and user.id == event.group.host.id
        }, status=200)
