from cyclehire import *
import cgi

data = cgi.FieldStorage()

code = None
try:
    code = data["code"].value
except KeyError:
    pass

name = None
try:
    name = data["n"].value
except KeyError:
    pass

latlon = None
try:
    latlon = data["s"].value.split(",")
except KeyError:
    try:
        latlon = [data["lat"].value, data["lon"].value]
    except KeyError:
        pass

if not code and (not name or not latlon or not len(latlon) == 2):
    print "You must specify a querystring ?code=<num> to load station information"
    exit()

body = getBody()

hour = getHour(body)

iterator = getStations(body)

print "Content-Type: text/xml"
#print "Content-Type: text/plain"
print "Cache-Control: max-age=60, must-revalidate"
print
print '<?xml version="1.0" encoding="UTF-8"?>'
print '<station>'

if code:
    for station in iterator:
        try:
            if station.group(1) == code:
                print '<id>' + station.group(1) + '</id>'
                print '<name>' + cgi.escape(station.group(2)) + '</name>'
                print '<bikes>' + station.group(5) + '</bikes>'
                print '<empty>' + station.group(6) + '</empty>'
                print '<open>' + station.group(8) + '</open>'
                print '<updated>'+ hour.group(1) + '</updated>'
                break
        except:
            pass
else:
    done = False
    for station in iterator:
        #print station.group(2).lower().split(",")[0].strip()
        try:
            if station.group(2).lower().split(",")[0].strip() == name.lower().strip():
                print '<id>' + station.group(1) + '</id>'
                print '<name>' + cgi.escape(station.group(2)) + '</name>'
                print '<bikes>' + station.group(5) + '</bikes>'
                print '<empty>' + station.group(6) + '</empty>'
                print '<open>' + station.group(8) + '</open>'
                print '<updated>'+ hour.group(1) + '</updated>'
                done = True
                break
        except:
            pass
    
    if not done:
        for station in iterator:
            if ("%.5f" % float(latlon[0])) == ("%.5f" % float(station.group(3))) and ("%.5f" % float(latlon[1])) == ("%.5f" % float(station.group(4))):
            #if latlon[0] == station.group(3) and latlon[1] == station.group(4):
                print '<id>' + station.group(1) + '</id>'
                print '<name>' + cgi.escape(station.group(2)) + '</name>'
                print '<bikes>' + station.group(5) + '</bikes>'
                print '<empty>' + station.group(6) + '</empty>'
                print '<open>' + station.group(8) + '</open>'
                print '<updated>'+ hour.group(1) + '</updated>'
                print '<lat>' + station.group(3) + '</lat>'
                print '<lon>' + station.group(4) + '</lon>'
                break

print '</station>'

