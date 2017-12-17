//function save(dialog) {
//			for (var i=0; i<form1.elements.length-2; i++){
//			localStorage.setItem(form1.elements[i].name,form1.elements[i].value);
//			}
//		dialog.dismiss();
//	return false;
//}

function details() {
	var inputname = document.getElementById("name").value;
	var inputcontact = document.getElementById("contact").value;
	var inputemail = document.getElementById("email").value;
	localStorage.setItem("name", inputname);
	localStorage.setItem("contact", inputcontact);
	localStorage.setItem("email", inputemail);
}


window.onload = function details() {
    var currentuser = localStorage.getItem("name");
	document.getElementById("now").innerHTML = currentuser;
};