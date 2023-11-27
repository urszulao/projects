import json
from django.http import JsonResponse


def api_home(request, *args, **kwargs):
    # request -> HttpRequest -> Django
    # print(dir(request))
    # json data - request.body
    print(request.GET) # url query params
    print(request.POST)
    body = request.body # byte string of JSON data
    data = {}
    try:
        data = json.loads(body) #string of JSON fata -> Python Dictionary
    except:
        pass    
    print(data)
   # data['headers'] = request.headers #request.META
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    print(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse(data)