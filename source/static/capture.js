/**
Handles client-side interaction, primarily capturing the image.

@author: Elias Gabriel
@revision: v1.1
**/
const ENDPOINT = '/snapshot';

document.body.onkeyup = function(e) {
    if(e.keyCode == 32) {
		let canvas = document.createElement('canvas');
		let im = document.getElementById("capture");
		let bb = im.getBoundingClientRect();
		canvas.width = bb.width;
		canvas.height = bb.height;

		let context = canvas.getContext('2d');
		context.scale(-1, 1);
		context.drawImage(im, 0, 0, -bb.width, bb.height);
	
		let data = new FormData();
		data.append('URI', canvas.toDataURL('image/jpeg'));
		fetch(ENDPOINT, {
			method: "POST",
			body: data
		}).then(() => window.location.replace('/show'));
	}
};
