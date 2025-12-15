let map;
let markers = [];

function initMap() {
    // Center Sri Lanka
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 7.8731, lng: 80.7718 },
        zoom: 7,
    });

    // Add markers for recommended places
    addMarkers();
}

function addMarkers() {
    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));
    markers = [];

    // Add new markers if places are available
    if (window.recommendedPlaces && window.recommendedPlaces.length > 0) {
        window.recommendedPlaces.forEach(place => {
            const marker = new google.maps.Marker({
                position: { lat: place.lat, lng: place.lng },
                map: map,
                title: place.name
            });
            markers.push(marker);
        });

        // Adjust map bounds to show all markers
        const bounds = new google.maps.LatLngBounds();
        markers.forEach(marker => bounds.extend(marker.getPosition()));
        map.fitBounds(bounds);
    }
}
