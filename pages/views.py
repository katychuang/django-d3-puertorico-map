from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
# Create your views here.

def home(request):

    #pass to template
    return render_to_response("pages/index.html")
