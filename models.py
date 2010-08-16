from google.appengine.ext import db

class Event(db.Model):
    station = db.IntegerProperty(required=True)
    time = db.DateTimeProperty(required=True)
    event = db.IntegerProperty(required=True)

