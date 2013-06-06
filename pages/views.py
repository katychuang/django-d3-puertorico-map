from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template import RequestContext
import simplejson, urllib

# Create your views here.

def home(request):
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
    counties = simplejson.load(urllib.urlopen(api_url+"counties"))

    categories = simplejson.load(urllib.urlopen(api_url+"categories"))

    indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    #pass to template
    return render_to_response("pages/index.html",
        {"counties": counties,
        "categories": categories,
        "indicators": indicators})

def search(request):
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
    counties = simplejson.load(urllib.urlopen(api_url+"counties"))

    categories = simplejson.load(urllib.urlopen(api_url+"categories"))

    indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    query_cat = ''
    query_ind = ''
    found_entries = None
    if ('cat' in request.GET) and request.GET['cat'].strip():
        query_cat = request.GET['cat']

    if ('ind' in request.GET) and request.GET['ind'].strip():
        query_ind = request.GET['ind']
        filtered_ind = simplejson.load(urllib.urlopen(api_url + "indicators?id=" + query_ind))


    return render_to_response('pages/index.html',
                              {"counties": counties,
                                "categories": categories,
                                "indicators": indicators,
                                "valuesfordisplay": filtered_ind},
                              context_instance=RequestContext(request))
