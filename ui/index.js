

function showThumb(){
	//trace un marqueur
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(this.velov_lat, this.velov_long),
		map: googleMap,
		title: "Pictures tagged here (@TODO replace by name of area?)",
		icon: "/tmp/placeholder.jpg"
	});

	var contentString = '<img src="/tmp/placeholder.jpg" />'

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
	var mapOptions = {
		zoom: 14
	};
	googleMap = new google.maps.Map(document.getElementById("googleMap"),mapOptions);

	showThumb()
}

document.onload = start