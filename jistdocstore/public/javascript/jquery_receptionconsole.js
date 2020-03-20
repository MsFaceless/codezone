//Handels the reception pages
//Dec 2012-12-31
$(function(){
    $( "#reception_tabs" ).tabs({ 
        heightStyle: "fill", 
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            //$( "#grv_console_tabs" ).tabs("option","deactive", 2 );
            $("#grv_back_button").click(function(){
                var selected = $("#invoicing_tabs").tabs('option', 'selected');
                $("#invoicing_tabs").tabs('remove', selected);
                $("#invoicing_tabs").tabs('select', selected - 1);
            });
             // close icon: removing the tab on click
            $( "#invoicing_tabs span.ui-icon-close" ).live( "click", function() {
                var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
                $( "#" + panelId ).remove();
                $("#invoicing_tabs").tabs( "refresh" );
            });
             // actual addTab function: adds new tab using the input from the form above
            function addTab(jcno,index) {
                var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>",
                    tabCounter = 2;
                var label = "JCNo " + jcno,
                    id = "ui-tabs-JCContract",
                    li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) );
                    //tabContentHtml = tabContent.val() || "Tab " + tabCounter + " content.";
                //$("#invoicing_tabs").find( ".ui-tabs-nav" ).append( li );
                //$("ul li:eq(1)").after($("<li>Pink Panther</li>"));
                $("#invoicing_tabs").find( ".ui-tabs-nav li:eq(1)" ).after( li );
                //$("#invoicing_tabs").append( "<div id='" + id + "'></div>" );
                tabCounter++;
                //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
                //$("#invoicing_tabs").tabs( "refresh" );
                //var thislen = $("#invoicing_tabs").tabs( "length" );
                $("#invoicing_tabs").tabs('select', 2);
            }
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
    $( "#dt_start_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#dt_last_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#telstartdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#outofoffice_telstartdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#myoutofoffice_telstartdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#message_radio").buttonset();
    $("#outofoffice_timestart").timepicker({
        'timeFormat':'H:i:s',
        'step':15,
        'minTime':'5am',
        'disableTimeRanges': [
                ['8pm', '11:55pm'],
                ['12am', '4am']
            ]
    });
    $("#telephonecall_message").attr('cols',40).attr('rows',10);
    $("#will_call_again").click(function(){
        $("#telephonecall_message").val('Person Will Call Again.');
    });
    $("#call_back").click(function(){
        $("#telephonecall_message").val('Please Call Back.');
    });
    $("#no_message").click(function(){
        $("#telephonecall_message").val('No Message Left.');
    });
    $("#btn_telephonecall_new").click(function(){
        var formserial = $("#telephonecall_new_form").serialize();
        //console.log(formserial);
        var toperson = $("#userlist");
        var topersonval = toperson.val();
        //console.log(topersonval);
        var jqxhr = $.post("/receptioncont/do_save_new_message?"+formserial+"&toperson="+topersonval, function(data) {
            clear_form_elements($("#telephonecall_new_form"));
            //$("#telephonecall_new_form").clearForm();
            return false;
        });
      return false;
    });
    $("#button_get_messages_dates").click(function(){
        //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
        startdate = $("#telstartdate").val();
        $("#output_telephonecall_view").load("/receptioncont/do_search_telephone_messages?dateadded="+startdate);
      return false;
    });
    $("#btn_outofoffice_new").click(function(){
        var formserial = $("#outofoffice_new_form").serialize();
        var toperson = $("#outofoffice_user_name");
        var topersonval = toperson.val();
        var sitename = $("#outofoffice_site_name");
        var sitenameval = sitename.val();
        var sitetimethere = $("#outofoffice_duration");
        var sitetimethereval = sitetimethere.val();
        var jqxhr = $.post("/receptioncont/do_save_new_out_of_office_movement?"+formserial+"&toperson="+topersonval+"&sitename="+sitenameval+"&outofoffice_est_hours_there="+sitetimethereval, function(data) {
            clear_form_elements($("#outofoffice_new_form"));
            //$("#telephonecall_new_form").clearForm();
            return false;
        });
      return false;
    });
    $("#button_get_outoffice_dates").click(function(){
        //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
        startdate = $("#outofoffice_telstartdate").val();
        $("#output_outofoffice_view").load("/receptioncont/do_search_outofoffice_movements?dateadded="+startdate);
      return false;
    });
    $("#button_get_myoutoffice_dates").click(function(){
        //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
        startdate = $("#myoutofoffice_telstartdate").val();
        $("#output_myoutofoffice_view").load("/productioncont/do_search_outofoffice_movements?dateadded="+startdate);
      return false;
    });
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
    function align_form_left_elements(ele) {
        $(ele).find(':input').each(function() {
            switch(this.type) {
                case 'password':
                case 'select-multiple':
                case 'select-one':
                case 'text':
                    $(this).css('margin-left','400px');
                case 'textarea':
                    $(this).val('');
                    break;
                case 'checkbox':
                case 'radio':
                    this.checked = false;
            }
        });

    }

});


