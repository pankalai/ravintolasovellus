// Check if geolocation is available in the browser
if ("geolocation" in navigator) {
    // Get the user's current location
    navigator.geolocation.getCurrentPosition(function(position) {
        // The user's latitude and longitude are in position.coords.latitude and position.coords.longitude
        const latitude = position.coords["latitude"];
        const longitude = position.coords.longitude;

        localStorage.setItem('latitude', latitude);
        localStorage.setItem('longitude', longitude);
        localStorage.setItem('location_asked', true);
        console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);

    }, function(error) {
        console.log(error.code == error.PERMISSION_DENIED)
        switch (error.code) {
            case error.PERMISSION_DENIED:
                console.error("User denied the request for geolocation.");
                localStorage.setItem('location_asked', true);
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
    });
} else {
    console.error("Geolocation is not available in this browser.");
}

window.history.back()