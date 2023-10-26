// This is the manager for the leaflet map for the site

/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function myFunction() {
    var x = document.getElementById("topnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}


// coordinates = (latitude, longitude)
function createMap(coordinates, zoomLevel) {
    try {
        let map = L.map('map').setView(coordinates, zoomLevel)

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copywrite">OpenStreetMap</a>',
        }).addTo(map);
        createRedMarker(map)
        return map
    } catch (err) {
        console.log('There was an error creating the map ' + err)
    }
}


// marker from the map click event
function createRedMarker(map) {
    let redMarker = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    redMarkerClicker(redMarker, map)
}


function redMarkerClicker(redMarker, map) {
    const latitudeInput = document.querySelector('#latitude-input')
    const longitudeInput = document.querySelector('#longitude-input')
    let marker = null

    map.on('click', function(mapEvent) {
        const latLng = mapEvent.latlng  
        latitudeInput.value = latLng.lat
        longitudeInput.value = latLng.lng
        if (marker != null) {
            map.removeLayer(marker)
        }
        marker = L.marker([latitudeInput.value, longitudeInput.value], {icon: redMarker}).addTo(map)
        map.panTo([latitudeInput.value, longitudeInput.value])
    })
}


// For the tabbed content
function openSource(evt, sourceName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(sourceName).style.display = "block";
    evt.currentTarget.className += " active";
}

