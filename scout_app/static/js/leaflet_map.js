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


function createMap(coordinates, zoomLevel) {
    try {
        let map = L.map('map').setView(coordinates, zoomLevel)

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copywrite">OpenStreetMap</a>',
        }).addTo(map);
        return map
    } catch (err) {
        console.log('There was an error creating the map ' + err)
    }
}







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

function displayYelpData(map, yelp_display_data) {

        try {

            // // regex uses look-forwards and look-behinds to select only single-quotes that should be selected
            // // https://stackoverflow.com/posts/69597114/revisions
            // const regex = /('(?=(,\s*')))|('(?=:))|((?<=([:,]\s*))')|((?<={)')|('(?=}))/g

            // // replace single quotes to double quotes but keep 's
            // let regexYelpData = yelpApiDataset.replace(regex, '"')
            // // replace slash with a space
            // // https://stackoverflow.com/questions/2479309/javascript-and-backslashes-replace
            // let removeSlashYelpData = regexYelpData.replace(/\\/, " ")
            // // parse data
            // let yelp_display_data = JSON.parse(removeSlashYelpData)
            
            // for loop to add yelp data to the map markers

            for (let categoryType of venues) {
                if (categoryType.data.length > 0) {
                    for (let element of categoryType.data) {
                        console.log(element)
                        // // L.marker([data.coordinates.latitude, data.coordinates.longitude]).addTo(markerFeatureGroup)                
                        // let markerText = `
                        //                 <div><img style="width: 200px;" src="${element['image']}"></div>
                        //                 <div><strong>${element['name']}</strong>
                        //                 <div>${element['phone']}</div> 
                        //                 <div>${element['full_address']}</div>
                        //                 <div>${element['rating']} out of 5 stars (${element['review_count']} reviews)</div>
                        //                 <div><a href="${element['url']}" target="_blank">More info</a></div>
                        //                 `
                        // L.marker([element['latitude'], element['longitude']]).bindPopup(markerText).addTo(map)
                        // // L.marker([data.coordinates.latitude, data.coordinates.longitude]).addTo(markerFeatureGroup)                

            
                        // let marker = new L.Icon({
                        //     iconUrl: categoryType.image_url,
                        //     shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        //     iconSize: [25, 41],
                        //     iconAnchor: [12, 41],
                        //     popupAnchor: [1, -34],
                        //     shadowSize: [41, 41]
                        //   });
                        // map.setView([latitudeCoordinates, longitudeCoordinates], 12)
                        // L.marker([latitudeCoordinates, longitudeCoordinates], {icon: marker}).addTo(map)
                    }
                }
    
            }     
            return map   
    
        } catch (err) {
            console.log(err.message)
        }
    
}