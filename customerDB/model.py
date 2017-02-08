from google.appengine.ext import db
class CustomerT(db.Model):
  firstName=db.StringProperty()
  lastName = db.StringProperty()
  age=db.IntegerProperty()
  email=db.StringProperty()





    
