from cyclehire import *
import cgi

data = cgi.FieldStorage()

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

if not name or not latlon or not len(latlon) == 2:
    print "You must specify a querystring ?n=<name>&s=<lat>,<lon> to load station information"
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

done = False
for station in iterator:
    if station.group(2).lower() == name.lower():
        print '<name>' + cgi.escape(station.group(2)) + '</name>'
        print '<bikes>' + station.group(5) + '</bikes>'
        print '<empty>' + station.group(6) + '</empty>'
        print '<open>' + station.group(8) + '</open>'
        print '<updated>'+ hour.group(1) + '</updated>'
        print '<lat>' + station.group(3) + '</lat>'
        print '<lon>' + station.group(4) + '</lon>'
        done = True
        break

if not done:
    for station in iterator:
        if ("%.5f" % float(latlon[0])) == ("%.5f" % float(station.group(3))) and ("%.5f" % float(latlon[1])) == ("%.5f" % float(station.group(4))):
        #if latlon[0] == station.group(3) and latlon[1] == station.group(4):
            print '<name>' + cgi.escape(station.group(2)) + '</name>'
            print '<bikes>' + station.group(5) + '</bikes>'
            print '<empty>' + station.group(6) + '</empty>'
            print '<open>' + station.group(8) + '</open>'
            print '<updated>'+ hour.group(1) + '</updated>'
            print '<lat>' + station.group(3) + '</lat>'
            print '<lon>' + station.group(4) + '</lon>'
            break

print '</station>'

