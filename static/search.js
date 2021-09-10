 "use strict";


// Function for autocomplete 
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
} 

// Example - fade out the Welcome header 
  // $("#myHeader").toggle(2000);
 
// Example - alert when clicking on hike search button
  // $('#hike-search').on('submit', () => {
  //   alert('testing 2');
  // });


// HIKE SEARCH - AUTOCOMPLETE 
$.get('/search', (res) => {
  // console.log('search test')
  // console.log(res)

  autocomplete(document.getElementById("hike-search-bar"), res);

  // autocomplete(($('#hike-search-bar')), res);

  
});

// const test = ['apple', 'berry', 'cherry']

// autocomplete(document.getElementById("hike-search-bar"), test);







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
      $('#userName').text(formInputs['email']);

      $("#flash-message").html(res);

      // hide flash message after 3 seconds 
      $(document).ready(function(){
        setTimeout(function(){
            $("#flash-message").hide("2000")
            }, 3000);
      });

      $.get('/loggedin', (response) => {
        $(".homepage-loggedin").html(response);
        // console.log(response);
        // alert('logged in resposne');
      });

      // $('#myNavbar-login').css("visibility", "visible");
      // $('#myNavbar-login').text("Logout");
  
    }

    else {
      $("#flash-message").html(res);

      // hide flash message after 3 seconds 
      $(document).ready(function(){
        setTimeout(function(){
            $("#flash-message").hide("2000")
            }, 3000);
      });
    }

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

});

    
  // Test getting all bookmark coordinates 
  $.get('/bookmarks/map.json', (res) => {
    console.log("test___test____test____test");
    console.log("response is ", res)  // response is a list of dictionaries
    $.each(res,function(index,value){ 
      console.log(index, value);    
      // index: 0, value: dictionary of lat, long and hike_id
   });
    
  });




