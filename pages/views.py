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

    #if an indicator is selected, it should filter api
    if ('indicators' in request.GET) and request.GET['indicators'].strip():
        query_ind = request.GET['indicators']
        filtered_ind = simplejson.load(urllib.urlopen(api_url + "indicators?id=" + query_ind))

        jsonURL = api_url + "indicators?id=" + query_ind
        indicatorName = filtered_ind[1]['indicator']

    # filter into 2 dictionaries for rendering into tables sorted by alpha and values.
    for item in filtered_ind:
        counties[item['county_id']] = item['county']
        sortedValues[item['county']] = item['value']

    #json_string = simplejson.dumps(filtered_ind)

    context = {"counties": counties,
                "indicators": indicators,
                "valuesfordisplay": filtered_ind,
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": jsonURL,
                "indicatorName": indicatorName}

    return render_to_response('pages/index.html', context,
                              context_instance=RequestContext(request))

def joven(request):
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
    counties = simplejson.load(urllib.urlopen(api_url+"counties"))

    categories = simplejson.load(urllib.urlopen(api_url+"categories"))

    indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    context = {"counties": counties,
               "categories": categories,
               "indicators": indicators}

    #pass to template
    return render_to_response("pages/joven.html", context)

"""
<option value="58"><font><font>Children between 3 and 4 years who are not enrolled (%)</font></font></option>

<option value="59"><font><font>Children not enrolled in school (%)</font></font></option>

<option value="60"><font><font>Youths 16 to 19 years are not enrolled nor school diploma (%)</font></font></option>

<option value="61"><font><font>Children 5 to 17 years who speak Spanish and English is "less than very well" (%)</font></font></option>

<option value="62"><font><font>Children who speak another language at home other than English and Spanish (%)</font></font></option>

<option value="63"><font><font>Youth aged 18 to 24 enrolled in or completed college </font></font></option>

<option value="64"><font><font>Educational Attainment in the 25 and older - Less than ninth grade (%)</font></font></option>

<option value="65"><font><font>Educational Attainment in the 25 and older - Between ninth and fourth year (not graduate) (%)</font></font></option>

<option value="66"><font><font>Educational Attainment in the 25 and older - Fourth year or equivalent (%)</font></font></option>

<option value="67"><font><font>Educational Attainment in the 25 years and over - Some years in college (no degree) (%)</font></font></option>

<option value="68"><font><font>Educational Attainment in the 25 and older - Associate Degree (%)</font></font></option>

<option value="69"><font><font>Educational Attainment in the 25 and older - University degree (%) </font></font></option>

<option value="70"><font><font>Educational Attainment in the 25 and older - graduate or professional diploma (%) </font></font></option>

<option value="71"><font><font>Educational Attainment in the group 25-34 years old - High school or more (%) </font></font></option>

<option value="72"><font><font>Educational Attainment in the group 25-34 years old - Bachelor or more (%)</font></font></option>

"""

def enrollment(request):
    context = {}


    #pass to template
    return render_to_response("pages/joven.html", context)

def college(request):
    context = {}

    #pass to template
    return render_to_response("pages/joven.html", context)

def workforce(request):

    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/indicators?id="

    #metrics
    # % Of people in the workforce with lower education than fourth year (25 - 64 years)
    under4th = apiurl+"73"

    #% Of people in the workforce with education fourth year (25 - 64 years)
    fourth = apiurl+"74"

    #% Of people in the workplace with some years in the univ or an associate degree (25 - 64 years)
    assoc = apiurl+"75"

    #% Of people in the workforce with degree or higher (25 - 64 years)
    degre = apiurl+"76"



    filtered_ind = simplejson.load(urllib.urlopen(api_url + "indicators?id=" + query_ind))

    indicatorName = filtered_ind[1]['indicator']

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": filtered_ind,
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": indicatorName}


    #pass to template
    return render_to_response("pages/index.html", context)



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
