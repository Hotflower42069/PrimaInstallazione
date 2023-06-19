window.addEventListener("load", page_loaded);

function page_loaded() {
	// checkboxes
	checkbox_google_chrome=document.getElementById("google_chrome");
	checkbox_mozilla_firefox=document.getElementById("mozilla_firefox");
	checkbox_7_zip=document.getElementById("7_zip");
	checkbox_adobe_reader=document.getElementById("adobe_reader");
	checkbox_vlc=document.getElementById("vlc");

	checkbox_uninstall_office=document.getElementById("uninstall_office");
	checkbox_windows_updates=document.getElementById("windows_updates");
	checkbox_windows_hello=document.getElementById("windows_hello");


	// start button
	start_button=document.getElementById("start");
	start_button.addEventListener("click", function(event) {
		checkbox_list=[checkbox_google_chrome, checkbox_mozilla_firefox, checkbox_7_zip, checkbox_adobe_reader, checkbox_vlc];
		packages=[];
		for(const element of checkbox_list) {
			if(element.checked) {
				packages.push({"name": element.getAttribute("data-screen-name"), "value": element.getAttribute("data-package-name")});
			}
		}

		// change buttons status
		start_button.querySelector(".spinner-border").hidden=false;
		start_button.querySelector(".text").textContent="Sto lavorando...";
		start_button.disabled=true;
		log_button.hidden=true;

		eel.main(packages, checkbox_uninstall_office.checked, checkbox_windows_updates.checked, checkbox_windows_hello.checked);
	});


	// log button
	log_button=document.getElementById("log");
	log_button.addEventListener("click", function(event) {
		eel.create_log_file();
	});
}

eel.expose(main_finished);
function main_finished() {
	// change buttons status
	start_button.querySelector(".spinner-border").hidden=true;
	start_button.querySelector(".text").textContent="Avvia";
	start_button.disabled=false;
	log_button.hidden=false;
}

// prevent window resizing
window.addEventListener("resize", function(){
	window.resizeTo(650, 700);
});