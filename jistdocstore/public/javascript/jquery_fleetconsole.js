$(function(){
    $( "#fleet_tabs" ).tabs({ 
        heightStyle: "fill", 
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#tblfleetlist").delegate('tr','mouseover mouseleave click',function(e) {
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
                    $('#fleet_tabs ul:first li:eq(3) a').text("Edit Fleet ID: "+col0text);
                    $("#fleet_tabs").tabs('select', 3);
                    $("#div_editfleet").load("/transportcont/get_edit_fleet_form/"+alltrim(col0text),function(){
                        var dateacquired = $( "#edit_date_acquired" ).val();
                        var datefuelexpire = $( "#edit_fuel_card_expiry_date" ).val();
                        $( "#edit_date_acquired" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_fuel_card_expiry_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_vehicle_description" ).css("width","300px");
                        $( "#edit_date_acquired" ).val(dateacquired);
                        $( "#edit_fuel_card_expiry_date" ).val(datefuelexpire);
                        $("#new_fleet_form").hide();
                        $("#edit_fleet_form").show();
                        $("#edit_btn_fleet").click(function(){
                            //console.log("Made It Here to OK");
                            var activestatus = $( "#edit_fleet_active" ).val();
                            var driverid = $( "#edit_driver_id" ).val();
                            var formserial = $("#edit_fleet_form").serialize();
                            //console.log(formserial);
                            var jqxhr = $.post("/transportcont/saveeditfleet?"+formserial+"&edit_fleet_active="+activestatus+"&edit_driver_id="+driverid, function(data) {
                                clear_form_elements($("#edit_fleet_form"));
                                $('#fleet_tabs ul:first li:eq(3) a').text("Fleet Item Info");
                                if (activestatus=='1'){
                                $("#fleet_tabs").tabs('select', 2);
                                }else{
                                $("#fleet_tabs").tabs('select', 1);
                                };
                                return false;
                            });
                          return false;
                        });
                    });

                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#tblactivefleetlist").delegate('tr','mouseover mouseleave click',function(e) {
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
                    $('#fleet_tabs ul:first li:eq(3) a').text("Edit Fleet ID: "+col0text);
                    $("#fleet_tabs").tabs('select', 3);
                    $("#div_editfleet").load("/transportcont/get_edit_fleet_form/"+alltrim(col0text),function(){
                        var dateacquired = $( "#edit_date_acquired" ).val();
                        var datefuelexpire = $( "#edit_fuel_card_expiry_date" ).val();
                        $( "#edit_date_acquired" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_fuel_card_expiry_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_date_acquired" ).val(dateacquired);
                        $( "#edit_fuel_card_expiry_date" ).val(datefuelexpire);
                        $("#new_fleet_form").hide();
                        $("#edit_fleet_form").show();
                        $("#edit_btn_fleet").click(function(){
                            //console.log("Made It Here to OK");
                            var activestatus = $( "#edit_fleet_active" ).val();
                            var driverid = $( "#edit_driver_id" ).val();
                            var formserial = $("#edit_fleet_form").serialize();
                            //console.log(activestatus);
                            var jqxhr = $.post("/transportcont/saveeditfleet?"+formserial+"&edit_fleet_active="+activestatus+"&edit_driver_id="+driverid, function(data) {
                                clear_form_elements($("#edit_fleet_form"));
                                $('#fleet_tabs ul:first li:eq(3) a').text("Fleet Item Info");
                                if (activestatus=='1'){
                                $("#fleet_tabs").tabs('select', 2);
                                }else{
                                $("#fleet_tabs").tabs('select', 1);
                                };

                                return false;
                            });
                          return false;
                        });
                    });
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#tbldriverlist").delegate('tr','mouseover mouseleave click',function(e) {
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
                    console.log(col0text);
                    $('#fleet_tabs ul:first li:eq(5) a').text("Edit Driver ID: "+col0text);
                    $("#fleet_tabs").tabs('select', 5);
                    $("#div_editdriver").load("/transportcont/get_edit_driver_form/"+alltrim(col0text),function(){
                        var datelicexpire = $( "#edit_licence_exp_date" ).val();
                        var datepdpexpire = $( "#edit_pdp_exp_date" ).val();
                        $( "#edit_licence_exp_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_pdp_exp_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#edit_driver_name_id" ).css("width","300px");
                        $( "#edit_licence_exp_date" ).val(datelicexpire);
                        $( "#edit_pdp_exp_date" ).val(datepdpexpire);
                        $("#new_driver_form").hide();
                        $("#edit_driver_form").show();
                        $("#edit_btn_driver").click(function(){
                            //console.log("Made It Here to OK");
                            var activestatus = $( "#edit_driver_active" ).val();
                            var driverid = $( "#driver_id_edit" ).val();
                            var formserial = $("#edit_driver_form").serialize();
                            //console.log(formserial);
                            var jqxhr = $.post("/transportcont/saveeditdriver?"+formserial+"&edit_driver_active="+activestatus+"&edit_driver_id="+driverid, function(data) {
                                clear_form_elements($("#edit_driver_form"));
                                $('#fleet_tabs ul:first li:eq(5) a').text("Driver Info");
                                $("#fleet_tabs").tabs('select', 4);
                                $("#edit_driver_form").hide();
                                return false;
                            });
                          return false;
                        });
                    });

                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#add_btn_fleet").click(function(){
                //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
                $('#fleet_tabs ul:first li:eq(3) a').text("Add New Fleet ");
                $("#fleet_tabs").tabs('select', 3);
                clear_form_elements($("#div_editfleet"));
                $("#new_fleet_form").show();
                $("#edit_fleet_form").hide();
              return false;
            });
            $("#add_btn_driver").click(function(){
                //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
                $('#fleet_tabs ul:first li:eq(5) a').text("Add New Driver ");
                $("#fleet_tabs").tabs('select', 5);
                clear_form_elements($("#div_editdriver"));
                $("#new_driver_form").show();
                $("#edit_driver_form").hide();
              return false;
            });
        }, 
       select: function(event,ui){
            console.log("select pressed old tab is:" +ui.oldPanel) 
            console.log("select pressed new tab is:" +ui.panel.id) 
            if (ui.panel.id == 'ui-tabs-FleetTransportLink'){
                $("#link_all_fleet_div").load("/fleetcont/get_fleet_resources_active_html",function(data){
                    $("#tbl_active_fleet_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var fleet_id = alltrim(col0text); 
                            var selectedtab = $("#fleet_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/fleetcont/link_fleet_to_transport/"+fleet_id, function(data) {
                                $("#fleet_tabs").tabs('select', selectedtab-1);
                                $("#fleet_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
                $("#link_all_transport_div").load("/fleetcont/get_transport_resources_active_html",function(data){
                    $("#tbl_active_transport_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var transport_id = alltrim(col0text); 
                            var selectedtab = $("#fleet_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/fleetcont/delink_fleet_from_transport/"+transport_id, function(data) {
                                $("#fleet_tabs").tabs('select', selectedtab-1);
                                $("#fleet_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
            };
       },
   });

    $("#btn_fleet_new").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        var formserial = $("#new_fleet_form").serialize();
        var activestatus = $( "#fleet_active" ).val();
        var driverid = $( "#driver_name" ).val();
        var uniqid1 = Math.random();
        var jqxhr = $.post("/transportcont/savenewfleet?"+formserial+"&uniqid="+uniqid1+"&fleet_active="+activestatus+"&driver_id="+driverid, function(data) {
            clear_form_elements($("#new_fleet_form"));
            $("#new_fleet_form").hide();
            $('#fleet_tabs ul:first li:eq(3) a').text("Fleet Item Info");
            //return false;
            if (activestatus=='1'){
            $("#fleet_tabs").tabs('select', 2);
            }else{
            $("#fleet_tabs").tabs('select', 1);
            };

            return false;
        });
      //return false;
    });
    $("#btn_driver_new").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        var formserial = $("#new_driver_form").serialize();
        var uniqid1 = Math.random();
        var jqxhr = $.post("/transportcont/savenewdriver?"+formserial+"&uniqid="+uniqid1, function(data) {
            clear_form_elements($("#new_driver_form"));
            $("#new_driver_form").hide();
            $('#fleet_tabs ul:first li:eq(5) a').text("Driver Info");
            //return false;
            $("#fleet_tabs").tabs('select', 4);
            return false;
        });
      //return false;
    });
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

    }
    $( "#date_acquired" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#fuel_card_expiry_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#licence_exp_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#pdp_exp_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#vehicle_description" ).css("width","300px");
    $( "#driver_name_id" ).css("width","500px");
});




