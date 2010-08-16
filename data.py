from models import Event

import cgi, re
from google.appengine.ext import db
from datetime import datetime

querystring = cgi.FieldStorage()
try:
    if re.match("[0-9]+", querystring['t'].value):
        
        dt = float(querystring['t'].value)
        
        fromTime = int(dt / 900) * 900
        toTime = fromTime + 900
        
        q = db.GqlQuery("SELECT * FROM Event WHERE time >= DATETIME('" + str(datetime.fromtimestamp(fromTime)) + "') AND time < DATETIME('" + str(datetime.fromtimestamp(toTime)) + "')")
        
        events = q.fetch(400)
        
        #print "Content-Type: text/xml"
        print "Content-Type: text/plain"
        #print "Cache-Control: max-age=60, must-revalidate"
        print
        print '<?xml version="1.0" encoding="UTF-8"?>'
        print '<events>'
        
        for event in events:
            print '<event>'
            print '<station>' + str(event.station) + '</station>'
            print '<bikes>' + str(event.event) + '</bikes>'
            print '</event>'
        
        print '</events>'

except KeyError:
    print
    print 'You must give a valid datetime'
    pass
