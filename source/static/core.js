/**
Handles all the client-side interaction, primarily file drag and drop and upload.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
**/
const ENDPOINT = "/capture";

// Wrap all JS in a function to protect scopes
(function() {
	let dropzone = document.getElementById('dropzone');
	['dragenter', 'dragover', 'dragleave'].forEach(e => dropzone.addEventListener(e, preventDefaults, false));
	
	function preventDefaults(e) {
		/* Stops all default event propogation, as to avoid undesired behaviors. */
		e.preventDefault();
		e.stopPropagation();
	}
	
	// Add event listener for the `drop` event, to pass files to the file handler
	dropzone.addEventListner('drop', e => {
		preventDefaults(e);
		uploadFiles(e.dataTransfer.files);
	}, false);

	function uploadFiles(files) {
		/* Uploads files to the sever-side endpoint, error catching if something goes wrong. */
		let formData = new FormData();
		// Append each file to the request body, naming each one by index
		[...files].forEach(f, i => formData.append('images[]', f, i + file.name.slice(file.name.lastIndexOf('.') + 1))
		
		// Send request to the server
		fetch(ENDPOINT, {
			method: 'POST',
			body: formData
		}).catch(() => (document.getElementById("error").style.visibility = "visible"));
	}
})();
