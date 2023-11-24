function getSyncScriptParams() {
    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length-1];
    var scriptName = lastScript;
    return {
        "lat" : scriptName.getAttribute('lat'),
        "lon" : scriptName.getAttribute('lon')
    };
}


var map = L.map('map').setView([getSyncScriptParams()["lat"], getSyncScriptParams()["lon"]], 11);

var maptype= 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png' 
var attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
// var maptype = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png' 
// var attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'

L.tileLayer(maptype, {attribution: attr}).addTo(map);