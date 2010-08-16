import urllib2, re, time
from google.appengine.api import memcache
import google.appengine.api.urlfetch_errors
from google.appengine.api import urlfetch

url = "https://web.barclayscyclehire.tfl.gov.uk/maps"

def getBodyFromSource():
    
    body = None
    
    result = urlfetch.fetch(url, headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.125 Safari/533.4',
        'Cookie': 'lchssession=ptg3rt7agfjn1o0fb97h5ucu30; lchscookie=8GWR+vVYVvgA4zorlxsKZHUNJJf5D3yP0alCje16Wook/8LycoQ1kp4ChDilU7ERP5PsoD1qr9fL+g==; TS7a8c97=a453e668928323c382383038186169ba1ef6bf3601842a764c5c7eb2d8ab25308e56355aea3035482dbd56d6'
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

