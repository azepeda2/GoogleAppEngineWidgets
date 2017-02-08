from google.appengine.ext import db
class VoteTable(db.Model):
  vote = db.StringProperty()
  user = db.UserProperty()



 


    
