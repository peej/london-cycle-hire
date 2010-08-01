import urllib2, re, time
from google.appengine.api import memcache
import google.appengine.api.urlfetch_errors
from google.appengine.api import urlfetch

url = "https://web.barclayscyclehire.tfl.gov.uk/maps"

def getBodyFromSource():
    #http = urllib2.urlopen(url)
    #body = http.read()
    #http.close()
    
    body = None
    
    result = urlfetch.fetch(url, headers = {'Cache-Control': 'max-age=60'})
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

