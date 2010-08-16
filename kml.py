from cyclehire import *
import cgi

body = getBody()

hour = getHour(body)

iterator = getStations(body)

print "Content-Type: application/vnd.google-earth.kml+xml"
#print "Content-Type: text/plain"
print "Cache-Control: max-age=60, must-revalidate"
print
print '<?xml version="1.0" encoding="UTF-8"?>'
print '<kml xmlns="http://www.opengis.net/kml/2.2">'
print '<Document>'
print '<name>London Cycle Hire</name>'
print '<description>List of stations and their availability</description>'

for station in iterator:
    print '<Placemark id="' + station.group(1) + '">'
    print '<name>' + cgi.escape(station.group(2)) + '</name>'
    print '<description><![CDATA['
    print '<p>Number of bikes: ' + station.group(5) + '</p>'
    print '<p>Number of empty docks: ' + station.group(6) + '</p>'
    if station.group(8) == "true":
        print '<p><strong>Station not in operation</strong></p>'
    print '<p>Last updated at: '+ hour.group(1) + '</p>'
    print ']]></description>'
    print '<Point>'
    print '<coordinates>' + station.group(4) + ',' + station.group(3) + ',0</coordinates>'
    print '</Point>'
    print '</Placemark>'

print '</Document>'
print '</kml>'
