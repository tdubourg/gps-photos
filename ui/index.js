
var	load_images_db = function (db_path) {
	console.log("Start load_images_db")
	// Might be used later, but for now I'd rather not have any user input, so we'll just use a simplistic web server
	// to serve the files
	// // Check for the various File API support.
	// if (window.File && window.FileReader && window.FileList && window.Blob) {
	//   // Great success! All the File APIs are supported.
	// 
	// } else {
	//   alert('The File APIs are not fully supported in this browser. Your browser SUCKS!');
	// }
	$.ajax({
		url: db_path,
		async: false,
		success: function (csvd) {
			data = $.csv2Array(csvd);
			console.log("load_images_db: Success!")
			console.log(data)
		},
		dataType: "text",
		complete: function () {
			// call a function on complete 
		}
	});
	console.log("End load_images_db")
}


function showThumb(){
	//trace un marqueur
	var placeholder = "thumbs/20141017_131027_Richtone(HDR).jpg"
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(this.velov_lat, this.velov_long),
		map: googleMap,
		title: "Pictures tagged here (@TODO replace by name of area?)",
		icon: placeholder
	});

	var contentString = '<img src="' + placeholder + '" />'

	var infowindow = new google.maps.InfoWindow({
		content: contentString
	});

	google.maps.event.addListener(marker, 'click', function() {
		if (infowindowOpen){
			infowindowOpen.close();
		}
		infowindowOpen = new google.maps.InfoWindow({
			content: contentString
		});
		infowindowOpen.open(googleMap,marker);
	});
}

var start = function () {
	alert("HEY")
	load_images_db("/thumbs/heyhey.csv")
	var mapOptions = {
		zoom: 14
	};
	googleMap = new google.maps.Map(document.getElementById("googleMap"),mapOptions);
	showThumb()
}

document.ready = start