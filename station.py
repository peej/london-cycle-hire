from cyclehire import *
import cgi

data = cgi.FieldStorage()
try:
    latlon = data["s"].value.split(",")
except KeyError:
    try:
        latlon = [data["lat"].value, data["lon"].value]
    except KeyError:
        pass
if not latlon or not len(latlon) == 2:
    print "You must specify a querystring ?s=<lat>,<lon> to load station information"
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

for station in iterator:
    if ("%.4f" % float(latlon[0])) == ("%.4f" % float(station.group(3))) and ("%.4f" % float(latlon[1])) == ("%.4f" % float(station.group(4))):
        print '<name>' + cgi.escape(station.group(2)) + '</name>'
        print '<bikes>' + station.group(5) + '</bikes>'
        print '<empty>' + station.group(6) + '</empty>'
        print '<open>' + station.group(8) + '</open>'
        print '<updated>'+ hour.group(1) + '</updated>'
        print '<lat>' + station.group(3) + '</lat>'
        print '<lon>' + station.group(4) + '</lon>'
        break

print '</station>'

