$(document).ready(function() {
var jistlatlng = (-33.972926835808714,18.695262372493744);
    var jistlat = '-33.973046951191726';
    var jistlng = '18.695039749145508';
    $("#btn_search_currentposition").button();
    $("#btn_search_gohome").button();
    $("#btn_change_start_position").button();
    $("#btn_search_address").button();
    $("#mapsearch_address").css('width','300px');
    $("#btn_search_address").click(function(){
        var direction_canvas = document.getElementById('map_directions_canvas');
        var map_canvas = document.getElementById('map_maps_canvas');
        var streetview_canvas = document.getElementById('map_streetview_canvas');
        direction_canvas.innerHTML = '';
        map_canvas.innerHTML = '';
        streetview_canvas.innerHTML = '';
        var address = $("#mapsearch_address").val();
        geocodeAddress(address);
        $("#mapsearch_address").val('');
        //$("#map_location_canvas").empty();
        //callback_get_saved_locations();
        //$("#map_location_canvas").load("/productioncont/get_my_saved_locations",function(){
        //   return false;  
        //});
        //clear_form_elements($("#search_directions"));
        return false;
    });
    $("#btn_search_gohome").click(function(){
        initializeGoogleMaps();
        //var direction_canvas = document.getElementById('map_directions_canvas');
        //var map_canvas = document.getElementById('map_maps_canvas');
        //var streetview_canvas = document.getElementById('map_streetview_canvas');
        //direction_canvas.innerHTML = '';
        //map_canvas.innerHTML = '';
        //streetview_canvas.innerHTML = '';
        $("#map_location_canvas").empty();
        $("#map_directions_canvas").empty();
        $("#map_maps_canvas").empty();
        $("#map_streetview_canvas").empty();
        $("#warnings_panel").empty();
        callback_get_saved_locations();
        var lat = $("#mapsearch_lat").val();
        var lng = $("#mapsearch_lng").val();
        var loc = lat +','+ lng
        //geocodeLatLng(parseFloat(lat),parseFloat(lng));
        //clear_form_elements($("#search_directions"));
        return false;
    });
    $("#btn_search_currentposition").click(function(){
        $("#map_location_canvas").empty();
        GetGeoLocationGoogleMaps();
        var lat = $("#mapsearch_lat").val();
        var lng = $("#mapsearch_lng").val();
        var loc = lat +','+ lng
        //geocodeLatLng(lat,lng);
        return false;
    });
    $("#btn_search_streetviewpic").button();
    $("#btn_search_streetviewpic").click(function(){
        var lat = $("#mapsearch_lat").val();
        var lng = $("#mapsearch_lng").val();
        var loc = lat +','+ lng
        var size = '430x215';
        var staticsize = '420x210';
        var heading0 = '0';
        var heading90 = '90';
        var heading180 = '180';
        var heading270 = '270';
        var pitch = '0';
        var sensor = 'false';
        var param0 = '&heading='+heading0
        var param90 = '&heading='+heading90
        var param180 = '&heading='+heading180
        var param270 = '&heading='+heading270
        var zoom16 = '&zoom=17';
        var zoom14 = '&zoom=15';
        var zoom12 = '&zoom=14';
        var zoom10 = '&zoom=09';
        var zoom5 = '&zoom=5';
        var maptype = '&maptype=roadmap'
        var markerto = '&markers=color:blue%7Clabel:T%7C' + loc
        var key_api = 'AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I'
        var params = '&size='+size+'&location='+loc+'&pitch='+pitch+'&sensor='+sensor+'&key='+key_api;
        var streetpage = 'http://maps.googleapis.com/maps/api/streetview?';
        var mappagemain = 'http://maps.googleapis.com/maps/api/staticmap?';
        var mapparams = 'center='+lat+','+lng+'&size='+staticsize+'&sensor='+sensor+'&key='+key_api;
        var mappage16 = mappagemain + mapparams + markerto + zoom16
        var mappage14 = mappagemain + mapparams + markerto + zoom14
        var mappage12 = mappagemain + mapparams + markerto + zoom12
        var mappage10 = mappagemain + mapparams + markerto + zoom10
        var mapdirections = "<a href='/productioncont/export_google_street_view?lat=" + lat +"&lng=" +lng+"'><img src='/images/pdficon.jpg'></img></a>"
        var headerstreet = "<h3 class='ui-widget-shadow'>Street View<span class='span_steplen'>" + mapdirections+"</span></h3>"
        var headermaps = "<h3 class='ui-widget-shadow'>Map View</h3>"
        $("#map_streetview_canvas").empty();
        $("#map_maps_canvas").empty();
        $("#map_streetview_canvas").append(headerstreet + "<img class='static_map_small' src='"+streetpage+params+param0+"'></img><img class='static_map_small 'src='"+streetpage+params+param90+"'></img><br/><img class='static_map_small' src='"+streetpage+params+param180+"'></img></img><img class='static_map_small' src='"+streetpage+params+param270+"'></img><br/>" );
        $("#map_maps_canvas").append(headermaps + "<img class='static_map_small' src='"+mappage16+"'></img><img class='static_map_small' src='"+mappage14+"'></img><br/><img class='static_map_small' src='"+mappage12+"'></img><img class='static_map_small' src='"+mappage10+"'></img>");
        return false;
    });
    $("#btn_change_directions_saved_locations").button();
    $("#btn_change_directions_saved_locations").click(function(){
        $("#dialog_choose_locations_div").load( "/productioncont/get_dialog_saved_locations_directions", function( data ) {
            $( "#dialog_choose_locations" ).dialog({
                autoOpen: false,
                height: 280,
                width: 550,
                //modal: true,
                buttons: {
                    "Get Directions": function() {
                        var bValid = true;

                        if ( bValid ) {

                            var formserial = $("#dialog_choose_locations_frm").serialize();
                            var startcords = $("#location_start").val()
                            var endcords = $("#location_end").val()
                            var startlat = startcords.split(',')[1]
                            var startlng = startcords.split(',')[2]
                            var endlat = endcords.split(',')[1]
                            var endlng = endcords.split(',')[2]
                            //console.log(startpoint);
                            //console.log(endpoint);
                            var route = calcRouteFromOutside(startlat,startlng,endlat,endlng);
                            //var jqxhr = $.post("/productioncont/get_directions_between?"+formserial, function(data) {
                                    //callback_get_saved_locations();
                            //       return false 
                            //});
                            $( this ).dialog( "close" );
                        }
                    },
                    Cancel: function() {
                                $( this ).dialog( "close" );
                            }
                },
                close: function() {
                            clear_form_elements($("#dialog_choose_locations_frm"));
                            $( this ).find('input').val('');
                       }
            });
            $("#dialog_choose_locations").dialog("open"); 
        });
        return false;
    });
    $( "#dialog_location_div" ).dialog({
        autoOpen: false,
        height: 480,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;

                if ( bValid ) {

                    var formserial = $("#dialog_location_frm").serialize();

                    var jqxhr = $.post("/productioncont/save_location?"+formserial, function(data) {
                            callback_get_saved_locations();
                           return false 
                    });
                    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                        $( this ).dialog( "close" );
                    }
        },
        close: function() {
                    clear_form_elements($("#dialog_location_frm"));
                    $( this ).find('input').val('');
               }
    });
    function clear_form_elements(ele) {
        $(ele).find(':input').each(function() {
            switch(this.type) {
                case 'password':
                case 'select-multiple':
                case 'select-one':
                    $(this).val('');
                    break;
                case 'text':
                    $(this).val('');
                    break;
                case 'textarea':
                    $(this).val('');
                    break;
                case 'checkbox':
                case 'radio':
                    this.checked = false;
            }
        });
    }
    function callback_get_saved_locations() {
        $("#map_location_canvas").load("/productioncont/get_my_saved_locations",function(){
            //$("#map_location_canvas").css('overflow-x','scroll');
            $("#map_location_canvas").css('overflow-y','scroll');
            $(".location_trash").click(function(){
                var loc = $(this).attr('value')
                ajqhr = $.post( "/productioncont/deactivate_location/"+ loc, function(data) {
                    callback_get_saved_locations()
                    return false;
                });
                    return false;
            });
            $(".location_screenview").click(function(){
                var loc = $(this).attr('value')
                ajqhr = $.get( "/productioncont/get_single_location/"+ loc, function(data) {
                    //callback_get_saved_locations()
                    var jsondata = $.parseJSON(data);
                    //console.log(jsondata.lat);
                    var endlat = jsondata.lat;
                    var endlng = jsondata.lng;
                    var startlat = jistlat;
                    var startlng = jistlng;
                    $("#mapsearch_lat").val(endlat);
                    $("#mapsearch_lng").val(endlng);
                    //geocodeLatLng(startlat,endlng);
                    var route = calcRouteFromOutside(startlat,startlng,endlat,endlng);
                    //console.log(route);
                    $("#btn_search_streetviewpic").trigger('click');
                    var htmdirections = $("#map_directions_canvas").html();
                    //console.log(htmdirections);
                    callback_do_exports(loc);
                    return false;
                });
                    return false;
            });
           return false;  
        });

    };
    $(".directions_pdf").click(function(){
        var loc = $(this).attr('value')
        ajqhr = $.post( "/productioncont/deactivate_location/"+ loc, function(data) {
            callback_get_saved_locations()
            return false;
        });
            return false;
    });
    callback_get_saved_locations()
    $("#btn_export_location").button();
    $("#btn_export_location").click(function(){
        var lat = $("#mapsearch_lat").val();
        var lng = $("#mapsearch_lng").val();
        $("#dialog_lat").val(lat)
        $("#dialog_lng").val(lng)
        var loc = lat +','+ lng
        $("#dialog_location_div").dialog("open"); 
        return false;
    });

    function callback_do_exports(loc) {
        $(".export_directions").click(function(){
            //console.log("Achieved to get to Export");
            ajqhr = $.get( "/productioncont/get_single_location/"+ loc, function(data) {
                //callback_get_saved_locations()
                var jsondata = $.parseJSON(data);
                //console.log(jsondata.lat);
                var endlat = jsondata.lat;
                var endlng = jsondata.lng;
                var startlat = jistlat;
                var startlng = jistlng;
                $("#mapsearch_lat").val(endlat);
                $("#mapsearch_lng").val(endlng);
                var route = calcRouteFromOutside(startlat,startlng,endlat,endlng);
                //console.log(route);
                $("#btn_search_streetviewpic").trigger('click');
                var htmdirections = $("#map_directions_canvas").html();
                //console.lOG(HTmdirections);
                return false;
            });
                return false;
        });
    };
});
