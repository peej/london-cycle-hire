import urllib2, re, time
from google.appengine.api import memcache
import google.appengine.api.urlfetch_errors
from google.appengine.api import urlfetch

url = "https://web.barclayscyclehire.tfl.gov.uk/maps"

def getBodyFromSource():
    
    body = None
    
    result = urlfetch.fetch(url, headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.125 Safari/533.4',
        'Cookie': 'lchssession=pjlp17o7lebjjls6j0o5cfsv93; lchscookie=LDRM4pwHV9mRXksrlxsKZHUNJJf5D/MU0vfDBZXmroDA9uhCK61eu3uFr/NSwcgvpdmqQxQRksCsYg==; TS7a8c97=e54430b2bc1cbb70decaf7049c2ea192e322cbf2c6cc76f84c5c57d2d8ab25303643aa8bea3035484c09c470; CP=null*; ccokieenable'
    })
    
    if result.status_code == 200:
        body = result.content
        memcache.set(key="body", value=body)
        
    return body

def getBodyFromMemcache():
    body = memcache.get("body")
    #body = None
    if body is None:
        try:
            body = getBodyFromSource()
        except google.appengine.api.urlfetch_errors.DownloadError:
            print "Could not load data, sorry I tried really hard"
            exit()
    return body

def getBody():
    time = memcache.get("time")
    if time is None:
        memcache.add(key="time", value=True, time=60)
        try:
            return getBodyFromSource()
        except google.appengine.api.urlfetch_errors.DownloadError:
            return getBodyFromMemcache()
        
    else:
        return getBodyFromMemcache()
        
def getHour(body):
    regex = re.compile('hour=\'([0-9:]+)\'')
    return regex.search(body)

def getStations(body):
    regex = re.compile('station=\{id:"([0-9]+)",name:"([^"]+)",lat:"([^"]+)",long:"([^"]+)",nbBikes:"([0-9]+)",nbEmptyDocks:"([0-9]+)",installed:"(true|false)",locked:"(true|false)",temporary:"(true|false)"')
    return regex.finditer(body)

