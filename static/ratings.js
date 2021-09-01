 "use strict";

// Test - hide ratings form 
$('#ratings').hide(); 

// Add bookmark for Saved Hike

$('#bookmarks').on('submit', (evt) => {
  evt.preventDefault();  
  console.log('test from bookmarks click')

  // if 'Completed this hike'
  if ($("input[type=radio][name=bookmark]:checked").val() === "True") {

    alert('hike completed, now you can rate it');

    $('#ratings').show();
    $('#bookmarks').hide();
  }

  else if ($("input[type=radio][name=bookmark]:checked").val() === "False") {

    alert('hike saved');
    let hikeID = $("#hidden-hike-id").val()
    let url = "/hikeList/" + hikeID + "/add_bookmark"
    console.log(url)
    // get <hike_id> from hike_details.html bookmark form 
    $.post(url, {is_completed: "False"});
  
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
  console.log('test from ratings submit click')

  let rating = $("#ratings input[name=rating").val()
  let comments = $("#ratings input[name=comments").val()

  console.log(rating);
  console.log(comments);

  let hikeID = $("#hidden-hike-id").val()
  let url = "/hikeList/" + hikeID + "/add_rating"

  console.log(url)

  $.post(url, {is_completed: "True", rating: rating, comments: comments});
});