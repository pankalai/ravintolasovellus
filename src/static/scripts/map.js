var latitude;
var longitude;
var user_location = false;
var markers;

// Asking user location
if (localStorage.getItem("location_asked") == null) {

    if ("geolocation" in navigator) {

        navigator.geolocation.getCurrentPosition(function(position) {
            
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            localStorage.setItem("latitude", latitude);
            localStorage.setItem("longitude", longitude);
            localStorage.setItem("location_asked", true);

            execute()
        }, function(error) {
            
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    console.error("User denied the request for geolocation.");
                    localStorage.setItem("location_asked", true);
                    break;
                case error.POSITION_UNAVAILABLE:
                    console.error("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    console.error("The request to get user location timed out.");
                    break;
                case error.UNKNOWN_ERROR:
                    console.error("An unknown error occurred.");
                    break;
            }
            execute()
        });
    } else {
        console.error("Geolocation is not available in this browser.");
    }
  
} else {
    execute()
}


function getSyncScriptParams(name) {
    var scripts = document.getElementsByTagName("script");
    var lastScript = scripts[scripts.length-1];
    var scriptName = lastScript;
    return scriptName.getAttribute(name)
}


function setCenter() {

    if (localStorage.getItem("latitude") != null || localStorage.getItem("longitude") != null) {
        latitude = localStorage.getItem("latitude")
        longitude = localStorage.getItem("longitude")
        user_location = true
    } else {
        latitude = getSyncScriptParams("lat")
        longitude = getSyncScriptParams("lon")
    }

}


function drawMap() {
    var zoom;
    if (user_location) {
        zoom = 13
    } else {
        zoom = 9
    }
    var map = L.map("map").setView([latitude, longitude], zoom);

    var maptype= "http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png" 
    var attr = "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors, &copy; <a href='http://cartodb.com/attributions'>CartoDB</a>"

    // var maptype = "https://tile.openstreetmap.org/{z}/{x}/{y}.png" 
    // var attr = "&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>"

    L.tileLayer(maptype, {attribution: attr}).addTo(map);

    markers = getSyncScriptParams("markers");
    markers = Array.from(eval(markers));
    markers.forEach((marker) => {
        var m = L.marker([marker.lat, marker.lon]).addTo(map)
        m.bindPopup(marker.info)
        m.bindTooltip(marker.name)
    });

}

function execute() {
    setCenter();
    drawMap();
}


