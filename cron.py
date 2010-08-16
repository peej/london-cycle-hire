from cyclehire import *
from models import Event

from google.appengine.ext import db
from datetime import *

import logging
from google.appengine.api import quota

start = quota.get_request_cpu_usage()

#body = getBodyFromSource()
body = getBody()

hour = getHour(body)

iterator = getStations(body)

print "Content-type: text/plain"
print

for station in iterator:
    
    hr = hour.group(1).split(":")
    dt = datetime.combine(date.today(), time(int(hr[0]), int(hr[1])))
    
    stationKey = "station" + station.group(1)
    newBikeNumber = int(station.group(5))
    oldBikeNumber = memcache.get(stationKey)
    
    if oldBikeNumber != None:
        
        if oldBikeNumber != newBikeNumber:
            
            memcache.set(key=stationKey, value=newBikeNumber)
            
            print "event for " + stationKey + ": " + str(newBikeNumber - oldBikeNumber)
            logging.info("event for " + stationKey + ": " + str(newBikeNumber - oldBikeNumber))
            
            e = Event(
                station = int(station.group(1)),
                time = dt,
                event = newBikeNumber - oldBikeNumber
            )
            e.put()
            
    else:
        memcache.set(key=stationKey, value=newBikeNumber)
    
end = quota.get_request_cpu_usage()
logging.info("request cost %d megacycles." % (start - end))

