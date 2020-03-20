$(document).ready(function() {

var jistlatlng = (-33.972926835808714,18.695262372493744);
    var jistlat = '-33.973046951191726';
    var jistlng = '18.695039749145508';
    var zoom_count = 1;
    $("#map_contract_search_div").load("/contractscont/get_map_contract_search_frm",function(){
        
        $("#filter_contract_one").change(function(){
            var thisval = $(this).val();
            //console.log(thisval);
            var startlat = thisval.split(',')[1]
            var startlng = thisval.split(',')[2]
            setContractMarkerOne(startlat,startlng);
            $("#map_contract_search_div").hide();
            $("#map_contract_canvas").css('width','100%');
            return false;
        });
        $("#filter_contract_point").change(function(){
            var thisval = $(this).val();
            //console.log(thisval);
            //var startlat = thisval.split(',')[1]
            //var startlng = thisval.split(',')[2]
            //setContractMarkerOne(startlat,startlng);
            //$("#map_contract_search_div").hide();
            //$("#map_contract_canvas").css('width','100%');
            $.get("/contractscont/get_point_contracts_coords?point="+thisval,function(response){
                //console.log(response); 
                var jsondata = $.parseJSON(response);
                clearmarkerArray();
                setTimeout(function() {
                    //clearInterval(zoomMarkerInterval);
                    //map.setZoom(11);
                    var contract_search_div = document.getElementById('map_contract_search_div');
                    var contract_canvas = document.getElementById('map_contract_canvas');
                    contract_search_div.style.display = 'block';
                    contract_canvas.style.width = '80%' ;
                },1500);

                for (var i = 0; i < jsondata['pointlist'].length; i++) {
                    var lat = jsondata['pointlist'][i].lat;
                    var lng = jsondata['pointlist'][i].lng;
                    var text = jsondata['pointlist'][i].point;
                    setContractMarkerOne(lat,lng,text);
                }

            return false;
            }); 
            return false;
        
        });
        return false;  
    });

});
