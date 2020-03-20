$(function(){
    $( "#transport_tabs" ).tabs({ 
        heightStyle: "fill", 
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
           //$( "#grv_console_tabs" ).tabs("option","deactive", 2 );
           $("#somebutton").click(function(){
           });
       }, 
       select: function(event,ui){
            //console.log("select pressed old tab is:" +ui.oldPanel) 
            //console.log("select pressed new tab is:" +ui.panel.id) 
            if (ui.panel.id == 'ui-tabs-ActiveTransportRequests'){
                $("#transport_reqs_active").load("/transportcont/get_transport_list_active_html",function(data){
                    $("#tbl_active_transport_all").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    $("#tbl_active_transport_all").delegate('td','click',function(e){
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
                            if ($(this).index() == 13){ 
                                //console.log("Trash pressed");
                                var scopeid = $(this).parent().find("td").eq(0).html();
                                var uniqid = Math.random();
                                var curTabSelected = $('#transport_tabs .ui-tabs-active').index();
                                $("#ui-tabs-WayBills").load("/transportcont/get_transportreq_loading_all/"+scopeid, function(data) {
                                    $("#transport_tabs").tabs("select",'ui-tabs-WayBills');
                                    $("#btn_close_transport_loading").remove();
                                    $("#btn_add_transport_loading").remove();
                                    return false;
                                });
                            };
                        };
                        return false;
                    });

                });
            };
            if (ui.panel.id == 'ui-tabs-FleetTransportLink'){
                $("#link_all_fleet_div").load("/transportcont/get_fleet_resources_active_html",function(data){
                    $("#tbl_active_fleet_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var fleet_id = alltrim(col0text); 
                            var jqxhr = $.post("/transportcont/link_fleet_to_transport/"+fleet_id, function(data) {

                            });
                            //$("#edit_description").val(alltrim(col4text)); 
                            //$("#edit_unit").val(alltrim(col5text)); 
                            //$("#edit_qty").val(alltrim(col7text)); 
                            //$("#edit_price").val(alltrim(col8text)); 
                            //$("#edit_total").val(alltrim(col9text)); 
                            //$("#edit_description").focus(); 
                            $( "#dialog_schedule_transport" ).dialog("open");
                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
                $("#link_all_transport_div").load("/transportcont/get_transport_resources_active_html",function(data){
                    return false;
                });
            };
            if (ui.panel.id == 'ui-tabs-ScheduledTrips'){
                $("#transport_scheduled_trips").load("/transportcont/get_transport_scheduled_trips_html",function(data){
                    $("#tbl_active_transport_scheduled").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            return false;

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    $("#tbl_active_transport_scheduled").delegate('td','click',function(e){
                        e.preventDefault();
                        e.stopPropagation();
                        if ($(this).parent().index() != 0){ 
                            if ($(this).index() == 14){ 
                                //Edit Schedule
                                var orderitemid = $(this).parent().find("td").eq(0).html();
                                var col0text = $(this).parent().find("td").eq(0).html();
                                $("#req_id").val(alltrim(col0text)); 
                                $.get( "/transportcont/get_edit_dialog_schedule?req_id_edit="+alltrim(col0text), function( data ) {
                                        //console.log(data)
                                        $( "#transport_dialog_schedule_div" ).html( data );
                                        $( "#dialog_schedule_transport_edit" ).dialog({
                                            autoOpen: false,
                                            height: 480,
                                            width: 550,
                                            modal: true,
                                            buttons: {
                                                "Save": function() {
                                                    var bValid = true;

                                                    if ( bValid ) {

                                                        var formserial = $("#dialog_transport_schedule_frm_edit").serialize();

                                                        var jqxhr = $.post("/transportcont/schedule_transport_req_edit?"+formserial, function(data) {
                                                                $("#transport_tabs").tabs("select",0);
                                                                $("#transport_tabs").tabs("select",'ui-tabs-ScheduledTrips');
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
                                                        clear_form_elements($("#dialog_transport_schedule_frm_edit"));
                                                        $( this ).find('input').val('');
                                                        //$("#transport_dialog_schedule_div").remove();
                                                        $(this).remove();
                                                        //console.log("Made It Here");
                                                   }
                                        });
                                        var dateval = $("#schedule_date_edit").val(); 
                                        $("#schedule_date_edit").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate", dateval);
                                        //$("#schedule_date_edit").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                                        $("#schedule_timestart_edit").timepicker({
                                            'timeFormat':'H:i:s',
                                            'step':15,
                                            'minTime':'5am',
                                            'disableTimeRanges': [
                                                    ['8pm', '11:55pm'],
                                                    ['12am', '4am']
                                                ]
                                        });
                                        $( "#dialog_schedule_transport_edit" ).dialog("open");

                                });
                            };
                            if ($(this).index() == 15){ 
                                //console.log("Trash pressed");
                                var scopeid = $(this).parent().find("td").eq(0).html();
                                var uniqid = Math.random();
                                var curTabSelected = $('#transport_tabs .ui-tabs-active').index();
                                var jqxhr = $.post("/transportcont/unschedule_transport_req?req_id="+alltrim(scopeid), function(data) {
                                        $("#transport_tabs").tabs("select",0);
                                        $("#transport_tabs").tabs("select",'ui-tabs-ScheduledTrips');
                                       return false 
                                });

                            };
                        };
                    });
                });

            };
            if (ui.panel.id == 'ui-tabs-Directions'){
                //$("#transport_tabs").tabs("select",'ui-tabs-Directions');
                $("#map_canvas").css('width','100%');
            };
       },
    });
    $( "#transport_req_tabs" ).tabs({ 
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
        disable: function(event,ui){
            console.log("Disable pressed");
       },
       add: function(event,ui){
            console.log("Tab Added");
            $("#invoicing_tabs").tabs('select', '#' + ui.panel.id);
       },
       select: function(event,ui){
            console.log("select pressed old tab is:" +ui.oldPanel) 
            console.log("select pressed new tab is:" +ui.panel.id) 
       },
       beforeActivate: function(event,ui){
            if (ui.oldPanel){
            console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
            }
            console.log("beforeActivate pressed new tab is:" +ui.panel) 
       }
    });
    $( "#dialog_schedule_transport" ).dialog({
        autoOpen: false,
        height: 480,
        width: 550,
        //modal: true,
        buttons: {
            "Save": function() {
                var bValid = true;

                if ( bValid ) {

                    var formserial = $("#dialog_transport_schedule_frm").serialize();

                    var jqxhr = $.post("/transportcont/schedule_transport_req?"+formserial, function(data) {
                            $("#transport_tabs").tabs("select",'ui-tabs-ScheduledTrips');
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
                    clear_form_elements($("#dialog_transport_schedule_frm"));
                    $( this ).find('input').val('');
               }
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
    $("#schedule_timestart").timepicker({
        'timeFormat':'H:i:s',
        'step':15,
        'minTime':'5am',
        'disableTimeRanges': [
                ['8pm', '11:55pm'],
                ['12am', '4am']
            ]
    });
    $("#btn_add_new_transport_req").click(function(e){
                var jcnotext = $("#del_jcno").val();
                var del_date = $("#del_date_required").val();
                var from_start = $("#from_start").val();
                var to_end = $("#to_end").val();
                if (jcnotext == '' || del_date == '' || from_start == '' || to_end == ''){
                    $("#warningdiv").html("No Site, No Date, No From , No Destination, No Transport Request")
                        $("#warningdiv").fadeIn(2000,function(){
                            $("#warningdiv").fadeOut('slow')    
                        });return false;
                };
                var formserial = $("#transport_req_new_form").serialize();
                var jqxhr = $.post("/transportcont/save_new_transport_req?"+formserial,function(data){
                    var bill_reqid = data;
                    $("#transport_req_waybill_new").load("/transportcont/get_new_waybill_form/"+alltrim(bill_reqid),function(data){
                        $("#btn_save_new_way_bill").button();
                        $("#bill_reqid").css('width','80px');
                        $("#bill_item").css('width','80px');
                        $("#bill_unit").css('width','80px');
                        $("#bill_qty").css('width','80px');
                        $("#bill_description").css('width','300px');
                        $("#btn_add_new_transport_req").attr('disabled','disabled');
                        $("#del_jcno").attr('disabled','disabled');
                        $("#del_date_required").attr('disabled','disabled');
                        $("#request_person").attr('disabled','disabled');
                        $("#btn_add_new_transport_req").hide();

                        $("#btn_save_new_way_bill").click(function(e){
                            var formserial2 = $("#new_way_bill_form").serialize();

                            var jqxhr = $.post("/transportcont/save_new_way_bill?"+formserial2+"&bill_reqid="+bill_reqid,function(data){
                                $("#transport_req_waybill_all").load("/transportcont/get_transportreq_loading_all/"+alltrim(bill_reqid),function(data){
                                    $("#btn_add_transport_loading").remove();
                                    $("#btn_close_transport_loading").button();
                                    $("#btn_close_transport_loading").click(function(){
                                       window.close()  
                                    });
                                    return false;
                                });
                                return false;
                            });
                            $("#bill_item").val('');
                            $("#bill_unit").val('');
                            $("#bill_qty").val('');
                            $("#bill_description").val('');
                            return false;
                        });
                        $( "#transport_req_tabs" ).tabs("option","active", 1 );
                        return false;
                    });
                    $("#transport_req_waybill_all").load("/transportcont/get_transportreq_loading_all/"+alltrim(bill_reqid),function(data){
                            //$("#btn_close_transport_loading").remove();
                            $("#btn_add_transport_loading").remove();
                        return false;
                    });
                    return false;
                });
                return false;
    });
    $("#btn_search_driver_schedule").click(function(e){
                $("#transport_driver_schedules").empty();
                var formserial = $("#search_driver_schedule_frm").serialize();
                $("#transport_driver_schedules").load("/transportcont/get_transport_drivers_schedules_html?"+formserial,function(data){
                    return false;

                });

                return false;
    });
    $("#btn_search_schedule").click(function(e){
                $("#transport_scheduled_trips").empty();
                var formserial = $("#search_schedule_frm").serialize();
                $("#transport_scheduled_trips").load("/transportcont/get_transport_drivers_schedules_by_date_html?"+formserial,function(data){
                    return false;

                });

                return false;
    });
    $("#btn_search_dailytrip_sheet").click(function(e){
                $("#transport_driver_tripsheets").empty();
                var formserial = $("#search_dailytrip_sheet_frm").serialize();
                $("#transport_driver_tripsheets").load("/transportcont/get_transport_drivers_tripsheets_html?"+formserial,function(data){
                    return false;
                });

                return false;
    });
    $("#btn_add_dailytrip_sheet").click(function(e){
                $("#transport_driver_tripsheets").empty();
                var formserial = $("#search_dailytrip_sheet_frm").serialize();
                $("#transport_driver_tripsheets").load("/transportcont/get_new_dialog_tripsheet?"+formserial,function(data){
                    $( "#dialog_trip_sheet_transport" ).dialog({
                        autoOpen: false,
                        height: 680,
                        width: 750,
                        modal: true,
                        buttons: {
                            "Save": function() {
                                var bValid = true;

                                if ( bValid ) {
                                    var formserial = $("#dialog_transport_trip_sheet_frm").serialize();
                                    var jqxhr = $.post("/transportcont/save_new_tripsheet?"+formserial, function(data) {
                                            $("#transport_tabs").tabs("select",'ui-tabs-DailyTripSheets');
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
                                    //clear_form_elements($("#dialog_transport_trip_sheet_frm"));
                                    $( this ).find('input').val('');
                                    window.location.reload();
                               }
                    });
                    $("#trip_sheet_schedule_id").css('width','500px');
                    $("#trip_sheet_timestart").timepicker({
                        'timeFormat':'H:i:s',
                        'step':05,
                        'minTime':'5am',
                        'disableTimeRanges': [
                                ['8pm', '11:55pm'],
                                ['12am', '4am']
                            ]
                    });
                    $("#trip_sheet_timeend").timepicker({
                        'timeFormat':'H:i:s',
                        'step':05,
                        'minTime':'5am',
                        'disableTimeRanges': [
                                ['8pm', '11:55pm'],
                                ['12am', '4am']
                            ]
                    });
                    $( "#dialog_trip_sheet_transport" ).dialog("open");
                    return false;
                });
                return false;
    });
    $("#del_date_required").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#btn_add_new_transport_req").button();
    $("#schedule_fleet_id").css('width','400px');
    $("#transport_tabs" ).tabs("option","active", 1 );
    $("#btn_search_driver_schedule").button();
    $("#btn_search_dailytrip_sheet").button();
    $("#btn_add_dailytrip_sheet").button();
    $("#btn_search_schedule").button();
    var dateval = new Date();
    $("#schedule_driver_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate",dateval );
    $("#schedule_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate",dateval );
    $("#schedule_driver_name").css('width','400px');
    $("#trip_sheet_fleet_id").css('width','400px');
    $("#trip_sheet_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate",dateval );

    //$(window).trigger('resize');
    //$("#ui-tabs-Directions").css('height','100%');
    //$("#map_canvas").css('height','100%');
    //$("#transport_tabs").tabs("select",'ui-tabs-Directions');
    //$("#transport_tabs").tabs("select",'ui-tabs-DailyTripSheets');
    //$("#map_canvas").css('width','100%');
    function debugrun(){
        $("#del_jcno").val(2575);
        $("#del_date_required").val('2014-01-09');
        $("#from_start").val('From Here');
        $("#to_end").val('To Here');
        $("#btn_add_new_transport_req").trigger('click');
    };
    //debugrun();
});

