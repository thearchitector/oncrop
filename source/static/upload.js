/**
Handles client-side interaction, primarily file drag and drop and upload.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0.1
**/
const ENDPOINT = "/upload";
const REDIRECT = "/marker";

// find the box by div id
let dropzone = document.getElementById('dropzone');
// allow script to understand what files are being dragged over the div
['dragenter', 'dragover', 'dragleave'].forEach(e => dropzone.addEventListener(e, preventDefaults, false));

// avoid undesirable behaviours
function preventDefaults(e) {
	/* Stops all default event propagation, as to avoid undesired behaviors. */
	e.preventDefault();
	e.stopPropagation();
}

// Add event listener for the `drop` event, to pass files to the file handler
dropzone.addEventListener('drop', e => {
	preventDefaults(e);
	uploadFiles(e.dataTransfer.files);  // from the drop event, .files is a list of all files that have been uploaded
}, false);

function uploadFiles(files) {
	/* Uploads files to the sever-side endpoint, error catching if something goes wrong. */
	let formData = new FormData();  // creates class to store data
	if (files.length !== 1) {  // check to make sure that only one file has been uploaded
		document.getElementById("error").style.visibility = "visible"
	} else {
		// Append each file to the request body, naming each one by index
		Array.from(files).forEach((f, i) => formData.append('images[]', f));

  		// Send request to the server
  		fetch(ENDPOINT, {
			method: 'POST',
			body: formData
  		}).then(data => window.location.replace(REDIRECT))  // data is the json success message
			.catch(() => (document.getElementById("error").style.visibility = "visible"));
	}

}
