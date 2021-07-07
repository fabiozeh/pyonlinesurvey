function take_part() {
	const form = document.getElementById('contact-form');
	const thanks = document.getElementById('response-thanks');
	const msg = document.getElementById('response-message');
	const fd = new FormData(form);
	
	var req = new XMLHttpRequest();
	
	req.onreadystatechange = function() {
    	if (this.readyState == 4){
    		if (this.status == 200) {
       			form.style.display = "none";
       			thanks.style.display = "";
       		}
       		else {
       			msg.innerHTML = req.responseText
       			msg.style.display = "";
       			form.elements.forEach(element => element.disabled = false);
       		}
    	}
	};
	req.open("POST", form.action, true);
	req.send(fd);
	form.elements.forEach(element => element.disabled = true);
}

function fetch_step(event) {
	event.preventDefault();
	const main_div = document.getElementById('main_div');
	const form = document.getElementById('survey-form');

	var req = new XMLHttpRequest();
	
	req.onreadystatechange = function() {
    	if (this.readyState == 4){
    		if (this.status == 200) {
       			main_div.innerHTML = req.responseText
       		}
       		else {
       			//same...
       			main_div.innerHTML = req.responseText
       		}
    	}
	};
	if (form) {
		const fd = new FormData(form);
		req.open("POST", "xp-data", true);
		req.send(fd);
	}
	else {
		req.open("GET", "xp-steps", true);
		req.send();
		// loading element?
	}
	return false;
}