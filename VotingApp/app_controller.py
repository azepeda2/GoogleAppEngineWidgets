
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import model
from appengine_utilities import sessions


# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    logouturl = users.create_logout_url('/')
    template_values={'userName':user, 'logouturl':logouturl}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

class VoteHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    voteText = self.request.get('voteText') 
    userVotes = db.GqlQuery('Select * from VoteTable')
    logouturl = users.create_logout_url('/')
    userVoteQuery = db.GqlQuery('Select * from VoteTable where user=:1',user)
    voter = userVoteQuery.get()
    if not voter:
	voter = model.VoteTable()
	voter.user = user
    voter.vote = voteText
    voter.put()
    template_values={'userVotes':userVotes,'logouturl':logouturl}
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
					# MainPage handles the home page load
                                     [('/', MainPage),
 				      ('/onvote', VoteHandler)
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
