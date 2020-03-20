$(function(){
    $( "#contracts_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#contracts_wip_table").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                    //$("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,4);
                    //$("#myjistconsole_tabs").tabs('select', 4);
                }else   {
                    $(this).removeClass("hover");
                }
            });

        }
    });
    $( "#site_address_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#contracts_wip_table").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                    //$("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,4);
                    //$("#myjistconsole_tabs").tabs('select', 4);
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $(".export_site_directions").click(function(){
               var lat = $(this).attr('lat'); 
               var lng = $(this).attr('lng'); 
               var jcno = $(this).attr('jcno'); 
               var site = $(this).attr('site'); 
               get_site_address_maps(lat,lng,jcno,site);
               $("#site_address_tabs").tabs('select', 2);
            });

        },
       select: function(event,ui){
           return
        }
    });
    $("#contracts_tabs").tabs('select', 1);
    $("#search_contract_jcno").css('width','100px');
    $("#search_contract_client").css('width','200px');
    $("#search_contract_sitename").css('width','200px');
    $("#search_contract_description").css('width','200px');
    $("#search_contract_orderno").css('width','100px');
    $("#button_search_contract_jcno").button();
    $("#button_search_contract_client").button();
    $("#button_search_contract_sitename").button();
    $("#button_search_contract_description").button();
    $("#button_search_contract_orderno").button();
    $("#button_add_new_contract").button();
    $("#button_search_contract_jcno").click(function(){
        var searchphrase = $("#search_contract_jcno").val()
        $("#div_contracts_site").empty();
        $("#div_contracts_site").load("/contractscont/get_search_contracts?switch=JCNo&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_contracts_table();
            return false;
        });
    });
    $("#button_search_contract_sitename").click(function(){
        var searchphrase = $("#search_contract_sitename").val()
        $("#div_contracts_site").empty();
        $("#div_contracts_site").load("/contractscont/get_search_contracts?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_contracts_table();
            return false;
        });
    });
    $("#button_search_contract_client").click(function(){
        var searchphrase = $("#search_contract_client").val()
        $("#div_contracts_site").empty();
        $("#div_contracts_site").load("/contractscont/get_search_contracts?switch=SearchClient&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_contracts_table();
            return false;
        });
    });
    $("#button_search_contract_description").click(function(){
        var searchphrase = $("#search_contract_description").val()
        $("#div_contracts_site").empty();
        $("#div_contracts_site").load("/contractscont/get_search_contracts?switch=SearchDescription&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_contracts_table();
            return false;
        });
    });
    $("#button_search_contract_orderno").click(function(){
        var searchphrase = $("#search_contract_orderno").val()
        $("#div_contracts_site").empty();
        $("#div_contracts_site").load("/contractscont/get_search_contracts?switch=SearchOrderNo&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_contracts_table();
            return false;
        });
    });
    $("#button_add_new_contract").click(function(){
        $("#div_contracts_site").empty();
         $("#contract_orderdate").datepicker();        
        $("#contract_orderdate").datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#dialog_contract_new" ).dialog("open");
        
    });
    $( "#dialog_contract_new" ).dialog({
        autoOpen: false,
        height: 480,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;
                if ( bValid ) {
                    var formserial = $("#dialog_contract_new_frm").serialize();
                    var jqxhr = $.post("/contractscont/ajaxnewcontract?"+formserial, function(data) {
                            //$("#contracts_tabs").tabs("select",2);
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
                    clear_form_elements($("#dialog_contract_new_frm"));
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_contract_edit" ).dialog({
        autoOpen: false,
        height: 680,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;

                if ( bValid ) {

                    var formserial = $("#dialog_contract_edit_frm").serialize();

                    var jqxhr = $.post("/contractscont/ajaxeditcontract?"+formserial, function(data) {
                            //$("#contracts_tabs").tabs("select",2);
                            $("#div_contracts_site").empty();
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
                    clear_form_elements($("#dialog_contract_edit_frm"));
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_orderitems_edit" ).dialog({
        autoOpen: false,
        height: 480,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;

                if ( bValid ) {

                    var formserial = $("#dialog_orderitems_edit_frm").serialize();

                    var jqxhr = $.post("/contractscont/ajax_save_edit_orderitem?"+formserial, function(data) {

                        $("#outputcontractdata").load("/contractscont/get_contract_orderitems/"+alltrim(data),function(responseTxt,statusTxt,xhr){
                            get_output_contract_data(data)
                           return false 
                        });
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
                    clear_form_elements($("#dialog_orderitems_edit_frm"));
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_orderitems_new" ).dialog({
        autoOpen: false,
        height: 480,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;

                if ( bValid ) {

                    var formserial = $("#dialog_orderitems_new_frm").serialize();

                    var jqxhr = $.post("/contractscont/ajax_save_new_orderitem?"+formserial, function(data) {

                        $("#outputcontractdata").load("/contractscont/get_contract_orderitems/"+alltrim(data),function(responseTxt,statusTxt,xhr){
                            get_output_contract_data(data)
                           return false 
                        });
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
                    clear_form_elements($("#dialog_orderitems_new_frm"));
                    $( this ).find('input').val('');
               }
    });
    function activate_contracts_table(){
        $("#tbl_active_contracts_loading").delegate('tr','mouseover mouseleave click',function(e) {
            //e.preventDefault();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#tbl_active_contracts_loading").delegate('td','click',function(e){
            e.preventDefault();
            e.stopPropagation();
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 12){ 
                    var orderitemid = $(this).parent().find("td").eq(0).html();
                    var col0text = $(this).parent().find("td").eq(0).html();
                    var col1text = $(this).parent().find("td").eq(1).html();
                    var col4text = $(this).parent().find("td").eq(4).html();
                    var col5text = $(this).parent().find("td").eq(5).html();
                    var col6text = $(this).parent().find("td").eq(6).html();
                    var col7text = $(this).parent().find("td").eq(7).html();
                    var col8text = $(this).parent().find("td").eq(8).html();
                    var col9text = $(this).parent().find("td").eq(9).html();
                    var uniqid = Math.random();
                    //$( "#edit_description" ).css("width","400px");
                    var dateval = new Date();
                    $("#schedule_date_this").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate", dateval);
                    $("#req_id").val(alltrim(col0text)); 
                    $("#fleet_id").val(); 
                    $( "#dialog_schedule_transport" ).dialog("open");
                    //var curTabSelected = $('#transport_tabs .ui-tabs-active').index();
                    //$("#transport_tabs").tabs("load",curTabSelected);
                };
                if ($(this).index() == 9){ 
                    var jno_id = $(this).parent().find("td").eq(0).html();
                    get_output_contract_data(jno_id)
                    var curTabSelected = $('#contracts_tabs .ui-tabs-active').index();
                    //console.log(curTabSelected)
                    $("#contracts_tabs").tabs("select",curTabSelected + 1);
                    return false;
                };
                return false;
            };
            return false;
        });
        $(".pic_contract_new_edit").click(function(){
            var jno = $(this).attr('jcno');
            $("#dialog_contract_edit").load("/contractscont/get_edit_contract_dialog?jno="+alltrim(jno),function(responseTxt,statusTxt,xhr){
                $( "#dialog_contract_edit" ).dialog("open");
                // $("#contract_orderdate_edit").datepicker();        
                //$("#contract_orderdate_edit").datepicker( "option", "dateFormat", "yy-mm-dd" );
            });
        });
    };
    function get_output_contract_data(jno_id){
        $("#outputcontractdata").load("/contractscont/get_contract_orderitems/"+alltrim(jno_id),function(responseTxt,statusTxt,xhr){
            $(".pic_orderitem_edit").click(function(){
                var jno = $(this).attr('jcno');
                var thisid = $(this).attr('id');
                //console.log(jno);
                //console.log(thisid);
                //
                $("#dialog_orderitems_edit").load("/contractscont/get_edit_orderitems_dialog?orderitemid="+alltrim(thisid),function(responseTxt,statusTxt,xhr){
                    $("#orderitem_description").css("width","350px");
                    $( "#orderitem_qty" ).change(function(e){
                        if ( $(this).val()){
                            var supp_price = $("#orderitem_price").val();
                            var supp_total = parseFloat(supp_price)*parseFloat($(this).val());
                            $( "#orderitem_total" ).val(supp_total.toFixed(2));
                        };
                    });
                    $( "#orderitem_price" ).change(function(e){
                        if ( $(this).val()){
                            var supp_qty = $("#orderitem_qty").val();
                            var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
                            $( "#orderitem_total" ).val(supp_total.toFixed(2));
                        };
                    });
                    $( "#dialog_orderitems_edit" ).dialog("open");
                    $("#orderitem_item").focus();

                });
            });
            $("#btn_add_new_orderitem").click(function(){
                //console.log("Clicked Pressed"); 
                $("#orderitem_new_description").css("width","350px");
                $( "#orderitem_new_qty" ).change(function(e){
                    if ( $(this).val()){
                        var supp_price = $("#orderitem_new_price").val();
                        var supp_total = parseFloat(supp_price)*parseFloat($(this).val());
                        $( "#orderitem_new_total" ).val(supp_total.toFixed(2));
                    };
                });
                $( "#orderitem_new_price" ).change(function(e){
                    if ( $(this).val()){
                        var supp_qty = $("#orderitem_new_qty").val();
                        var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
                        $( "#orderitem_new_total" ).val(supp_total.toFixed(2));
                    };
                });
                var thisjno = $(this).attr('value');
                //console.log(thisjno);
                $("#orderitem_new_jcno").val(thisjno);
                $( "#dialog_orderitems_new" ).dialog("open");
                $("#orderitem_new_item").focus();
            });
            return false
        });
    };

    function alltrim(str) {
                return str.replace(/^\s+|\s+$/g, '');
    };
    function clear_form_elements(ele) {
        $(ele).find(':input').each(function() {
            switch(this.type) {
                case 'password':
                case 'select-multiple':
                case 'select-one':
                case 'text':
                case 'textarea':
                    $(this).val('');
                    break;
                case 'checkbox':
                case 'radio':
                    this.checked = false;
            }
        });

    };
    function get_site_address_maps(lat,lng,jcno,site){
        //var lat = $("#mapsearch_lat").val();
        //var lng = $("#mapsearch_lng").val();
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
        var stringpdfmain = "<a href='/productioncont/export_google_maps?lat=" + lat + "&lng=" +lng+"&jcno="+jcno+"&site="+site+"'><img src='/images/pdficon.jpg'></img></a>"
        var headerstreet = "<h3 class='ui-widget-shadow'>Street View<span class='span_steplen'>" + mapdirections+"</span></h3>"
        var headermaps = "<h3 class='ui-widget-shadow'>Mapped Directions for JCNo: "+jcno + " "+" Site: "+site+"<span class='span_steplen'>" + stringpdfmain+"</span></h3>"
        $("#map_streetview_sites").empty();
        $("#map_maps_sites").empty();
        $("#map_streetview_sites").append(headerstreet + "<img class='static_map_small' src='"+streetpage+params+param0+"'></img><img class='static_map_small 'src='"+streetpage+params+param90+"'></img><br/><img class='static_map_small' src='"+streetpage+params+param180+"'></img></img><img class='static_map_small' src='"+streetpage+params+param270+"'></img><br/>" );
        $("#map_maps_sites").append(headermaps + "<img class='static_map_small' src='"+mappage16+"'></img><img class='static_map_small' src='"+mappage14+"'></img><br/><img class='static_map_small' src='"+mappage12+"'></img><img class='static_map_small' src='"+mappage10+"'></img>");
        return false;
    };
    $("#site_address_tabs").tabs('select', 1);
});

