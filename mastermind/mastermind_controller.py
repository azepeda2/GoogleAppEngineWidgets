
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from appengine_utilities import sessions
import model
import mastermind
# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
    session = sessions.Session()
    colors=["red","blue","green","purple","yellow","brown"]
    session['secret']=mastermind.generateSecret(colors)
    numGuesses=0
    session['numGuesses']=numGuesses
    showScores = db.GqlQuery("Select * from Scores")
    template_values={'showScores':showScores,'secret':session['secret']}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))


class GuessHandler(webapp.RequestHandler):
  def get(self):
    session=sessions.Session()
    color1=str(self.request.get('color1'))
    color2=str(self.request.get('color2'))
    color3=str(self.request.get('color3'))
    color4=str(self.request.get('color4'))
    guess=[]
    numGuesses=session['numGuesses']
    numGuesses=numGuesses+1
    guess.append(color1)
    guess.append(color2)
    guess.append(color3)
    guess.append(color4)
    guessCopy=guess[:]
    secret=session['secret']
    secretCopy=secret[:]
    match=mastermind.computeExacts(guessCopy,secretCopy)
    partialMatches=mastermind.computePartials(guessCopy,secretCopy)
    if match==4:
      gameStatus='Congratulations you are a winner! You guessed the secret colors! If you would like to play again click new game below'
      scores=model.Scores()
      scores.numGuesses=numGuesses
      scores.put()
    else:
      gameStatus='Awww mayne. Try again! If you want to try a completely new secret click new game below'
    session['numGuesses']=numGuesses
    showScores = db.GqlQuery("Select * from Scores")
    template_values={'guess':guess,'showScores':showScores,'secret':session['secret'], 'match':match, 'partialMatches':partialMatches, 'gameStatus':gameStatus}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

class NewGameHandler(webapp.RequestHandler):
    def get(self):
      session = sessions.Session()
      colors=["red","blue","green","purple","yellow","brown"]
      session['secret']=mastermind.generateSecret(colors)
      numGuesses=0
      session['numGuesses']=numGuesses
      showScores = db.GqlQuery("Select * from Scores")
      template_values={'showScores':showScores,'secret':session['secret']}
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
                                       ('/newgame',NewGameHandler),
                                      ('/on_guess', GuessHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
