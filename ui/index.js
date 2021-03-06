
var load_images_db = function (db_path) {
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
	var result = null
	$.ajax({
		url: db_path,
		async: false,
		success: function (csvd) {
			data = $.csv2Array(csvd);
			console.log("load_images_db: Success!")
			console.log(data)
			result = data
		},
		dataType: "text",
		complete: function () {
			// call a function on complete 
		}
	});
	console.log("End load_images_db")
	return result
}


var infowindowOpen = null

function showThumb(data){
	//trace un marqueur
	var placeholder = "thumbs/20141017_131027_Richtone(HDR).jpg"
	var img_url = data[4].replace("./ui", "")
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(data[2], data[3]),
		map: googleMap,
		title: "Pictures tagged here (@TODO replace by name of area?)",
		icon: img_url
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
	return marker
}

var start = function () {
	pictures = load_images_db("/thumbs/heyhey.csv")
	var mapOptions = {
		center: { lat: 41.41361111111111, lng: 2.1530555555555555}, 
		zoom: 9
	};
	googleMap = new google.maps.Map(document.getElementById("googleMap"),mapOptions);
	
	var markers = []
	for (var i = pictures.length - 1; i >= 0; i--) {
		markers.push(showThumb(pictures[i]))
	};

	markerClusterer = new MarkerClusterer(googleMap, markers, {
	  maxZoom: 10,
	  gridSize: null,
	});
}

google.maps.event.addDomListener(window, 'load', start);