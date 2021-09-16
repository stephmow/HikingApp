 "use strict";

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
    
        // console.log("Hike #", hikeID, "coordinates are: ", data);

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

// Call google map function 
initAutocomplete();

// Hide ratings until user clicks hike has been completed 
$('#ratings').hide(); 

// Add bookmark for Saved Hike
$('#bookmarks').on('click', (evt) => {
  evt.preventDefault();  

  // If 'Completed this hike'
  if ($("input[type=radio][name=bookmark]:checked").val() === "True") {
    // alert('hike completed, now you can rate it'); 
    $('#ratings').show();
    $('#bookmarks').hide();
  }

  else if ($("input[type=radio][name=bookmark]:checked").val() === "False") {
    // alert('hike saved'); 

    let hikeID = $("#hidden-hike-id").val()
    let url = "/hikeList/" + hikeID + "/add_bookmark"
    
    // get <hike_id> from hike_details.html bookmark form 
    $.post(url, {is_completed: "False"}, (res) => {
      $('#bookmarks-header').html(res);
    });
  }

  else {
    alert("enter in something please");  
  }

});


// Add rating for completed hike
// function addRating() {
//   $('#ratings').hide()
// };

$('#ratings').on('submit', (evt) => {
  evt.preventDefault();  

  let rating = $("input[type=radio][name=rating]:checked").val()
  // console.log(rating);
  let comments = $("#ratings input[name=comments").val()

  let hikeID = $("#hidden-hike-id").val()
  let url = "/hikeList/" + hikeID + "/add_rating"

  // console.log(url)

  $.post(url, {is_completed: "True", rating: rating, comments: comments}, (res) => {
    $('#bookmarks-header').html(res);
  });
});