"use strict"

const latlng = {lat: 0, lng: 0};

// Initialize and add the map
function initAutocomplete() {

    // Hike coordinates
    let hikeID = $("#hidden-hike-id").val()
    let url = "/hikeList/" + hikeID + "/map.json"

    $.get(url, (data) => {
        latlng['lat'] = data['lat']
        latlng['lng'] = data['lng']
    
        console.log("Hike #", hikeID, "coordinates are: ", data);

    // The map, centered at given coordinates
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 8,
        center: latlng,
        mapTypeId: "roadmap"
        
    });

    // The marker, positioned at given coordinates
    const marker = new google.maps.Marker({
        position: latlng,
        map: map,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        }
    });

    });
    };
