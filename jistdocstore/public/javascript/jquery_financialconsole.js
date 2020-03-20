//Handels the financial pages
//Dec 2012-12-31
$(document).ready(function(){
    $( "#financial_tabs" ).tabs({ 
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
            if (ui.panel.id=='ui_tabs_GraphView'){
                ajqhr = $.get( "/mngntcont/get_contracts_wip_balances_all_point_json", function(point_data) {
                    var myJSONData = {
                      'data': [9,8,3,6],
                      'labels': ['BoBGT','Lucy','Gary','Hoolio'],
                      'tooltips': ['Bob did well','Lucy had her best result','Gary - not so good','Hoolio had a good start']
                     }
                    var point_list = $.parseJSON(point_data);
                    console.log(point_list.data) 
                    var myChart = new RGraph.Bar('contract_bars_canvas', point_list.data)
                        .set('tooltips', point_list.tooltips)
                        .set('labels', point_list.labels)
                        .draw();
                });
            };
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
    $("#button_get_messages_date").click(function(){
      var $combo_invoicelist = $("#combo_invoicelist"); 
      var $invoiceid = $("#invoiceid"); 
      var selected_invoicelist = $combo_invoicelist.val();
      var formserial = $("#invoice_payment_form").serialize();
      //console.log(formserial);
      var jrkqxhr = $.post("/invoicingcont/savenewinvoicepayment/"+$combo_invoicelist.val()+"?"+formserial, function(data1,status1,xhr1) {
              var $combo_invoicelist = $("#combo_invoicelist"); 
              $("#combo_invoicelist").trigger("change");
              return false;
            });
      return false;
    }); 
    $( "li", $("#point_gallery") ).click(function(event) {
        var target = $( event.target );
        var person = $(this);    
        personid = person.children('div').html(),
        $("#financial_wip_per_point").load("/mngntcont/ajax_contracts_wip_balances_per_point/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
            //alert("External content loaded successfully!");
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
});


