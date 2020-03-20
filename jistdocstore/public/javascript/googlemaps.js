//google.maps.visualRefresh = true;
var initialmap;
var map;
var geocoder;
var jistlatlng = (-33.972926835808714,18.695262372493744);
var jisthomelatlng
var directionsDisplay;
var directionsService;
var stepDisplay;
var markerArray = [];
var geocoder;
var destination;
var enddestinationlatLng

function initializeGoogleMaps() {
  jisthomelatlng =  new google.maps.LatLng(-33.972926835808714,18.695262372493744)
    //-33.972926835808714
    //18.695262372493744
  geocoder = new google.maps.Geocoder();
  document.getElementById('mapsearch_lat').value = jisthomelatlng.lat();
  document.getElementById('mapsearch_lng').value = jisthomelatlng.lng();
  var mapOptions = {
    zoom: 11,
    center: jisthomelatlng ,
  };

  map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
  directionsService = new google.maps.DirectionsService();
  placeMarkerJistLogo(jisthomelatlng, map);
  geocoder = new google.maps.Geocoder();
  google.maps.event.addListener(map, 'zoom_changed', function() {
      //console.log(e);
  });
  google.maps.event.addListener(map, 'click', function(e) {
      //console.log(e);
      placeMarker(e.latLng, map);
      document.getElementById('mapsearch_lat').value = e.latLng.lat();
      document.getElementById('mapsearch_lng').value = e.latLng.lng();
      var destination = e.latLng;
      var start = jisthomelatlng;
      var route = calcRoute(start,destination);
      //geocodeLatLng(e.latLng.lat(),e.latLng.lng());
      var direction_canvas = document.getElementById('map_directions_canvas');
      var map_canvas = document.getElementById('map_maps_canvas');
      var streetview_canvas = document.getElementById('map_streetview_canvas');
      direction_canvas.innerHTML = '';
      map_canvas.innerHTML = '';
      streetview_canvas.innerHTML = '';
      //console.log(route);
  });
    // Create a renderer for directions and bind it to the map.
  var rendererOptions = {
    map: map
  }
  directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

      // Instantiate an info window to hold step text.
  stepDisplay = new google.maps.InfoWindow();
    //geocodeLatLng(jisthomelatlng.lat(),jisthomelatlng.lng());
  var addressdiv = document.getElementById("google_address");
  addressdiv.innerHTML = '';
  addressdiv.innerHTML = "<h6 class='effect6'>Nebula Crescent, Blackheath, Cape Town </h6>";
};

function GetGeoLocationGoogleMaps() {
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);
      //console.log(pos.lat());
      //console.log(pos.lng());
      var mapOptions = {
          zoom: 18,
          position: pos,
          mapTypeId: google.maps.MapTypeId.SATELLITE
      };
      initialmap = new google.maps.Map(document.getElementById('map_location_canvas'),
          mapOptions);

      var infowindow = new google.maps.InfoWindow({
        map: initialmap,
        position: pos,
        content: "My Current Position ",
      });
      initialmap.setCenter(mapOptions.position);
      document.getElementById('mapsearch_lat').value = pos.lat();
      document.getElementById('mapsearch_lng').value = pos.lng();
      initialmap.setTilt(45);
    }, function() {
      handleNoGeolocation(true);
    });
  } else {
    // Browser doesn't support Geolocation
    handleNoGeolocation(false);
  }
}
function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = 'Error: The Geolocation service failed.';
  } else {
    var content = 'Error: Your browser doesn\'t support geolocation.';
  };

  var options = {
    map: initialmap,
    position: new google.maps.LatLng(jisthomelatlng.lat(), jisthomelatlng.lng()),
    content: content
  };

  var infowindow = new google.maps.InfoWindow(options);
  initialmap.setCenter(options.position);
};
function placeMarker(position, map) {
  var marker = new google.maps.Marker({
    position: position,
    map: map,
  });
  map.panTo(position);
};
function placeMarkerJistLogo(position, map) {
var image = {
    url: '/images/jistweblogosmallest.png',
    // This marker is 20 pixels wide by 32 pixels tall.
    size: new google.maps.Size(70, 67),
    // The origin for this image is 0,0.
    origin: new google.maps.Point(0,0),
    // The anchor for this image is the base of the flagpole at 0,32.
    anchor: new google.maps.Point(0, 30),
    scaledSize: new google.maps.Size(30,30)
  };
  var marker = new google.maps.Marker({
    position: position,
    map: map,
    icon: image
  });
  map.panTo(position);
};
function geocodeAddress(address) {
    //var address = document.getElementById("address").value;
    var addressdiv = document.getElementById("google_address");
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        //console.log(results[0].formatted_address);
        //console.log(addressdiv);
        //addressdiv.innerHTML = '';
        addressdiv.innerHTML = "<h6 class='effect6'>" + results[0].formatted_address + '</h6>';
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        //alert("Geocode was not successful for the following reason: " + status);
        addressdiv.innerHTML = "<h6 class='effect6'>  Could Not Geocode Address to Coordinates </h6>";
      }
    });
  }
