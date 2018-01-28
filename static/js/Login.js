//function save(dialog) {
//			for (var i=0; i<form1.elements.length-2; i++){
//			localStorage.setItem(form1.elements[i].name,form1.elements[i].value);
//			}
//		dialog.dismiss();
//	return false;
//}

function details() {
	var name = document.getElementById("name").value;
	var password = document.getElementById("password").value;
	localStorage.setItem("name", name);
	localStorage.setItem("password", password);
}


window.onload = function details() {
    var currentuser = localStorage.getItem("name");
	document.getElementById("now").innerHTML = currentuser;
};