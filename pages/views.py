from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
import simplejson, urllib

# Create your views here.

def home(request):
    url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/counties"
    counties = simplejson.load(urllib.urlopen(url))

    #pass to template
    return render_to_response("pages/index.html", {"counties": counties})
