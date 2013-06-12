from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template import RequestContext
import simplejson, urllib, json
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
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/indicators?id="

    # Children not enrolled in school (%)
    noenroll_all =api_url+"59"

    #Children between 3 and 4 years who are not enrolled (%)
    noenroll_3_4 = api_url+"58"

    #Youths 16 to 19 years are not enrolled nor school diploma (%)
    noenroll_teen = api_url+"60"

    # Youth aged 18 to 24 enrolled in or completed college
    noenroll_adult = api_url+"63"

    sortedValues = {}
    indicatorName = []

    ind1 = simplejson.load(urllib.urlopen(noenroll_all))
    ind2 = simplejson.load(urllib.urlopen(noenroll_3_4))
    ind3 = simplejson.load(urllib.urlopen(noenroll_teen))
    ind4 = simplejson.load(urllib.urlopen(noenroll_adult))

    newTable = []

    for i in xrange(78): #height
     row = []
     for j in xrange(5): #width
      row.append('')
     newTable.append(row)

    for item in ind1:
        sortedValues[item['county']] = item['value']


    for i in xrange(77):
        #print ind1[i]
        county = int(ind1[i]['county_id'])
        val1 = ind1[i]['value']

        #print ind1[i]['county_id'] + ind1[i]['county']

        newTable[county][0] = unicode(ind1[i]['county']) #[u'A\xf1asco
        newTable[county][1] = ind1[i]['value']
        newTable[county][2] = ind2[i]['value']
        newTable[county][3] = ind3[i]['value']
        newTable[county][4] = ind4[i]['value']

        valuesfordisplay = json.dumps(newTable)

    newTable[0][0] = "county"
    newTable[0][1] = "Children not enrolled in school"
    newTable[0][2] = "Children between 3 and 4 years who are not enrolled "
    newTable[0][3] = "Youths 16 to 19 years are not enrolled nor school diploma"
    newTable[0][4] = "Youth aged 18 to 24 enrolled in or completed college"

    #print newTable

    the_dump=json.dumps("['foo', {'bar':['baz', null, 1.0, 2]}]")

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": newTable,
                "jsondata": newTable,
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": "% of school enrollment"}


    #pass to template
    return render_to_response("pages/index.html", context)



def college(request):
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/indicators?id="
    # Children not enrolled in school (%)
    noenroll_all =api_url+"59"


    sortedValues = {}
    indicatorName = []

    ind1 = simplejson.load(urllib.urlopen(noenroll_all))
    ind2 = simplejson.load(urllib.urlopen(noenroll_3_4))
    ind3 = simplejson.load(urllib.urlopen(noenroll_teen))
    ind4 = simplejson.load(urllib.urlopen(noenroll_adult))

    newTable = []

    for i in xrange(78): #height
     row = []
     for j in xrange(5): #width
      row.append('')
     newTable.append(row)

    for item in ind1:
        sortedValues[item['county']] = item['value']


    for i in xrange(77):
        #print ind1[i]
        county = int(ind1[i]['county_id'])
        val1 = ind1[i]['value']

        #print ind1[i]['county_id'] + ind1[i]['county']

        newTable[county][0] = unicode(ind1[i]['county']) #[u'A\xf1asco
        newTable[county][1] = ind1[i]['value']
        newTable[county][2] = ind2[i]['value']
        newTable[county][3] = ind3[i]['value']
        newTable[county][4] = ind4[i]['value']

        valuesfordisplay = json.dumps(newTable)

    newTable[0][0] = "county"
    newTable[0][1] = "Children not enrolled in school"
    newTable[0][2] = "Children between 3 and 4 years who are not enrolled "
    newTable[0][3] = "Youths 16 to 19 years are not enrolled nor school diploma"
    newTable[0][4] = "Youth aged 18 to 24 enrolled in or completed college"

    #print newTable

    the_dump=json.dumps("['foo', {'bar':['baz', null, 1.0, 2]}]")

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": [["Country", "Group 1", "Group 2", "Group 3", "Group 4"], ["", "", "", "", ""]],
                "jsondata": newTable,
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": "% of college enrollment"}


    #pass to template
    return render_to_response("pages/index.html", context)

def workforce(request):

    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/indicators?id="

    #metrics
    # % Of people in the workforce with lower education than fourth year (25 - 64 years)
    under4th = api_url+"73"

    #% Of people in the workforce with education fourth year (25 - 64 years)
    fourth = api_url+"74"

    #% Of people in the workplace with some years in the univ or an associate degree (25 - 64 years)
    assoc = api_url+"75"

    #% Of people in the workforce with degree or higher (25 - 64 years)
    degre = api_url+"76"

    sortedValues = {}
    indicatorName = []

    ind1 = simplejson.load(urllib.urlopen(under4th))
    indicatorName.append(ind1[1]['indicator'])

    ind2 = simplejson.load(urllib.urlopen(fourth))
    indicatorName.append(ind2[1]['indicator'])

    ind3 = simplejson.load(urllib.urlopen(assoc))
    indicatorName.append(ind3[1]['indicator'])

    ind4 = simplejson.load(urllib.urlopen(degre))
    indicatorName.append(ind4[1]['indicator'])

    newTable = []

    for i in xrange(78): #height
     row = []
     for j in xrange(5): #width
      row.append('')
     newTable.append(row)

    for item in ind1:
        sortedValues[item['county']] = item['value']


    for i in xrange(77):
        #print ind1[i]
        county = int(ind1[i]['county_id'])
        val1 = ind1[i]['value']

        #print ind1[i]['county_id'] + ind1[i]['county']

        newTable[county][0] = unicode(ind1[i]['county']) #[u'A\xf1asco
        newTable[county][1] = ind1[i]['value']
        newTable[county][2] = ind2[i]['value']
        newTable[county][3] = ind3[i]['value']
        newTable[county][4] = ind4[i]['value']

        valuesfordisplay = json.dumps(newTable)

    newTable[0][0] = "county"
    newTable[0][1] = "under 4th year"
    newTable[0][2] = "4th year"
    newTable[0][3] = "some college"
    newTable[0][4] = "university degree"

    #print newTable

    the_dump=json.dumps("['foo', {'bar':['baz', null, 1.0, 2]}]")

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": newTable,
                "jsondata": valuesfordisplay,
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": "% of people in the workforce with education"}


    #pass to template
    return render_to_response("pages/index.html", context)


# Speaking both Languages
#Children 5 to 17 years who speak Spanish and English is "less than very well" (%)
#biling = apiurl+"61"

#Children who speak another language at home other than English and Spanish (%)
#biling = apiurl+"62"



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
