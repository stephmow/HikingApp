 "use strict";

/* Ajax get request to get all hikes from the search route.  Then Autocomplete success function is called which takes in: 
  (1) the search input provided by user 
  (2) search results from '/search' route  */
$.get('/search.json', (res) => {
  autocomplete(document.getElementById("hike-search-bar"), res);
  });

// Starting center position will be the Bay Area
const latlng = {lat: 37.7749, lng: -122.4194}; 

// Function for Google Map
function initAutocomplete() {

  // The map, centered at given coordinates
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 5,
    center: latlng,
    mapTypeId: "roadmap"
    });

  // Ajax get request for user's bookmarked hike coordinates
  $.get('/bookmarks/map.json', (data) => {
    // Markers for bookmarked (saved) hikes, show as yellow markers
    let marker, i;
    for (i = 0; i < data.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
        map: map,
        icon: {url: "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"},
        });
      }
    });

  // Ajax get request for user's completed hike coordinates
  $.get('/ratings/map.json', (data) => {
    // Markers for completed hikes, show as green markers
    let marker, i;
    for (i = 0; i < data.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
        map: map,
        icon: {url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"},
        });
      };
    });
  };

// Ajax Submit button for user login form. 
$('#user-login').on('submit', (evt) => {
  evt.preventDefault(); 
  const formInputs = {
    'email': $('#login-email').val(),
    'password': $('#login-pass').val()
    };   

  // Ajax post request if user successfully logs in, hide login forms 
  $.post('/login', formInputs, (res) => {
    if (res == "You are logged in.") {
      $("#user-login").toggle(2000);   
      $("#create-account").toggle(2000);   
      flash(res);

      // Ajax get request for logged in user's info including bookmarks and ratings with google map
      $.get('/loggedin', (response) => {
        $(".homepage-loggedin").fadeOut(500, function() {
          $(this).html(response);
          $(this).fadeIn(2000);
          initAutocomplete();
          $.get('/search.json', (res) => {
            autocomplete(document.getElementById("hike-search-bar"), res);
            });
          });
        });
      }

    else {
      flash(res);
      }
    });
  });

// Ajax submit button to create an account and flash message
$('#create-account').on('submit', (evt) => {
  evt.preventDefault(); 
  const formInputs = {
    'email': $('#account-email').val(),
    'password': $('#account-pass').val()
  };   

  // Ajax post request to create an account and flash message
  $.post('/users', formInputs, (res) => {
    flash(res);
    });
  });

// Ajax click to delete a bookmark 
$(".trash-bookmark").on('click', (evt) => {
  const formInputs = {
    'hike-id' : evt.target.value
    }
    
  // Ajax post request to delete the corresponding hike bookmark through backend route
  $.post("/delete_bookmark", formInputs, (res) => {
    // Visually remove the deleted hike line item
    $(`#li-${formInputs['hike-id']}`).remove()
    });
  });

// Ajax click to delete a rating 
$(".trash-rating").on('click', (evt) => {
  const formInputs = {
    'hike-id' : evt.target.value
    }
  // Ajax post request to delete the corresponding hike rating backend route
  $.post("/delete_rating", formInputs, (res) => {
    // Visually remove the deleted hike line item
    $(`#li-${formInputs['hike-id']}`).remove()
    });
  });