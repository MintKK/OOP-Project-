// Initialize Firebase
  var config = {
    apiKey: "AIzaSyDHDEfsJT-eOjxv5iv3ShEuawYkHpzizyM",
    authDomain: "oopp-c6fcf.firebaseapp.com",
    databaseURL: "https://oopp-c6fcf.firebaseio.com",
    projectId: "oopp-c6fcf",
    storageBucket: "oopp-c6fcf.appspot.com",
    messagingSenderId: "907051099185"
  };
  firebase.initializeApp(config);

  var messagesRef = firebase.database().ref('message');

// listen for form submit
document.getElementById('contactForm').addEventListener('submit',submitForm);

function submitForm(e) {
    e.preventDefault();

   //get value
    var name = getInputVal('name');
    var email = getInputVal('email');
    var phone = getInputVal('phone');
    var message = getInputVal('message');

    //save message
    saveMessage(name,phone,email,message);
}

// function to get get for val
function getInputVal(id){
    return document.getElementById(id).value;
}

//save ,message to firebase
function saveMessage(name,email,phone,message){
    var newMessageRef = messagesRef.push();
    alert('test')
    newMessageRef.set({
        name:name,
        email:email,
        phone:phone,
        message:message
    });
}
