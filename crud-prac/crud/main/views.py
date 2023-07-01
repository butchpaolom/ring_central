from django.views.generic.base import TemplateView
from django.views import View
from main.serializers import UserSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
import math
from datetime import datetime


def logger(func):
    def wrap_func(*args, **kwargs):
        request = args[1]
        now = datetime.now()

        if 'requests' not in request.session:
            request.session['requests'] = []
        reqs = request.session['requests']
        reqs.append(f'[{now}] {request.method} {request.path} {request.scheme}')
        request.session['requests'] = reqs


        result = func(*args, **kwargs)
        return result
    return wrap_func

    

class HomePageView(View):
    @logger
    def get(self, request):
        count = User.objects.all().count()
        pages = math.ceil(count/5)
        return TemplateResponse(request, 'home.html', {'pages': pages})
    
class RequestsView(View):
    def get(self, request):
        if 'requests' not in request.session:
            return HttpResponse()
        logs = request.session['requests']
        return TemplateResponse(request, 'logs.html', {'logs': logs})


@method_decorator(csrf_exempt, name='dispatch')
class CRUDView(View):
    @logger
    def get(self, request):
        id = request.GET.get('id')
        page = request.GET.get('page')
        if not id:
            if page:
                user = User.objects.all().order_by('id')
                p = Paginator(user, 5)
                res = p.page(page)
                serializer = UserSerializer(res, many=True)
            else:
                user = User.objects.all()
                serializer = UserSerializer(user, many=True)
        else:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    
    @logger
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        username = body_data['username']
        email = body_data['email']
        first_name = body_data['first_name']
        last_name = body_data['last_name']
        password = body_data['password']
        try:
            user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name)
        except:
            return HttpResponseBadRequest()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    
    @logger
    def put(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        id = body_data['id']
        if not id:
            return HttpResponseBadRequest()
        user = get_object_or_404(User, id=id)
        username = body_data['username']
        email = body_data['email']
        first_name = body_data['first_name']
        last_name = body_data['last_name']
        password = body_data['password']

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.save()

        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    
    @logger
    def delete(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        id = body_data['id']
        if not id:
            return HttpResponseBadRequest()
        user = get_object_or_404(User, id=id)
        user.delete()
        return HttpResponse()
    



        