function geocodeLatLng(lat,lng) {
    //var address = document.getElementById("address").value;
    var addressdiv = document.getElementById("google_address");
    var latlng = new google.maps.LatLng(lat,lng);
    geocoder.geocode( { 'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);

        console.log(results[0].formatted_address)
        console.log(results[0].address_components[0].long_name)
        console.log(results[0].address_components[1].long_name)
        console.log(results[0].address_components[2].long_name)
        console.log(results[0].address_components[3].long_name)
        //console.log(results[1].address_components[0].long_name)
        //console.log(results[1].address_components[1].long_name)
        //console.log(results[1].address_components[2].long_name)
        //console.log(results[1].address_components[3].long_name)
        addressdiv.innerHTML = "<h6 class='effect6'>" + results[0].formatted_address +'</h6>';
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        //alert("Geocode was not successful for the following reason: " + status);
        addressdiv.innerHTML = "<h6 class='effect6'>  Could Not Geocode Coordinates to an Address  </h6>";

      }
    });
  }

function calcRoute(start,end) {
  // First, remove any existing markers from the map.
  for (var i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(null);
  }
  // Now, clear the array itself.
  enddestinationlatLng = end;
  markerArray = [];
  // Retrieve the start and end locations and create
  // a DirectionsRequest using WALKING directions.
  var request = {
      origin: start,
      destination: end,
      travelMode: google.maps.TravelMode.DRIVING
  };
  // Route the directions and pass the response to a
  // function to create markers for each step.
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      var warnings = document.getElementById('warnings_panel');
      warnings.innerHTML = '<b>' + response.routes[0].warnings + '</b>';
      directionsDisplay.setDirections(response);
      showSteps(response);
    }
      return response
  });
}
function calcRouteFromOutside(startlat,startlng,endlat,endlng) {
  var start = new google.maps.LatLng(startlat,startlng);
  enddestinationlatLng = new google.maps.LatLng(endlat,endlng);
  // First, remove any existing markers from the map.
  for (var i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(null);
  }
  // Now, clear the array itself.
  markerArray = [];
  // Retrieve the start and end locations and create
  // a DirectionsRequest using WALKING directions.
  var request = {
      origin: start,
      destination: enddestinationlatLng,
      travelMode: google.maps.TravelMode.DRIVING
  };
  // Route the directions and pass the response to a
  // function to create markers for each step.
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      var warnings = document.getElementById('warnings_panel');
      warnings.innerHTML = '<b>' + response.routes[0].warnings + '</b>';
      directionsDisplay.setDirections(response);
      showSteps(response);
      return response
    }
  });
}
function showSteps(directionResult) {
  // For each step, place a marker, and add the text to the marker's
  // info window. Also attach the marker to an array so we
  // can keep track of it and remove it when calculating new
  // routes.
  var myRoute = directionResult.routes[0].legs[0];
  var jsonroute = JSON.stringify(myRoute);
  var btnstring = "<button id='btn_change_start_position' onclick='func_change_start_position()'>Change Start Position</button>"
  var stringpdfmain = "<a href='/productioncont/export_google_directions?lat=" + enddestinationlatLng.lat() + "&lng=" + enddestinationlatLng.lng()+"&route="+jsonroute + "'>"
  var stringpdf = "<span class='span_steplen'>"+stringpdfmain;
  var direction_canvas = document.getElementById('map_directions_canvas');
  direction_canvas.innerHTML = '';
  var string1pdf = "<img src='/images/pdficon.jpg'></img>"
  pdfstring = stringpdf + string1pdf
  var header = "<h5 class='ui-widget-shadow'>Directions" + pdfstring +"</span></a></h5><b>"
  var startpoint = 'Start: ' + myRoute.start_address + '<br/>'
  var endpoint = 'End: ' + myRoute.end_address + '<br/>'
  var totaldistance = 'Total Distance: ' + myRoute.distance.text + '<br/>'
  var totaltime = 'Total Approx Time: ' + myRoute.duration.text + '<br/>'
  direction_canvas.innerHTML = header + startpoint + endpoint +totaldistance + totaltime + '</b><p/>';
  var addressdiv = document.getElementById("google_address");
  addressdiv.innerHTML = '';
  addressdiv.innerHTML = "<h6 class='effect6'>" + myRoute.end_address + "</h6>";
  //console.log(myRoute);
  for (var i = 0; i < myRoute.steps.length; i++) {
    var marker = new google.maps.Marker({
      position: myRoute.steps[i].start_location,
      map: map
    });
    attachInstructionText(marker, myRoute.steps[i].instructions);
    markerArray[i] = marker;
    //console.log(myRoute.steps[i].instructions);
    var duration =  "<span class='span_steplen'>" + 'Duration: ' + myRoute.steps[i].duration.text;
    var distance = ' Distance ' + myRoute.steps[i].distance.text + '</span><br/>';
    var instructions = direction_canvas.innerHTML + myRoute.steps[i].instructions
    direction_canvas.innerHTML =  instructions + duration + distance ;
  }
}
function attachInstructionText(marker, text) {
  google.maps.event.addListener(marker, 'click', function() {
    // Open an info window when the marker is clicked on,
    // containing the text of the step.
    stepDisplay.setContent(text);
    stepDisplay.open(map, marker);
  });
};
function func_change_start_position() {
    console.log("Made It"); 
    func_test();
};
function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I&v=3.exp&sensor=true&' +
      'callback=initializeGoogleMaps';
  document.body.appendChild(script);
};
window.onload = loadScript;
//google.maps.event.addDomListener(window, 'load', initializeGoogleMaps);
