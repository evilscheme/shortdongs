from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.utils import simplejson
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from shortdongs.shortener.models import *
from dongbits import dong_to_int
import re

def index(request):
    return direct_to_template(request, 'shortener/index.html')

def shorten(request):
    try:
        url = request.POST['url']
    except:
        raise Http404()
    
    if not re.match('^https?://.*', url):
        raise Http404()

    try:
        url = URL.objects.get(url=url)
    except URL.DoesNotExist:
        url = URL(url=url)
        url.save()
    
    return direct_to_template(request, 'shortener/showurl.html', {'url':url})

def dump(request):
    urls = URL.objects.all()

    return direct_to_template(request, 'shortener/dump.html', {'urls':urls})

def resolve(request, dong):
    dong = dong.replace('/', '')
    try:
        uid = dong_to_int(dong)
    except:
        raise Http404()
    
    url = get_object_or_404(URL, id=uid)

    return direct_to_template(request, 'shortener/redirect.html', {'url':url})