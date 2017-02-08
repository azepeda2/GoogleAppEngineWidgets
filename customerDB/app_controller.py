
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import CustomerT


# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
    searchmessage=''
    customers = db.GqlQuery("Select * from CustomerT")
    template_values={'searchmessage':searchmessage,'customerList':customers}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

class StoreItHandler(webapp.RequestHandler):
  def get(self):
    # get parameters
    first = self.request.get("first")
    last = self.request.get("last")
    age = self.request.get("age")
    age = int(age)
    email = self.request.get("email")
    searchmessage=''
    # create a new record
    customer = CustomerT()
    customer.firstName=first
    customer.lastName=last
    customer.age=age
    customer.email=email
    customer.put()

    self.redirect("/")
    
class OnlyShowHandler(webapp.RequestHandler):
  def get(self):
    # get parameters
    searchFirst = self.request.get("searchFirst")
    searchmessage='Your search reults: '
    customers = db.GqlQuery("SELECT * FROM CustomerT WHERE firstName = :1", searchFirst)
    customer= db.GqlQuery("SELECT * FROM CustomerT")
    template_values={'searchmessage':searchmessage,'filteredcustomerList':customers, 'customerList':customer}
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))


# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
					# MainPage handles the home page load
                                     [('/', MainPage),
				      ('/storeit',StoreItHandler),
                                      ('/only_show',OnlyShowHandler)
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
