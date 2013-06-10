from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template import RequestContext
import simplejson, urllib
from operator import itemgetter

#for contact form
from django.shortcuts import render
from pages.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

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
    #categories = simplejson.load(urllib.urlopen(api_url+"categories"))
    indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    indicatorName = ''
    query_ind = ''
    filtered_ind = ''
    found_entries = None
    jsonURL = ''
    sortedValues = {}
    counties = {}

    if ('indicators' in request.GET) and request.GET['indicators'].strip():
        query_ind = request.GET['indicators']
        filtered_ind = simplejson.load(urllib.urlopen(api_url + "indicators?id=" + query_ind))

        jsonURL = api_url + "indicators?id=" + query_ind
        indicatorName = filtered_ind[1]['indicator']

    for item in filtered_ind:
        counties[item['county_id']] = item['county']
        sortedValues[item['county']] = item['value']

    #json_string = simplejson.dumps(filtered_ind)

    return render_to_response('pages/index.html',
                              {"counties": counties,
                                "indicators": indicators,
                                "valuesfordisplay": filtered_ind,
                                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                                "jsonURL": jsonURL,
                                "indicatorName": indicatorName},
                              context_instance=RequestContext(request))

def joven(request):
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
    counties = simplejson.load(urllib.urlopen(api_url+"counties"))

    categories = simplejson.load(urllib.urlopen(api_url+"categories"))

    indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    #pass to template
    return render_to_response("pages/joven.html",
        {"counties": counties,
        "categories": categories,
        "indicators": indicators})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['noreply@email.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})
