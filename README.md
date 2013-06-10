
#Data Joven

This app streamlines the data analysis process for the Institute of Youth Development API.

Goals of this app:
- Easily publish the data visualizations online.
- Allow the enduser to create their own filters for [API](www.pixelogicpr.com/PRYouthAPI) data

This app is built with python's django framework, AtlasPR javascript library, and the theme comes from Institute for Youth Development.

Demo: http://puertorico.herokuapp.com/

Interactive Reports: http://puertorico.herokuapp.com/joven/

# Landing Page

This page shows the map of Puerto Rico (rendered by AtlasPR). There are links to the interactive report and to view indicators for education.

![landing](screenshot/landing.png)


# Interactive Report

This [page](http://puertorico.herokuapp.com/joven/) uses D3.js and NVD3.js to render both the map and the chart. Clicking on a county on the map will show statistics in the bar chart on the left.

![interactive](screenshot/interactive.png)
