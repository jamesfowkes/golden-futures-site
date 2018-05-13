var map=null;

$( document ).ready(function() {
  $("#location_selector_collapse").on("shown.bs.collapse", function(){
    if (map == null) {
      latlong = $data["latlong"].split(",")
      lat = parseFloat(latlong[0])
      long = parseFloat(latlong[1])
      map = initmap();
      marker = add_icon(map, lat, long, getIcon())
      map.on("click", function(e) {
        marker.setLatLng(e.latlng);
        $("#university_latlong").val(e.latlng.lat + "," + e.latlng.lng);
      });
      map.setView(new L.LatLng(lat, long), 14);
    }
  });
});
