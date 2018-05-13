var map=null;

$( document ).ready(function() {

  $("#map_collapse").on("shown.bs.collapse", function(){
    if (map == null) {
      map = initmap($data["osm_url"]);
      icons = []
      var arrayLength = $data["uni_latlong_data"].length;
      for (var i = 0; i < arrayLength; i++) {
        latlong = $data["uni_latlong_data"][i]["latlong"].split(",")
        url = $data["uni_latlong_data"][i]["view_url"]
        lat = parseFloat(latlong[0])
        long = parseFloat(latlong[1])
        icons.push(add_icon(map, lat, long, getIcon(), url));
      }
      icons_group = new L.featureGroup(icons)
      map.fitBounds(icons_group.getBounds());
    }
  });

});
