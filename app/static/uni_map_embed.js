var map=null;

$( document ).ready(function() {

  $("#open_map_link").on("click", function() {
    window.open($data["osm_url"], "_blank");
  });

  $("#map_collapse").on("shown.bs.collapse", function(){
    if (map == null) {
      latlong = $data["latlong"].split(",")
      lat = parseFloat(latlong[0])
      long = parseFloat(latlong[1])
      map = initmap(lat, long, getIcon(), $data["osm_url"]);
    }
  });
});
