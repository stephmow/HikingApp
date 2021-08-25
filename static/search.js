 "use strict";

// Example - fade out the Welcome header 
// $("#myHeader").toggle(2000);
 
// Example - alert when clicking on hike search button
$('#hike-search').on('click', (evt) => {
  alert('testing 2');
});

// Example - test '/test' and add in my name to the welcome header
  // $.get('/test', (evt) => {
  //   $('#userName').text(evt);
  // });

// Example - for logged in page 
$('#user-login').on('submit', (evt) => {
  evt.preventDefault(); 
  console.log('test from user-login script');

  const formInputs = {
    'email': $('#login-email').val(),
    'password': $('#login-pass').val()
  };   
  console.log(formInputs);

  $.post('/login', formInputs, (res) => {
    alert(res);
    $("#user-login").toggle(2000);   
    $("#create-account").toggle(2000);   
    $('#userName').text("add user email here");
    });

  });

