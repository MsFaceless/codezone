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
var markerArray = []
var zoomlevel
var zoomMarkerInterval
var markerCluster = null;
var imageUrl = 'http://chart.apis.google.com/chart?cht=mm&chs=24x32&' +
          'chco=FFFFFF,008CFF,000000&ext=.png';

function initializeJISTContractsMaps() {
  jisthomelatlng =  new google.maps.LatLng(-33.972926835808714,18.695262372493744)
  geocoder = new google.maps.Geocoder();
  //document.getElementById('mapsearch_lat').value = jisthomelatlng.lat();
  //document.getElementById('mapsearch_lng').value = jisthomelatlng.lng();
  var mapOptions = {
    zoom: 11,
    center: jisthomelatlng ,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  map = new google.maps.Map(document.getElementById('map_contract_canvas'), mapOptions);
  //directionsService = new google.maps.DirectionsService();
  placeMarkerJistLogo(jisthomelatlng, map);
  geocoder = new google.maps.Geocoder();
  markerCluster = new MarkerClusterer(map, markerArray);
  stepDisplay = new google.maps.InfoWindow();
  //google.maps.event.addListener(map, 'zoom_changed', function() {
      //console.log(e);
  //});
  google.maps.event.addListener(map, 'click', function(e) {
      //console.log(e);
      //placeMarker(e.latLng, map);
      //document.getElementById('mapsearch_lat').value = e.latLng.lat();
      //document.getElementById('mapsearch_lng').value = e.latLng.lng();
      //var destination = e.latLng;
      //var start = jisthomelatlng;
      //var route = calcRoute(start,destination);
      //geocodeLatLng(e.latLng.lat(),e.latLng.lng());
      //var direction_canvas = document.getElementById('map_directions_canvas');
      //var map_canvas = document.getElementById('map_maps_canvas');
      //var streetview_canvas = document.getElementById('map_streetview_canvas');
      //direction_canvas.innerHTML = '';
      //map_canvas.innerHTML = '';
      //streetview_canvas.innerHTML = '';
      //console.log(route);
  });
    // Create a renderer for directions and bind it to the map.
  var rendererOptions = {
    map: map
  }
  //directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

      // Instantiate an info window to hold step text.
  //stepDisplay = new google.maps.InfoWindow();
    //geocodeLatLng(jisthomelatlng.lat(),jisthomelatlng.lng());
  //var addressdiv = document.getElementById("google_address");
  //addressdiv.innerHTML = '';
  //addressdiv.innerHTML = "<h6 class='effect6'>Nebula Crescent, Blackheath, Cape Town </h6>";
};
function placeMarker(position, map) {
  var marker = new google.maps.Marker({
    position: position,
    map: map,
  });
  //map.panTo(position);
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
  map.zoom= 11;
};
function attachInstructionText(marker, text) {
  google.maps.event.addListener(marker, 'click', function() {
    // Open an info window when the marker is clicked on,
    // containing the text of the step.
    stepDisplay.setContent(text);
    stepDisplay.open(map, marker);
  });
};
// Add a marker to the map and push to the array.
function addMarker(location) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    color: 'white',
    icon:imageUrl,
    animation: google.maps.Animation.DROP
  });
  markerArray.push(marker);
  return marker
}

// Sets the map on all markerArray in the array.
function setAllMap(map) {
  for (var i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(map);
  }
}

// Removes the markerArray from the map, but keeps them in the array.
function clearmarkerArray() {
  setAllMap(null);
}

// Shows any markers currently in the array.
function showmarkers() {
  setAllMap(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearmarkerArray();
  markerArray = [];
};
function setMapToBounds() {
    var bounds = map.getBounds();
    map.panToBounds(bounds);
};

function setContractMarkerOne(lat,lng,contractdetails){
    destination = new google.maps.LatLng(lat,lng);
    //placeMarker(destination,map);
    var thismarker = addMarker(destination);
    attachInstructionText(thismarker,contractdetails);
    //map.setBounds(bounds);
    //console.log(bounds)
    //zoomlevel = 11; 
    //var contract_search_div = document.getElementById('map_contract_search_div');
    //var contract_canvas = document.getElementById('map_contract_canvas');
    //var contract_filter_one = document.getElementById('filter_contract_one');
    //var contract_filter_val = contract_filter_one.indexOf;
    //console.log(contract_filter_val);
    //map.setZoom(17);
    //zoomMarkerInterval = setInterval(function(){
    //    map.setZoom(zoomlevel);
    //    zoomlevel = zoomlevel + 2;
    //},2000);
    //map.panTo(destination);
    

};

function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I&v=3.exp&sensor=true&' +
      'callback=initializeJISTContractsMaps';
  document.body.appendChild(script);
};
window.onload = loadScript;

