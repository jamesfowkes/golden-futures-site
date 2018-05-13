function getIcon(path=null, size=null) {
	if (path === null) {
		path = $data["university_icon_path"]
	}

	if (size === null) {
		size = [20, 20]
	}

	return new L.icon({
    	iconUrl: path,
    	iconSize: size
	});
}

function initmap() {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 1, maxZoom: 18, attribution: osmAttrib});		

	map.addLayer(osm);
	return map
}

function add_icon(map, lat, long, icon, marker_url, tooltip="") {
	marker = new L.marker([lat, long], {icon: icon, title: tooltip})
	
	if (marker_url !== null) {
		marker.on('click', function(e) {
			url = marker_url;
			window.open(url);
		});
	}

	marker.addTo(map)

	return marker
}
