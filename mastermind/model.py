from google.appengine.ext import db
class Scores(db.Model):
  numGuesses=db.IntegerProperty()
