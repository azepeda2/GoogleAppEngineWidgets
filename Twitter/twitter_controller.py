
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from appengine_utilities import sessions

import model

# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
    user=users.get_current_user()
    #nickname= user.nickname()
    tweets=db.GqlQuery('Select * from TweetTable where user= :1', user)
    logouturl=users.create_logout_url('/')
    template_values={'tweets':tweets,'logouturl':logouturl}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

class SubmitTweetHandler(webapp.RequestHandler):
 def get(self):
      user= users.get_current_user()
      status=self.request.get('statusText')
      tweet=model.TweetTable()
      tweet.statusMessage=status
      tweet.user=user
      tweet.put()
      tweets=db.GqlQuery('Select * from TweetTable where user= :1', user)
      logouturl=users.create_logout_url('/')
      template_values={'tweets':tweets,'logouturl':logouturl}
      # render the page using the template engine
      path = os.path.join(os.path.dirname(__file__),'index.html')
      self.response.out.write(template.render(path,template_values))


# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
					# MainPage handles the home load
                                     [('/', MainPage),
					# when user clicks on add button, we call on_add action
					# check out index.html to see where on_add gets submitted
                                       ('/submit_tweet',SubmitTweetHandler)
                                       ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
