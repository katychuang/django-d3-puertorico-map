#------------------------------------------------------------------------------#
# Imports
#------------------------------------------------------------------------------#
import simplejson, urllib, json

from flask import * # do not use '*'; actually input the dependencies
import logging
from logging import Formatter, FileHandler
from forms import RegisterForm, LoginForm
#------------------------------------------------------------------------------#
# App Config
#------------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


# Login required decorator
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

#latin encoding
# http://writeonly.wordpress.com/2008/12/10/the-hassle-of-unicode-and-getting-on-with-it-in-python/
def decoder(str):
    # try:
    #     text = unicode(text, 'utf-8')
    #     return text
    # except TypeError:
    #     return unicode(text, 'latin-1')

    u = None
    # we could add more encodings here, as warranted.
    encodings = ('ascii', 'utf8', 'latin1')
    for enc in encodings:
        if u:  break
        try:
            u = unicode(str, enc)
        except UnicodeDecodeError:
            if verbose: print "error for %s into encoding %s" % (str, enc)
            pass
    if not u:
        u = unicode(str, errors='replace')
        if verbose:  print "using replacement character for %s" % str

    return u

#------------------------------------------------------------------------------#
# Controllers
#------------------------------------------------------------------------------#

@app.route("/")
def index():
    api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
    counties = ""  #simplejson.load(urllib.urlopen(api_url+"counties"))

    categories = ""  #simplejson.load(urllib.urlopen(api_url+"categories"))

    indicators = "" #simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

    #pass to template
    context = { "counties":   counties
              , "categories": categories
              , "indicators": indicators}

    return render_template("index.html")

@app.route("/joven/")
def joven():
    try:
        api_url = "http://www.pixelogicpr.com/PRYouthAPI/public/api/"
        context = {"json_data": api_url}

        counties = simplejson.load(urllib.urlopen(api_url+"counties"))
        # categories = simplejson.load(urllib.urlopen(api_url+"categories"))
        # indicators = simplejson.load(urllib.urlopen(api_url+"indicatorsList"))

        # context = {"counties": counties,
        #            "categories": categories,
        #            "indicators": indicators}
    except:
        context = {"json_data": "/static/js/edu.json"}

    return render_template("joven.html", **context)

@app.route("/search/")
def search():
    return render_template("index.html")

@app.route("/enrollment/")
def enrollment():
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

        newTable[county][0] = ind1[i]['county'].encode('ascii', 'ignore')
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

    jsondata = {}
    values = []
    for row in newTable:
        # clear data structures
        v = {}
        values = []

        values.append({"value": row[1], "label": "a"})
        values.append({"value": row[2], "label": "b"})
        values.append({"value": row[3], "label": "c"})
        values.append({"value": row[4], "label": "d"})

        v["values"] = values
        jsondata[row[0]] = [v]

    print simplejson.dumps(jsondata)

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": newTable,
                "jsondata": "/static/js/enrollment.json",
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": "% of school enrollment"}


    #pass to template
    return render_to_response("index.html", **context)

@app.route("/college/")
def college():
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
    return render_to_response("index.html", **context)

@app.route("/workforce/")
def workforce():
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

        #valuesfordisplay = json.dumps(newTable)

    newTable[0][0] = "county"
    newTable[0][1] = "under 4th year"
    newTable[0][2] = "4th year"
    newTable[0][3] = "some college"
    newTable[0][4] = "university degree"


    jsondata = {}
    values = []
    for row in newTable:
        # clear data structures
        v = {}
        values = []

        values.append({"value": row[1], "label": "a"})
        values.append({"value": row[2], "label": "b"})
        values.append({"value": row[3], "label": "c"})
        values.append({"value": row[4], "label": "d"})

        v["values"] = values
        jsondata[row[0]] = [v]

    #print simplejson.dumps(jsondata)

    context = {"counties": "",
                "indicators": "",
                "valuesfordisplay": newTable,
                "jsondata": "/static/js/workforce.json",
                "sorted": sorted(sortedValues.iteritems(), key=itemgetter(1), reverse=True),
                "jsonURL": api_url,
                "indicatorName": "% of people in the workforce with education"}


    #pass to template
    return render_to_response("index.html", context)



@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/login", methods=('GET', 'POST'))
def loginaction():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')

        ## TASK #1: You will be adding in the logic here for successful log in.

        ## TASK #2: You will be redirecting the user to the right template.
    return render_template("login.html", form=form)

@app.route("/register")
def register():
    return render_template("register.html")


# Error Handlers

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#------------------------------------------------------------------------------#
# Launch
#------------------------------------------------------------------------------#

# default  port
if __name__ == '__main__':
    app.run()

# or specify port
'''
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
'''
