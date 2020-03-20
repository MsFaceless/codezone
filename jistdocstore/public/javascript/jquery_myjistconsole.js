//Handels the myjist pages
//Dec 2012-12-31
$(document).ready(function() {
    $( "#myjistconsole_tabs" ).tabs({ 
        heightStyle: "fill", 
    beforeLoad: function( event, ui ) {
        ui.jqXHR.error(function() {
            ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
        });
    },
    spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
    load: function( event, ui ) {
        $("#purchase_req_user_all_table").delegate('tr','mouseover mouseleave click',function(e) {
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
                //var selectedtab = $("#myjistconsole_tabs").tabs('option', 'selected');
                //$("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,selectedtab+1);
                //$("#myjistconsole_tabs").tabs('select', selectedtab+1);
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#purchase_req_user_all_table").delegate('td','click',function(e){
            e.preventDefault();
            e.stopPropagation();
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 8){ 
                    //console.log("delete pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random()
                };
                if ($(this).index() == 9){ 
                    //console.log("9 pressed");
                    var reqitemid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random();
                    $("#activereqitemid").val(reqitemid);
                    $( "#dialog_purchasereq_notes" ).dialog("open");
                    $( "#purchasereq_notes_all" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+reqitemid);
                };
                if ($(this).index() == 10){ 
                    //console.log("notes pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random();
                    var curTabSelected = $('#myjistconsole_tabs .ui-tabs-active').index();
                    var jqxhr = $.post("/logisticscont/ajaxToggleUserSideBuyingReq/"+scopeid, function(data) {
                        myuser = $("#activemyuser").val();
                        $("#myjistconsole_tabs").tabs("load",curTabSelected);
                    });
                };
                if ($(this).index() == 13){ 
                    //console.log("Trash pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random();
                    var curTabSelected = $('#myjistconsole_tabs .ui-tabs-active').index();
                    var jqxhr = $.post("/logisticscont/ajaxToggleUserActiveBuyingReq/"+scopeid, function(data) {
                        //$("#myjistconsole_tabs").tabs("load","ui-tabs-MyPOReqs");
                        $("#myjistconsole_tabs").tabs("load",curTabSelected);
                        return false;
                    });
                };
            };
        });
        $("#points_contract_table").delegate('tr','mouseover mouseleave click',function(e) {
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
                var selectedtab = $("#myjistconsole_tabs").tabs('option', 'selected');
                $("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(col0text));
                //$( "#grv_console_tabs" ).tabs("option","active", 2 );
                $('#myjistconsole_tabs ul:first li:eq(2) a').text("JCNo: "+col0text);
                $("#myjistconsole_tabs").tabs('select', 2);
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#tbltelephonemsg_per_person").delegate('tr','mouseover mouseleave click',function(e) {
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
                //var selectedtab = $("#myjistconsole_tabs").tabs('option', 'selected');
                //$("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,selectedtab+1);
                //$("#myjistconsole_tabs").tabs('select', selectedtab+1);
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#tbltelephonemsg_per_person").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 7){ 
                    //console.log("notes pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random()
            var jqxhr = $.post("/productioncont/toggletelephonemsg_active/"+parseInt(scopeid), function(data) {
                //myuser = $("#activemyuser").val();
                //$("#ui-tabs-MyPOReqs").load("/logisticscont/purchase_reqs_items_per_user/"+myuser)
                $("#myjistconsole_tabs").tabs("load",6)
                return false;
            })
                };
            };
        });
        $("#tbl_active_transport_my_reqs").delegate('tr','mouseover mouseleave click',function(e) {
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
                //var selectedtab = $("#myjistconsole_tabs").tabs('option', 'selected');
                //$("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,selectedtab+1);
                //$("#myjistconsole_tabs").tabs('select', selectedtab+1);
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#tbl_active_transport_my_reqs").delegate('td','click',function(e){
            e.preventDefault();
            e.stopPropagation();
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 10000){ 
                    //console.log("notes pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random();
                    var curTabSelected = $('#myjistconsole_tabs .ui-tabs-active').index();
                    var jqxhr = $.post("/logisticscont/ajaxToggleUserSideBuyingReq/"+scopeid, function(data) {
                        myuser = $("#activemyuser").val();
                        $("#myjistconsole_tabs").tabs("load",curTabSelected);
                    });
                };
                if ($(this).index() == 13){ 
                    //console.log("Trash pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random();
                    var curTabSelected = $('#myjistconsole_tabs .ui-tabs-active').index();
                    var reqtableindex = $(this).parent().index();
                    $("#ui-tabs-MyWayBills").load("/transportcont/get_transportreq_loading_all/"+alltrim(scopeid), function(data) {
                        $("#tbl_active_transport_req_loading").delegate('tr','mouseover mouseleave click',function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            if (e.type == 'mouseover') {
                                $(this).addClass("hover");
                            } else if ( e.type == 'click' ) {
                                var loadingid = $(this).find("td").eq(0).html();
                                $("#transport_dialog_loading_edit_div").load("/transportcont/get_edit_dialog_loading?req_id_edit="+alltrim(loadingid), function(data) {
                                            //$( "#transport_dialog_loading_div" ).html( data );
                                            $( "#dialog_loading_transport_edit" ).dialog({
                                                autoOpen: false,
                                                height: 480,
                                                width: 550,
                                                modal: true,
                                                buttons: {
                                                    "Save": function() {
                                                        var bValid = true;

                                                        if ( bValid ) {

                                                            var formserial = $("#dialog_loading_frm_edit").serialize();

                                                            var jqxhr = $.post("/transportcont/save_edit_way_bill?"+formserial, function(data) {
                                                                    //$("#myjistconsole_tabs").tabs("select",0);
                                                                    //$("#myjistconsole_tabs").tabs("select",'ui-tabs-ScheduledTrips');
                                                                        $("#tbl_active_transport_my_reqs").find("tr").eq(reqtableindex).find("td").eq(13).trigger("click");

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
                                                            $(this).remove();
                                                            //console.log("Made It Here");
                                                       }
                                            });
                                    $( "#dialog_loading_transport_edit" ).dialog("open");
                                    $("#loading_description").focus();
                                    return false;
                                });

                                return false;

                            }else   {
                                $(this).removeClass("hover");
                            }
                        });
                        $("#myjistconsole_tabs").tabs("select",'ui-tabs-MyWayBills');
                        $("#btn_close_transport_loading").remove();
                        $("#btn_add_transport_loading").button();
                        $( "#btn_add_transport_loading" ).click(function(){
                                $("#transport_dialog_loading_new_div").load("/transportcont/get_new_dialog_loading?req_id_edit="+alltrim(scopeid), function(data) {
                                            //$( "#transport_dialog_loading_div" ).html( data );
                                            $( "#dialog_loading_transport_new" ).dialog({
                                                autoOpen: false,
                                                height: 480,
                                                width: 550,
                                                modal: true,
                                                buttons: {
                                                    "Save": function() {
                                                        var bValid = true;

                                                        if ( bValid ) {

                                                            var formserial = $("#dialog_loading_frm_new").serialize();

                                                            var jqxhr = $.post("/transportcont/save_new_dialog_loading?"+formserial, function(data) {
                                                                    //$("#myjistconsole_tabs").tabs("select",0);
                                                                    //$("#myjistconsole_tabs").tabs("select",'ui-tabs-ScheduledTrips');
                                                                        $("#tbl_active_transport_my_reqs").find("tr").eq(reqtableindex).find("td").eq(13).trigger("click");

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
                                                            $(this).remove();
                                                            //console.log("Made It Here");
                                                       }
                                            });
                                    $("#loading_description_edit").focus();
                                    return false;
                                });
                                $( "#dialog_loading_transport_new" ).dialog("open");
                        });

                        //$("#myjistconsole_tabs").tabs("select",'ui-tabs-MyWayBills');
                    });
                };
            };
        });


        // close icon: removing the tab on click
        $( "#myjistconsole_tabs span.ui-icon-close" ).live( "click", function() {
            var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
            $( "#" + panelId ).remove();
            $("#myjistconsole_tabs").tabs( "refresh" );
        });
        // actual addTab function: adds new tab using the input from the form above
        function addTab(jcno,index) {
            var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>",
                tabCounter = 2;
            var label = "JCNo " + jcno,
                id = "ui-tabs-JCContract",
                li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) );
            //tabContentHtml = tabContent.val() || "Tab " + tabCounter + " content.";
            //$("#myjistconsole_tabs").find( ".ui-tabs-nav" ).append( li );
            //$("ul li:eq(1)").after($("<li>Pink Panther</li>"));
            $("#myjistconsole_tabs").find( ".ui-tabs-nav li:eq(1)" ).after( li );
            //$("#myjistconsole_tabs").append( "<div id='" + id + "'></div>" );
            tabCounter++;
            $("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
            $("#myjistconsole_tabs").tabs( "refresh" );
            //var thislen = $("#myjistconsole_tabs").tabs( "length" );
            $("#myjistconsole_tabs").tabs('select', 2);
        }
    }, 
    disable: function(event,ui){
                 console.log("Disable pressed");
             },
    add: function(event,ui){
             console.log("Tab Added");
             $("#myjistconsole_tabs").tabs('select', '#' + ui.panel.id);
         },
    select: function(event,ui){
            if (ui.panel.id == 'ui-tabs-6'){
                console.log(ui.panel.id);

            };
            if (ui.panel.id=='ui_tabs_GanttView'){
                callback_load_gantt_contract_daily_view('daily');
            };

        },
    beforeActivate: function(event,ui){
                        if (ui.oldPanel){
                         //   console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
                        }
                        //console.log("beforeActivate pressed new tab is:" +ui.panel) 
                    }
    });
    function callback_load_gantt_contract_daily_view(view,personid){
        $button_daily = $("#button_view_daily_gantt").button(), 
        $button_monthly = $("#button_view_monthly_gantt").button(), 
        ajqhr = $.get( "/mngntcont/get_point_contracts_json_dates_table", function(date_data) {
            var gridx = 35;
            var gridy = 35;
            var startx = gridx*5;
            var starty = gridy;
            var date_list = $.parseJSON(date_data);
            var div_width = date_list[0].totaldays * (gridy/2) + (gridy*23);
            ajqhr = $.get( "/mngntcont/get_point_contracts_json_daily_data", function(data) {
                var jsondata = $.parseJSON(data);
                var cont_no = jsondata.length
                var div_height = cont_no * gridx + startx;
                var str_div_height = div_height + 'px';
                var str_div_width = div_width + 'px';
                // Get bounds of dates to create gantt view
                $("#jist_contract_gantt_div").css('height',str_div_height);
                $("#jist_contract_gantt_div").css('width',str_div_width);
                jist_gantt_view = new JistGanttView('jist_contract_gantt_canvas');
                //jist_gantt_view.drawGrid('lightgray',0,0,gridx,gridy);
                jist_gantt_view.drawGrid('lightgray',gridx*20,gridy*2.5,gridx/2,gridy/2);
                //jist_gantt_view.drawRect(x,y,width,height);
                //Do Headers
                jist_gantt_view.drawText('JCNo',startx-gridx,starty,gridy*2,'start','bottom');
                jist_gantt_view.drawText('Contract Name',startx-gridx,starty*3,gridy*10,'start','bottom');
                jist_gantt_view.drawText('Plan Start',startx-gridx,starty*11,gridy*2,'start','bottom');
                jist_gantt_view.drawText('Plan End',startx-gridx,starty*13,gridy*2,'start','bottom');
                // Done Headers
                var rgba = 'rgba(120,120,120,0.1)'
                var rgba2 = 'rgba(120,120,120,0.5)'
                jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.8)';
                jist_gantt_view.drawRect(gridx,gridy*2.5,gridx*18.5,gridy*1,rgba2); // header left top
                jist_gantt_view.context.fillRect(gridx,gridy*2.5,gridx*18.5,gridy*1,rgba2);
                jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.1)';
                jist_gantt_view.drawRect(gridx,gridy*4,gridy*18.5,div_height,rgba); //contract info table
                jist_gantt_view.context.fillRect(gridx*20,gridy*2.5,div_width,gridy*1.5);
                //Write the contracts table
                for (var i = 0; i < jsondata.length; i += 1) {
                    //console.log(startx,starty);
                    jist_gantt_view.drawText(jsondata[i].jno,startx,starty,gridy*2,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].site,startx,starty*3,gridy*10,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].planstart,startx,starty*11,gridy*2,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].planend,startx,starty*13,gridy*2,'start','bottom');
                    startx = startx + gridx; 
                    starty = starty + 0; 
                };
                jist_gantt_view.context.font = '10pt Helvetica';
                //Write the date names on the date table
                var datelabel_startx = gridx*4;
                var datelabel_starty = gridy*20;
                for (var i = 0; i < date_list[0].dayslist.length; i += 1) {
                    jist_gantt_view.drawText(date_list[0].dayslist[i],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    datelabel_starty = datelabel_starty + gridy/2; 
                };
                //Write the date on the date table
                var datelabel_startx = gridx*3 +gridx/2;
                var datelabel_starty = gridy*20;
                for (var i = 0; i < date_list[0].dayslist.length; i += 1) {
                    jist_gantt_view.drawText(date_list[0].dateslist[i],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    if (i % 9 == 0){
                        jist_gantt_view.drawText(date_list[0].monthslist[i],datelabel_startx-(gridx/2),datelabel_starty,gridy*5,'start','bottom');
                    };
                    datelabel_starty = datelabel_starty + gridy/2; 
                };
                //Write the gantt table
                var datelabel_startx = gridx*5;
                var datelabel_starty = gridy*20;
                var ganttlabel_startx = gridx*5;
                var ganttlabel_starty = gridy*20;
                jist_gantt_view.context.save();
                for (var i = 0; i < jsondata.length; i += 1) {
                    //console.log(startx,starty);
                    //console.log(jsondata[i].ganttlist);
                    //jist_gantt_view.drawText(jsondata[i].ganttlist[0],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    var jsonobj = jsondata[i];
                    var ganttlabel_starty = gridy*20;
                    ganttlabel_startx = datelabel_startx
                    for (var x = 0; x < jsondata[i].ganttlist.length; x += 1) {
                        //console.log(jsonobj.ganttlist.length);
                        //console.log(jsonobj.ganttlist);
                        if (jsonobj.ganttlist[x] == 'T'){
                            //jist_gantt_view.drawText(jsonobj.ganttlist[x],ganttlabel_startx,ganttlabel_starty,gridy/2,'start','bottom');
                            if (date_list[0].dayslist[x] != 'S'){
                                jist_gantt_view.drawGanttBar(ganttlabel_starty,ganttlabel_startx-gridx/2,gridy/2,gridx/2); 
                            };
                        };
                        ganttlabel_starty = ganttlabel_starty + gridy/2; 
                        //ganttlabel_startx = ganttlabel_startx + gridx; 
                    };
                    datelabel_startx = datelabel_startx + gridx; 
                };
                jist_gantt_view.context.restore();
            });
            $button_daily.click(function(e){
                console.log('daily pressed');
            });
            $button_monthly.click(function(e){
                console.log('monthly pressed');
            });
            return false;
        });
    };
    function callback_load_gantt_contract_monthly_view(view){
        $button_daily = $("#button_view_daily_gantt").button(), 
        $button_monthly = $("#button_view_monthly_gantt").button(), 
        ajqhr = $.get( "/mngntcont/get_point_contracts_json_dates_table", function(date_data) {
            var gridx = 35;
            var gridy = 35;
            var startx = gridx*5;
            var starty = gridy;
            var date_list = $.parseJSON(date_data);
            var div_width = date_list[0].totaldays * (gridy/2) + (gridy*23);
            ajqhr = $.get( "/mngntcont/get_point_contracts_json_monthly_data", function(data) {
                var jsondata = $.parseJSON(data);
                var cont_no = jsondata.length
                var div_height = cont_no * gridx + startx;
                var str_div_height = div_height + 'px';
                var str_div_width = div_width + 'px';
                // Get bounds of dates to create gantt view
                $("#jist_contract_gantt_div").css('height',str_div_height);
                $("#jist_contract_gantt_div").css('width',str_div_width);
                jist_gantt_view = new JistGanttView('jist_contract_gantt_canvas');
                //jist_gantt_view.drawGrid('lightgray',0,0,gridx,gridy);
                jist_gantt_view.drawGrid('lightgray',gridx*20,gridy*2.5,gridx/2,gridy/2);
                //jist_gantt_view.drawRect(x,y,width,height);
                //Do Headers
                jist_gantt_view.drawText('JCNo',startx-gridx,starty,gridy*2,'start','bottom');
                jist_gantt_view.drawText('Contract Name',startx-gridx,starty*3,gridy*10,'start','bottom');
                jist_gantt_view.drawText('Plan Start',startx-gridx,starty*11,gridy*2,'start','bottom');
                jist_gantt_view.drawText('Plan End',startx-gridx,starty*13,gridy*2,'start','bottom');
                // Done Headers
                var rgba = 'rgba(120,120,120,0.3)'
                var rgba2 = 'rgba(120,120,120,0.5)'
                jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.8)';
                jist_gantt_view.drawRect(gridx,0,gridx*18.5,gridy*4,rgba); // header left top
                jist_gantt_view.context.fillRect(gridx,0,gridx*18.5,gridy*4,rgba2);
                jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.2)';
                jist_gantt_view.drawRect(gridx,gridy*4,gridy*18.5,div_height,rgba); //contract info table
                jist_gantt_view.context.fillRect(gridx*20,gridy*2.5,div_width,gridy*1.5);
                //Write the contracts table
                for (var i = 0; i < jsondata.length; i += 1) {
                    //console.log(startx,starty);
                    jist_gantt_view.drawText(jsondata[i].jno,startx,starty,gridy*2,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].site,startx,starty*3,gridy*10,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].planstart,startx,starty*11,gridy*2,'start','bottom');
                    jist_gantt_view.drawText(jsondata[i].planend,startx,starty*13,gridy*2,'start','bottom');
                    startx = startx + gridx; 
                    starty = starty + 0; 
                };
                jist_gantt_view.context.font = '10pt Helvetica';
                //Write the date names on the date table
                var datelabel_startx = gridx*4;
                var datelabel_starty = gridy*20;
                for (var i = 0; i < date_list[0].dayslist.length; i += 1) {
                    jist_gantt_view.drawText(date_list[0].dayslist[i],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    datelabel_starty = datelabel_starty + gridy/2; 
                };
                //Write the date on the date table
                var datelabel_startx = gridx*3 +gridx/2;
                var datelabel_starty = gridy*20;
                for (var i = 0; i < date_list[0].dayslist.length; i += 1) {
                    jist_gantt_view.drawText(date_list[0].dateslist[i],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    if (i % 9 == 0){
                        jist_gantt_view.drawText(date_list[0].monthslist[i],datelabel_startx-(gridx/2),datelabel_starty,gridy*5,'start','bottom');
                    };
                    datelabel_starty = datelabel_starty + gridy/2; 
                };
                //Write the gantt table
                var datelabel_startx = gridx*5;
                var datelabel_starty = gridy*20;
                var ganttlabel_startx = gridx*5;
                var ganttlabel_starty = gridy*20;
                jist_gantt_view.context.save();
                for (var i = 0; i < jsondata.length; i += 1) {
                    //console.log(startx,starty);
                    //console.log(jsondata[i].ganttlist);
                    //jist_gantt_view.drawText(jsondata[i].ganttlist[0],datelabel_startx,datelabel_starty,gridy/2,'start','bottom');
                    var jsonobj = jsondata[i];
                    var ganttlabel_starty = gridy*20;
                    ganttlabel_startx = datelabel_startx
                    for (var x = 0; x < jsondata[i].ganttlist.length; x += 1) {
                        //console.log(jsonobj.ganttlist.length);
                        //console.log(jsonobj.ganttlist);
                        if (jsonobj.ganttlist[x] == 'T'){
                            //jist_gantt_view.drawText(jsonobj.ganttlist[x],ganttlabel_startx,ganttlabel_starty,gridy/2,'start','bottom');
                            if (date_list[0].dayslist[x] != 'S'){
                                jist_gantt_view.drawGanttBar(ganttlabel_starty,ganttlabel_startx-gridx/2,gridy/2,gridx/2); 
                            };
                        };
                        ganttlabel_starty = ganttlabel_starty + gridy/2; 
                        //ganttlabel_startx = ganttlabel_startx + gridx; 
                    };
                    datelabel_startx = datelabel_startx + gridx; 
                };
                jist_gantt_view.context.restore();
            });
            $button_daily.click(function(e){
                console.log('daily pressed');
            });
            $button_monthly.click(function(e){
                console.log('monthly pressed');
            });
            return false;
        });
    };
    function callback_load_form_contract_update(){
        $( "#cont_planned_start_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#cont_planned_end_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#cont_site_handover_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#cont_actual_start_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#cont_first_del_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        $( "#cont_final_completion_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        var $dropdown_pointsstatus = $("#dropdown_points_status_update"), 
            $dropdown_siteagentstatus = $("#dropdown_siteagent_status_update"), 
            $dropdown_status_update = $("#dropdown_status_update"), 
            $button_status = $("#button_status_update_pressed"), 
            $tblcontractdata = $("#contractdata_table"),
            $tblcontractdatacontractual = $("#contractdata_contractual_table"),
            $tblcontractdatadates = $("#contractdata_dates_table");
        theText =$("#contractdata_table tr").find("td").eq(4).html();
        var thissitejcno = $("#activesitejcno").val();
        $("#contract_overview_scope").load("/contractscont/ajaxsitescontractscopeofwork/"+thissitejcno);
    };

    $(document).ajaxComplete(function(event, xhr, settings) {
        var newsettings = settings.url.split("/");
        //console.log(newsettings);
        if ( newsettings[2] === "ajaxsitescontractstatusupdate" ) {
            $( "#cont_planned_start_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
            $( "#cont_planned_end_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
            $( "#cont_site_handover_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
            $( "#cont_actual_start_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
            $( "#cont_first_del_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
            $( "#cont_final_completion_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );

            var $dropdown_pointsstatus = $("#dropdown_points_status_update"), 
        $dropdown_siteagentstatus = $("#dropdown_siteagent_status_update"), 
        $dropdown_status_update = $("#dropdown_status_update"), 
        $button_status = $("#button_status_update_pressed"); 
    //callback_load_form_contract_update();
    $dropdown_pointsstatus.val($("#activesitepoint").val());
    $dropdown_siteagentstatus.val($("#activesitesiteagent").val());
    $dropdown_status_update.val($("#activesitestatus").val());
    $( "#cont_planned_start_date" ).val($("#activesiteplanstart").val());
    $( "#cont_planned_end_date" ).val($("#activesiteplanend").val());
    $( "#cont_site_handover_date" ).val($("#activesitesitehandover").val());
    $( "#cont_actual_start_date" ).val($("#activesiteactualstart").val());
    $( "#cont_first_del_date" ).val($("#activesitefirstdel").val());
    $( "#cont_final_completion_date" ).val($("#activesitefinalcompletion").val());
    //console.log($("#activesitepoint"));
    $( "#button_status_update_pressed" ).click(function(e){
        //$button_daily
        var formserial = $("#contract_status_form").serialize();
        //console.log(formserial);
        e.preventDefault();
        var uniqid1 = Math.random();
        var thissitejcno = $("#activesitejcno").val();
        var act_point = $dropdown_pointsstatus.val(),
        act_siteagent = $dropdown_siteagentstatus.val(),
        act_status = $dropdown_status_update.val();
    var jrkqxhr = $.post("/contractscont/ajaxeditcontractstatus/"+uniqid1+"/"+thissitejcno+"/"+act_point+"/"+act_siteagent+"/"+act_status+"?"+formserial, function(data1,status1,xhr1) {
        $("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(thissitejcno));
        $("#ui-tabs-Contractual").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(thissitejcno));
    });
    });
    $( "myjistconsole_tabs" ).on( "tabsbeforeactivate", function( event, ui ) {
        console.log("made it here"); 
    } )
    var thissitejcno = $("#activesitejcno").val();
    $("#contract_overview_scope").load("/contractscont/ajaxsitescontractscopeofwork_production/"+thissitejcno);
    //$( "#tabs-1" ).text( "Triggered ajaxComplete handler. The result is " +
    //                 xhr.responseHTML );
        }
    });
    $("#button_create_new_purchase_req").click(function(){
        window.open('/logisticscont/purchase_requisition_new', '_blank');
        window.opener.focus();
        return false;
    });
    $("#button_create_new_transport_req").click(function(){
        window.open('/transportcont/transport_req_console', '_blank');
        window.opener.focus();
        return false;
    });
    $("#button_upload_docs").click(function(){
        window.open('/productioncont/fileuploadconsole', '_blank');
        window.opener.focus();
        return false;
    });
    $("#button_go_jisterp").click(function(){
        var strWindowFeatures = "menubar=yes,location=yes,resizable=yes,scrollbars=yes,status=yes";
        var thiswin = window.open('http://localhost:8069', '_blank',strWindowFeatures);
        //var thiswin = window.open('http://jisttrading.no-ip.org:1337', '_blank',strWindowFeatures);
        //var logon = thiswin.document.getElementsByName('login');
        //console.log(thiswin);
        $(thiswin.opener.document).ready(function(){
            $(thiswin.opener.document.body).append('<p>this is it</p>');
            var logon = thiswin.opener.document.body;
            console.log(logon);
        });   
        thiswin.opener.focus();
        //return false;
    });
    $("#div_pics_site").css('width','48%');
    $("#div_pics_site").css('float','left');
    $("#jcno_upload_list_shared").css('width','48%');
    $("#search_pic_jcno").css('width','100px');
    $("#search_pic_client").css('width','200px');
    $("#search_pic_sitename").css('width','200px');
    $("#search_pic_description").css('width','200px');
    $("#search_pic_orderno").css('width','100px');
    $("#button_search_pic_jcno").button();
    $("#button_search_pic_client").button();
    $("#button_search_pic_sitename").button();
    $("#button_search_pic_description").button();
    $("#button_search_pic_orderno").button();
    $("#button_add_new_pic").button();
    $("#button_go_jisterp").button();
    $("#button_search_pic_jcno").click(function(){
        $('#jcno_upload_list_shared').empty();
        var searchphrase = $("#search_pic_jcno").val()
        $("#div_pics_site").empty();
        $("#div_pics_site").load("/contractscont/get_search_pics?switch=JCNo&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_pics_table();
            return false;
        });
    });
    $("#button_search_pic_sitename").click(function(){
        $('#jcno_upload_list_shared').empty();
        var searchphrase = $("#search_pic_sitename").val()
        $("#div_pics_site").empty();
        $("#div_pics_site").load("/contractscont/get_search_pics?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_pics_table();
            return false;
        });
    });
    $("#button_search_pic_client").click(function(){
        $('#jcno_upload_list_shared').empty();
        var searchphrase = $("#search_pic_client").val()
        $("#div_pics_site").empty();
        $("#div_pics_site").load("/contractscont/get_search_pics?switch=SearchClient&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_pics_table();
            return false;
        });
    });
    $("#button_search_pic_description").click(function(){
        $('#jcno_upload_list_shared').empty();
        var searchphrase = $("#search_pic_description").val()
        $("#div_pics_site").empty();
        $("#div_pics_site").load("/contractscont/get_search_pics?switch=SearchDescription&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_pics_table();
            return false;
        });
    });
    $(".thispoint").click(function(event) {
        $("#outputpoints").empty();
        //$( "#droppable" ).addClass( "newClass", 1000, callbackgallery );
        var target = $( event.target );
        var personid = $(this).attr('value');    
        $("#outputpoints").load("/mngntcont/ajaxgetmanagepoints/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
    $(".point_gantt").click(function(event) {
                var personid = $(this).attr('value');    
                callback_load_gantt_contract_daily_view('daily',personid);
    });
    $(window).resize(function(){
        var winwidth = $(window).width(); 
        setscreensize(winwidth);
    });
    function activate_pics_table(){
    $('.pics_by_jcno').click(function() {
        var thisval = $('#pics_by_jcno').val();
        var thisjcno = $(this).attr('jcno');
        $('#jcno_upload_list_shared').empty();
        $('#jcno_upload_list_shared').load("/productioncont/uploads_thumbs_per_jcno/"+thisjcno,function(){
            $('.thumb_clicked').click(function() {
                //console.log($(this));
                var picpath = $(this).attr('value');
                window.open('/productioncont/production_pic_viewer_jcno?fname='+picpath, '_blank');
                return false;
            });
        return false;
        });
        return false;
    });
    
    };
    function doJistConsoleIntervalUpdate()
    {
        $("#myjistconsole_myactivity_count").load("/productioncont/getmyjistbioinfo",function(){
        });
        setInterval (function(){
            $("#myjistconsole_myactivity_count").load("/productioncont/getmyjistbioinfo",function(){
                var $countdown = $("#countdown");
                var count = 24;
                //$countdown.html($(window).width());
                thiscount = setInterval(function(){
                    //$countdown.html($(window).width());
                    if (count == 0){
                        //$countdown.html($(window).width());
                        return false;
                    }else if(count>10){
                        $countdown.html("Idle !!!!!") 
                    //do nothing
                    }else{
                        $countdown.html("Updating in : "+count+" s") 
                    }
                    count--;

                },1000);  
                return false;
            });
        }, 
        24000 );
    };
    function open_in_new_tab(url )
    {
        window.open(url, '_blank');
        window.opener.focus();
    };
    $("input:radio").click(function(){
        if ( $(this).attr('checked')){
            var size = $(this).attr('value');
            setscreensize(size)
        }
    });
    $("#screensize_radio").buttonset();
    $("#button_create_new_purchase_req").button();
    $("#button_create_new_transport_req").button();
    $("#button_create_sitemeeting_req").button();
    $("#button_upload_docs").button();
    doJistConsoleIntervalUpdate();
    var depth = 2;
    var width = 90;
    var angle = 0;
    var canvas_space = 21;
    var arc_space_top = 16;
    var arc_space_sides = 25;
    var arc_line_width = 1.7;
    var scale = 0.5;
    //sierpinski_init();
    sierpinski = new Sierpinski("logo_canvas");
    //sierpinski.drawSierpinskiTriangleLogo(depth,width,angle);
    //sierpinski.drawSierpinskiTriangleVariable(depth,width,angle,25,16,25,3);
    sierpinski.drawSierpinskiTriangleVariable(depth,width,angle,canvas_space,arc_space_top,arc_space_sides,arc_line_width,scale);
    //console.log($(window).width()); 
    //setscreensize($(window).width());
    $(window).trigger("resize");
    //setscreensize(1900);
    //
});
function setscreensize(width){
    //console.log($(document).width())
    //console.log($(window).width())
    //console.log($(screen).width())
    //console.log(width)
    var navbar = width - 200
    var app_cont = width - 20
    $("#header").hide();
    $(".notice").hide();
    $(".loggedname").show();
    $("body").css('width',width+'px');
    $("body").css('height','100%');
    $(".navbar").css('width',navbar +'px');
    $("#app_container").css('width',app_cont + 'px');
    $("#app_container").css('height','100%');
    $("#myjistconsole_tabs").css('height','800px');
    $("#invoicing_tabs").css('height','800px');
    $("#payreq_tabs").css('height','800px');
    $("#transport_tabs").css('height','800px');
    $("#fleet_tabs").css('height','800px');
    $("#financial_tabs").css('height','800px');
    $("#contract_overview_tabs").css('height','800px');
    $("#reception_tabs").css('height','800px');
    $("#buying_console_tabs").css('height','800px');
    $("#grv_console_tabs").css('height','800px');
    $("#fileupload_tabs").css('height','800px');
    $("#eskom_5yr_fencing_tabs").css('height','800px');
    $("#ess_3yr_palisade_fencing_tabs" ).css('height','800px');
    $("#ess_3yr_palisade_fencing_production_tabs" ).css('height','800px');
    $("#manufacture_process_tabs" ).css('height','800px');
    $("#manufacture_raw_mat_tabs" ).css('height','800px');
    $("#manufacture_orders_tabs" ).css('height','800px');
    $("#rental_console_tabs" ).css('height','800px');
    $("#labour_teams_schedule_tabs" ).css('height','800px');
    $("#labour_teams_tabs" ).css('height','800px');
    $("#labour_employees_tabs" ).css('height','800px');
    $("#contact_employees_tabs" ).css('height','800px');
    $("#site_address_tabs" ).css('height','800px');
};
