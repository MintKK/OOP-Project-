$(document).ready(function(){   // when the document is ready run the functions below
    $("#submitBtn").click(function(){  //when you click the button run that function
        localStorage.setItem('name2',$("#name2").val());   //set value
        localStorage.setItem('email',$("#email").val());
        localStorage.setItem('phone',$("#phone").val());
        localStorage.setItem('message',$("#message").val());
        alert('Your message has been sent. \n Thank you!');
    });
});