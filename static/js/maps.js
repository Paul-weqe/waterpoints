
    function initMap() {
      // The location of Uluru
      var center = {lat: 1.3661556156293706, lng: 39.068242743190474};
      // The map, centered at Uluru
      var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 8, center: center});
        // The marker, positioned at Uluru
        var marker = new google.maps.Marker({position: center, map: map});
      }

      var data = {{points|tojson}}["data"];

      // points will hold data in the form points = [[a, b, c, d], [e, f, g, h]...[w, x, y, z]]
      // this means it will be an array of arrays
      // each array will be in the form [a, b, c, d] where a -> name, b -> lon, c -> lat, d -> id
      var points = [];
      for (var x in data){
        var coord = {};
        coord['name'] = data[x]['name'];
        coord['lon'] = data[x]['lon'];
        coord['lat'] = data[x]['lat'];
        coord['id'] = data[x]['id'];
        points.push(coord);
      }
    
