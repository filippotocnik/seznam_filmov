from google.appengine.ext import ndb


class Film(ndb.Model):
    ime = ndb.StringProperty()
    ocena = ndb.IntegerProperty()
    slika = ndb.TextProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
