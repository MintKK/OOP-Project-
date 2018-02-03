$(document).ready(function(){
    $("#name2").html(localStorage.getItem('name2'));      // get item from local storage
    $("#email").html(localStorage.getItem('email'));
    $("#phone").html(localStorage.getItem('phone'));
    $("#message").html(localStorage.getItem('message'));
    $("#home").click(function(){       //when its clicked run the function
        localStorage.clear();      //clear so that it only displays one thing
        window.location.href="/ss";   //redirect to ss
    });
});