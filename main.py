import webapp2
import os
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

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
