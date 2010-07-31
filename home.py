print """
<html>
<head>
    <title>London Cycle Hire</title>
</head>
<body>
<h1>London Cycle Hire</h1>
<p><a href="/kml">Get the KML file</a>, updated every minute with live data</p>
<form method="get" action="/station">
    <p>Get live station information</p>
    <label>Station name: <input name="n" type="text" value="River Street , Clerkenwell"></label><br>
    <label>Station latitude: <input name="lat" type="text" value="51.52916347"></label><br>
    <label>Station longitude: <input name="lon" type="text" value="-0.109970527"></label><br>
    <input type="submit">
</form>

<h2>Interactive map</h2>
<div id="map" style="width: 600px; height: 400px;"></div>
<p><a href="http://maps.google.com/?q=http://londoncyclehire.appspot.com/kml">View on Google Maps</a></p>
<script src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script>
window.onload = function () {
    var myOptions = {
        zoom: 12,
        center: new google.maps.LatLng(51.5006, -0.1308),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), myOptions);
    
    var kml = new google.maps.KmlLayer('http://londoncyclehire.appspot.com/kml');
    kml.setMap(map);
};
</script>

<h2>Get the Android app</h2>
<img src="/_/qr.jpg" alt="London Cycle Hire Android app download QR code">
</body>
</html>
"""
