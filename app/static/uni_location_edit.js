var map=null;

$( document ).ready(function() {
  $("#location_selector_collapse").on("shown.bs.collapse", function(){
    if (map == null) {
      latlong = $data["latlong"].split(",")
      lat = parseFloat(latlong[0])
      long = parseFloat(latlong[1])
      map = initmap(lat, long, getIcon());

      map.map.on("click", function(e) {
        map.marker.setLatLng(e.latlng);

        $("#university_latlong").val(e.latlng.lat + "," + e.latlng.lng);
      });
    }
  });
});
