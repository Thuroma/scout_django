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


function createMap() {
    try {
        let map = L.map('search-map').setView([37.09024, -95.712891], 4)
        displayMap(map)
    } catch (err) {
        console.log('There was an error creating the map' + err)
    }
}

function displayMap(map) {
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copywrite">OpenStreetMap</a>',
    }).addTo(map)
}
