#Statistics from the Education of Puerto Rico

[According to the 2000 Census](http://www.census.gov/prod/2003pubs/c2kbr-24.pdf), 60.0% of the population attained a high school degree or higher level of education, and 18.3% has a bachelor's degree or higher.

Completion of high school is important for employability and longevity. People who received their high school diploma or GED were 37.5 percent less likely to be unemployed than others according to the [Bureau of Labor Statistics](http://www.bls.gov/ooh/Management/Sales-managers.htm). In addition, individuals who do not receive a diploma are more likely to: require public assistance; have health problems; and engage in criminal activity.

Our project works to convert data into actionable insights for the policy decision makers.


#Data Joven Vizualizations

This app streamlines the data analysis process for the Institute of Youth Development API.

Goals of this app:

- Easily publish the data visualizations online.
- Allow the enduser to create their own filters for [API](http://www.pixelogicpr.com/PRYouthAPI) data


Technical Environment:

- Hosted on [Heroku](http://www.heroku.com) Cloud Service
- Python ([Django](https://www.djangoproject.com/), [SimpleJson](https://pypi.python.org/pypi/simplejson/))
- Javascript (D3.js, [AtlasPR](http://miguelrios.github.io/atlaspr), NVD3.js)
- Theme borrowed from PixelLogic's [prototype](pixelogic.co/c/bgc/www/)
- [API](http://www.pixelogicpr.com/PRYouthAPI) from Institute for Youth Development and PixelLogic


**Demo:**
http://puertorico.herokuapp.com

**Interactive Reports:**
http://puertorico.herokuapp.com/joven


## Screenshots

### 1. Landing Page

This page shows the map of Puerto Rico (rendered by AtlasPR). There are links to the interactive report and to view indicators for education.

![landing](screenshot/landing.png)


### 2. Interactive Report

This [page](http://puertorico.herokuapp.com/joven/) uses D3.js and NVD3.js to render both the map and the chart. Clicking on a county on the map will show statistics in the bar chart on the left.

![interactive](screenshot/interactive.png)

