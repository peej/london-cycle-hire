import urllib2, re
from google.appengine.api import memcache
import google.appengine.api.urlfetch_errors


url = "https://web.barclayscyclehire.tfl.gov.uk/maps"


def getBodyFromSource():
    http = urllib2.urlopen(url)
    body = http.read()
    http.close()
    memcache.add(key="body", value=body)
    return body

def getBodyFromMemcache():
    body = memcache.get("body")
    if body is None:
        try:
            body = getBodyFromSource()
        except DownloadError:
            print "Could not load data, sorry I tried reall hard"
            exit()
    return body

def getBody():
    time = memcache.get("time")
    if time is None:
        memcache.add(key="time", value=True, time=60)
        try:
            return getBodyFromSource()
        except DownloadError:
            return getBodyFromMemcache()
        
    else:
        return getBodyFromMemcache()
        
def getHour(body):
    regex = re.compile('hour=\'([0-9:]+)\'')
    return regex.search(body)

def getStations(body):
    regex = re.compile('station=\{id:"([0-9]+)",name:"([^"]+)",lat:"([^"]+)",long:"([^"]+)",nbBikes:"([0-9]+)",nbEmptyDocks:"([0-9]+)",installed:"(true|false)",locked:"(true|false)",temporary:"(true|false)"')
    return regex.finditer(body)

