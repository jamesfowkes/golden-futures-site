var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

var universityIcon = L.icon({
    iconUrl: $data["university_icon_path"],
    iconSize:     [20, 20], // size of the icon
});

function initmap(lat, long) {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 1, maxZoom: 18, attribution: osmAttrib});		

	// start the map in South-East England
	map.setView(new L.LatLng(lat, long), 14);
	map.addLayer(osm);

	marker = L.marker([lat, long], {icon: universityIcon})
	
	marker.on('click', function(e) {
		url = "http://www.openstreetmap.org/?mlat=" + this.getLatLng().lat + "&mlon=" + this.getLatLng().lng + "&zoom=14";
		window.open(url);
	});

	marker.addTo(map)

}

$( document ).ready(function() {
	latlong = $data["latlong"].split(",")
	lat = parseFloat(latlong[0])
	long = parseFloat(latlong[1])
	map = initmap(lat, long);
});
