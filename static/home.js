 "use strict";


// HIKE SEARCH - AUTOCOMPLETE 
$.get('/search', (res) => {
  // console.log(res)

  autocomplete(document.getElementById("hike-search-bar"), res);
  // autocomplete(($('#hike-search-bar')), res); 
});



// GOOGLE MAP - APPEARS WHEN USER IS LOGGED IN 
const latlng = {lat: 37.7749, lng: -122.4194};
// const latlng_list = []

// Initialize and add the map
function initAutocomplete() {

    // Hike coordinates
    // let hikeID = $("#hidden-hike-id").val()
            
    // The map, centered at given coordinates
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 5,
      center: latlng,
      mapTypeId: "roadmap"
      });

    $.get('/bookmarks/map.json', (data) => {
      // for item in bookmark_list 
      // add lat/lng to latlng dict 

        console.log("given coordinates are: ", data);

        // markers for bookmarked (saved) hikes
        let marker, i;
        
        for (i = 0; i < data.length; i++) {  

          console.log("BOOKMARKED coordinates are: ", data[i]['lat'], data[i]['lng']);

          console.log("hike_id is: ",data[i]['hike_id']); 


          marker = new google.maps.Marker({
            position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
            map: map,
            icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
            },
          });

          // OPTIONAL - INFO WINDOW POP UP 
          const infowindow = new google.maps.InfoWindow();

          google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
              infowindow.setContent(data[i]['hike_id']);
              infowindow.open(map, marker);
            }
          })(marker, i));

    
        }

    });

    $.get('/ratings/map.json', (data) => {
   
        // markers for completed hikes
        let marker, i;
        
        for (i = 0; i < data.length; i++) {  

          console.log("RATING coordinates are: ", data[i]['lat'], data[i]['lng']);

          marker = new google.maps.Marker({
            position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
            map: map,
            icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            },

          });
        };
    });


  };



// USER LOGIN - REMOVE CREATE ACCOUNT / LOGIN FORMS
$('#user-login').on('submit', (evt) => {
  evt.preventDefault(); 
  // console.log('test from user-login script');

  
  const formInputs = {
    'email': $('#login-email').val(),
    'password': $('#login-pass').val()
  };   
  // console.log(formInputs);

  $.post('/login', formInputs, (res) => {

    if (res == "You are logged in.") {
      $("#user-login").toggle(2000);   
      $("#create-account").toggle(2000);   
      // $('#userName').text(formInputs['email']);  

      // $("#flash-message").html(res);
      flash(res);

    






      // Add logout button to nav bar in 'base.html' 
      // $('#myNavbar-login').html('<li><a href="/logout">Logout</a></li>');

    

      $.get('/loggedin', (response) => {

        $(".homepage-loggedin").fadeOut(500, function() {
          $(this).html(response);
          $(this).fadeIn(500);
          initAutocomplete(); 
          $.get('/search', (res) => {
            autocomplete(document.getElementById("hike-search-bar"), res);
          });


        });
      


      });
    }

    else {
      // $("#flash-message").html(res);
      flash(res);
    }

  });

});


// ACCOUNT CREATION 
$('#create-account').on('submit', (evt) => {
  evt.preventDefault(); 
  // console.log('test from create-account script');
  
  const formInputs = {
    'email': $('#account-email').val(),
    'password': $('#account-pass').val()
  };   
  // console.log(formInputs);

  $.post('/users', formInputs, (res) => {

    // $("#flash-message").html(res);
    flash(res);
  });
});


// // Test getting all bookmark coordinates 
// $.get('/bookmarks/map.json', (res) => {
//   console.log("response is ", res)  // response is a list of dictionaries
//   $.each(res,function(index,value){ 
//     console.log(index, value);    
//     // index: 0, value: dictionary of lat, long and hike_id
//   });
// });

// Delete Bookmark 
$(".trash-bookmark").on('click', (evt) => {

  console.log('delete bookmark test');  
  console.log("evt is: ", evt);
  console.log("evt.target.value is: ", evt.target.value);


  const formInputs = {
    'hike-id' : evt.target.value
  }

  $.post("/delete_bookmark", formInputs, (res) => {
    console.log(res);

    // delete specific list item
    $(`#li-${formInputs['hike-id']}`).remove()
  });
});


// Delete Rating 
$(".trash-rating").on('click', (evt) => {

  console.log('delete rating test');  
  console.log("evt is: ", evt);
  console.log("evt.target.value is: ", evt.target.value);


  const formInputs = {
    'hike-id' : evt.target.value
  }

  $.post("/delete_rating", formInputs, (res) => {
    console.log(res);

    // delete specific list item
    $(`#li-${formInputs['hike-id']}`).remove()
  });
});