import json
import jwt
import bcrypt

import datetime
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Users
