from google.appengine.ext import db
class TweetTable(db.Model):
    statusMessage=db.StringProperty()
    date= db.DateTimeProperty(auto_now=True)
    user=db.UserProperty()
