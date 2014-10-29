# Overview

This is a stopgap until the data metrics team gives us the requested access to community data.

Pending bugs to provide a more permanent solution:

* bug 1081284 - Access to REST API for Tableau
* bug 1086706 - REST API access to Baloo/Vertica

# Solution

The temporary solution will be 

1. manually export CSV files out of Tableau
2. run a script to convert the files to a JSON format usable by MozID
3. open a PR to upload the new JSON to bedrock

This bug covers creating the script in #2.

This is hosted on GAE at http://booloo-mozid.appspot.com/

# Source Data

The source data we will be pull from is Tableau tabs

1. https://dataviz.mozilla.org/views/Active_Contributor_Dashboard/nums_total#1
2. https://dataviz.mozilla.org/views/Active_Contributor_Dashboard/nums_team#1
3. https://dataviz.mozilla.org/views/Active_Contributor_Dashboard/nums_source#1

There is a button at the bottom of the screen to allow you to export data.

# JSON Format

The data from the Tableau exports will be converted into the following format

http://doctodash.herokuapp.com/tab/all
