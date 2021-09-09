 "use strict";

// Example - fade out the Welcome header 
  // $("#myHeader").toggle(2000);
 
// Example - alert when clicking on hike search button
  // $('#hike-search').on('submit', () => {
  //   alert('testing 2');
  // });

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
    // alert(res);

    if (res == "You are logged in.") {
      $("#user-login").toggle(2000);   
      $("#create-account").toggle(2000);   
      $('#userName').text(formInputs['email']);
    };

      $.get('/loggedin', (response) =>{
        $(".homepage-loggedin").html(response);
        // console.log(response);
        // alert('logged in resposne');
      });

      // $('#myNavbar-login').css("visibility", "visible");
      // $('#myNavbar-login').text("Logout");

  
    });
  });

// GOOGLE MAP - APPEARS WHEN USER IS LOGGED IN 

const latlng = {lat: 37.7749, lng: -122.4194};
// const latlng_list = []

// Initialize and add the map
function initAutocomplete() {

    // Hike coordinates
    // let hikeID = $("#hidden-hike-id").val()
            
    // The map, centered at given coordinates
    var map = new google.maps.Map(document.getElementById("map"), {
      zoom: 5,
      center: latlng,
      mapTypeId: "roadmap"
      });

    $.get('/bookmarks/map.json', (data) => {
      // for item in bookmark_list 
      // add lat/lng to latlng dict 

        console.log("given coordinates are: ", data);

        // markers for bookmarked (saved) hikes
        var marker, i;
        
        for (i = 0; i < data.length; i++) {  

          console.log("BOOKMARKED coordinates are: ", data[i]['lat'], data[i]['lng']);

          marker = new google.maps.Marker({
            position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
            map: map,
            icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            },
          });
        }
    });

    $.get('/ratings/map.json', (data) => {
   
        // markers for completed hikes
        var marker, i;
        
        for (i = 0; i < data.length; i++) {  

          console.log("RATING coordinates are: ", data[i]['lat'], data[i]['lng']);

          marker = new google.maps.Marker({
            position: new google.maps.LatLng(data[i]['lat'], data[i]['lng']),
            map: map,
          });
        };
    });


  };

    
  // Test getting all bookmark coordinates 
  $.get('/bookmarks/map.json', (res) => {
    console.log("test___test____test____test");
    console.log("response is ", res)  // response is a list of dictionaries
    $.each(res,function(index,value){ 
      console.log(index, value);    
      // index: 0, value: dictionary of lat, long and hike_id
   });
    
  });