import webapp2
import csv
import os
import time
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, World!')

        template_values = {
            'greetings': 'greetings',
            'url': 'url',
            'url_linktext': 'url_linktext',
            'title': 'Booloo Export',
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/start.html')
        self.response.out.write(template.render(path, template_values))

class ProcessPage(webapp2.RequestHandler):
    def post(self):

        ## Load all files into lists
        teams_file_list = self.file_to_list(self.request.get('teamsFile'))
        source_file_list = self.file_to_list(self.request.get('sourceFile'))
        total_file_list = self.file_to_list(self.request.get('totalFile'))

        ## Split file lists into group lists
        ## 'key in CSV file' --> filename of JSON output
        # (teams_file_list) 'Sumo' --> sumo
        # (teams_file_list) 'Reps' --> reps
        # (teams_file_list) 'QA' --> qa
        # (teams_file_list) 'Firefox OS' --> firefoxos
        # (teams_file_list) 'Firefox for Android' --> firefoxforandroid
        # (teams_file_list) 'Firefox' --> firefox
        # (source_file_list) 'bugzilla' --> bugzilla
        # (source_file_list) 'github' --> github
        # (total_file_list) 'all' --> all
        final_data = []
        final_data.append(self.transform_data(teams_file_list, 1, 'Sumo', 'sumo'))
        final_data.append(self.transform_data(teams_file_list, 1, 'Reps', 'reps'))
        final_data.append(self.transform_data(teams_file_list, 1, 'QA', 'qa'))
        final_data.append(self.transform_data(teams_file_list, 1, 'Firefox OS', 'firefoxos'))
        final_data.append(self.transform_data(teams_file_list, 1, 'Firefox For Android', 'firefoxforandroid'))
        final_data.append(self.transform_data(teams_file_list, 1, 'Firefox', 'firefox'))
        final_data.append(self.transform_data(source_file_list, 0, 'bugzilla', 'bugzilla'))
        final_data.append(self.transform_data(source_file_list, 0, 'github', 'github'))
        final_data.append(self.transform_data(total_file_list, 0, 'NOKEY', 'all'))

        template_values = {
            'data':final_data,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/finish.html')
        self.response.out.write(template.render(path, template_values))

    def file_to_list(self, fle):
        ret = []
        rownum = 0
        reader = csv.reader(fle.split("\n"))
        for row in reader:
            if rownum == 0:
                header = row
            else:
                ret.append(row)                    
            rownum += 1 
        return ret

    def transform_data(self, src, key_pos, key, dest):
        # Create list
        filtered_list = []
        for row in src:
            if len(row) > 0:
                if row[key_pos] == key or key == 'NOKEY':
                    filtered_list.append(row)
        filtered_list.reverse()
    
        ## GAE doesn't let you write to files /facepalm
        #with open(dest,"w") as f:
        #    f.write('test')
        #    f.close()

        #for each

        return_json = ""
        i = 0
        return_json += '['
        for row in filtered_list:
            add_comma = ","
            if i == 0:
                add_comma = ""
            #September 29, 2014
            try:
                dt = time.strptime(row[key_pos+1], "%B  %d, %Y")
                week_date_string = time.strftime("%Y-%m-%d", dt)
                return_json += add_comma + '{"wkcommencing":"' + week_date_string + '","totalactive":' + row[key_pos+3] + ',"new":' +  row[key_pos+2] + '}'
                i += 1
            except ValueError:
                continue

        return_json += "]"
        return [return_json,dest]


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/process', ProcessPage)
], debug=True)
