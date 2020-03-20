$(document).ready(function() {
    $( "#manufacture_orders_tabs" ).tabs({ 
        heightStyle: "fill", 
        height: "600px",
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            //$( "#grv_console_tabs" ).tabs("option","deactive", 2 );
            function addTab(jcno,index) {
                var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>",
                    tabCounter = 2;
                var label = "JCNo " + jcno,
                    id = "ui-tabs-UploadedPicture",
                    li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) );
                    //tabContentHtml = tabContent.val() || "Tab " + tabCounter + " content.";
                //$("#fileupload_tabs").find( ".ui-tabs-nav" ).append( li );
                //$("ul li:eq(1)").after($("<li>Pink Panther</li>"));
                $("#fileupload_tabs").find( ".ui-tabs-nav li:eq(1)" ).after( li );
                //$("#fileupload_tabs").append( "<div id='" + id + "'></div>" );
                tabCounter++;
                //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
                //$("#fileupload_tabs").tabs( "refresh" );
                //var thislen = $("#fileupload_tabs").tabs( "length" );
                $("#fileupload_tabs").tabs('select', 2);
            }
        }, 
        disable: function(event,ui){
            console.log("Disable pressed");
       },
       add: function(event,ui){
            console.log("Tab Added");
            $("#fileupload_tabs").tabs('select', '#' + ui.panel.id);
       },
       beforeActivate: function(event,ui){
            if (ui.oldPanel){
            //console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
            }
            //console.log("beforeActivate pressed new tab is:" +ui.panel) 
       },
       select: function(event,ui){
            console.log("select pressed old tab is:" +ui.oldPanel) 
            console.log("select pressed new tab is:" +ui.panel.id) 
            console.log(ui.panel.id);
            if (ui.panel.id=='ui_tabs_GraphView'){

            };
       },
       load: function(event,ui){
            $("#tbl_active_jjmc_orderlist").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                e.stopPropagation();
                //console.log("Pay reqs Pressed");
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col2text = $(this).find("td").eq(2).html();
                    var col3text = $(this).find("td").eq(3).html();
                    var col4text = $(this).find("td").eq(4).html();
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#tbl_active_jjmc_orderlist").delegate('td','click',function(e){
                  if ($(this).parent().index() != 0){ 
                      //var totalincl = $(this).parent().find("td").eq(4).html();
                      //var orderid = $(this).parent().find("td").eq(0).html();
                      if ($(this).index() == 10){ 
                            //console.log("notes pressed");
                            var uniqid = Math.random()
                            var scopeid = $(this).parent().find("td").eq(0).html();
                            var jqxhr = $.post("/manufacturecont/ajaxToggleManufacturingProduction?orderitem_id="+parseInt(scopeid), function(data) {
                                    $("#ui-tabs-1").empty();
                                    var selected = $("#manufacture_orders_tabs").tabs('option', 'selected');
                                    $("#manufacture_orders_tabs").tabs('load', selected);
                                    return false;
                                })
                      };
                      if ($(this).index() == 8999){ 
                            var activesplitreqid = $(this).parent().find("td").eq(0).html();
                            $("#activesplitreqid").val(activesplitreqid);
                            $("#split_req_total_incl").val(alltrim(totalincl)); 
                            $( "#split_req_must_pay_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                            $( "#dialog_pay_req_split_payment" ).dialog("open");
                            $(this).addClass("hover");
                      };
                  };
            });
       }
    });
    $( "#manufacture_raw_mat_tabs" ).tabs({ 
        heightStyle: "fill", 
        height: "600px",
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
                $("#tbl_comp_list").delegate('tr','mouseover mouseleave click',function(e) {
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
                $("#tbl_comp_list").delegate('td','click',function(e){
                    var itemid = $(this).parent().find("td").eq(0).html();
                    var itemdescr = $(this).parent().find("td").eq(1).html();
                    var itemunit = $(this).parent().find("td").eq(2).html();
                    var itemqty = $(this).parent().find("td").eq(3).html();
                    var parentindex = $(this).parent().index();
                    if ($(this).parent().index() != 0){ 
                        if ($(this).index() == 2){ 
                            $("#dialog_add_manitem").load( "/manufacturecont/get_dialog_standarditem_add?item_id="+alltrim(itemid), function( data ) {
                                $( "#dialog_add_manufacturing_item" ).dialog({
                                    autoOpen: true,
                                    height: 580,
                                    width: 550,
                                    modal: true,
                                    buttons: {
                                        "Save": function() {
                                            var bValid = true;

                                            if ( bValid ) {

                                                $("#listid").prop('disabled',false)
                                                var formserial = $("#dialog_add_manufacturing_item_frm").serialize();

                                                var jqxhr = $.post("/manufacturecont/add_new_manufacturing_item_to_list?"+formserial, function(data) {
                                                        $("#tbl_comp_list").find("tr").eq(parentindex).find("td").eq(6).trigger("click");
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
                                                //$(this).hide();
                                                //console.log("Made It Here");
                                           }
                                });
                                $( "#dialog_add_manufacturing_item" ).dialog("open");
                                $("#listid").prop('disabled',true)
                                $("#matname").focus();
                            });
                        };
                        if ($(this).index() == 3){ 
                            $("#dialog_add_manitem").load( "/manufacturecont/get_dialog_standarditem_edit?item_id="+alltrim(itemid), function( data ) {
                                $( "#dialog_edit_manufacturing_item" ).dialog({
                                    autoOpen: true,
                                    height: 380,
                                    width: 550,
                                    modal: true,
                                    buttons: {
                                        "Save": function() {
                                            var bValid = true;

                                            if ( bValid ) {

                                                $("#listid").prop('disabled',false)
                                                var formserial = $("#dialog_edit_manufacturing_item_frm").serialize();

                                                var jqxhr = $.post("/manufacturecont/save_edit_manufacturing_item_to_list?"+formserial, function(data) {
                                                        //$("#tbl_comp_list").find("tr").eq(parentindex).find("td").eq(6).trigger("click");
                                                        window.location.reload();
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
                                                //$(this).hide();
                                                //console.log("Made It Here");
                                           }
                                });
                                $( "#dialog_edit_manufacturing_item" ).dialog("open");
                                $("#listid").prop('disabled',true)
                                $("#matname").focus();
                            });
                        };
                        if ($(this).index() == 4){ 
                            return false;
                        };
                        if ($(this).index() == 6){ 
                            $("#divstandardmatlistitems").load("/manufacturecont/get_table_data_manufacturing_item?itemid="+itemid,function(data){
                                //console.log("Load Pressed");
                                $("#tbl_comp_list_items").delegate('tr','mouseover mouseleave click',function(e) {
                                    e.preventDefault();
                                    if (e.type == 'mouseover') {
                                        $(this).addClass("hover");
                                    } else if ( e.type == 'click' ) {
                                        var values = '';
                                        var tds = $(this).find('td');
                                    }else   {
                                        $(this).removeClass("hover");
                                    }
                                });
                                $("#tbl_comp_list_items").delegate('td','click',function(e){
                                    var itemiditems = $(this).parent().find("td").eq(0).html();
                                    var itemdescr = $(this).parent().find("td").eq(1).html();
                                    var itemunit = $(this).parent().find("td").eq(2).html();
                                    var itemqty = $(this).parent().find("td").eq(3).html();
                                    if ($(this).parent().index() != 0){ 
                                        if ($(this).index() == 4){ 
                                        };
                                        if ($(this).index() == 12){ 
                                            var jqxhr = $.post("/manufacturecont/delete_standard_list_item?itemid="+itemiditems, function(data) {
                                                $("#tbl_comp_list").find("tr").eq(parentindex).find("td").eq(6).trigger("click");
                                                //console.log("Delete Pressed");
                                            });

                                        };
                                    };
                                });
                            });

                        };
                        return false;
                    };
                });
        }, 
        disable: function(event,ui){
            console.log("Disable pressed");
       },
       add: function(event,ui){
            console.log("Tab Added");
            $("#fileupload_tabs").tabs('select', '#' + ui.panel.id);
       },
       beforeActivate: function(event,ui){
            //if (ui.oldPanel){
            //console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
            //}
            //console.log("beforeActivate pressed new tab is:" +ui.panel) 
       }
    });
    $( "#manufacture_process_tabs" ).tabs({ 
        heightStyle: "fill", 
        height: "600px",
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {

            $("#tbl_active_jjmc_progresslist").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                e.stopPropagation();
                //console.log("Pay reqs Pressed");
                var thisprogressindex = $(this).index();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col2text = $(this).find("td").eq(2).html();
                    var col3text = $(this).find("td").eq(3).html();
                    var col4text = $(this).find("td").eq(4).html();

                    $("#process_flow_div").load("/manufacturecont/get_jjmc_progress_stages?order_id="+alltrim(col0text),function(data){
                        var icons = {
                              header: "ui-icon-circle-arrow-e",
                              activeHeader: "ui-icon-circle-arrow-s"
                            };
                        $("#process_flow_accordion" ) .accordion({
                            header: "h3",
                            heightStyle: 'content', 
                            icons: icons,
                            active: 'false',
                          }).sortable({
                            axis: "y",
                            handle: "h3",
                            stop: function( event, ui ) {
                              // IE doesn't register the blur when sorting
                              // so trigger focusout handlers to remove .ui-state-focus
                              ui.item.children( "h3" ).triggerHandler( "focusout" );
                            }
                          });
                        $(".button_move_on").button();
                        var selected = $("#manufacture_process_tabs").tabs('option', 'selected');
                        $("#manufacture_process_tabs").tabs('select', 'ui-tabs-ProcessFlow');
                        $(".button_move_on").click(function(){
                            var man_stage_id = $(this).attr('man_stage_id')
                            var man_po_item = $(this).attr('man_po_item')
                            //console.log($(this).attr('man_po_item')); 
                                $.get( "/manufacturecont/get_edit_dialog_workflow?man_stage_id="+alltrim(man_stage_id)+"&man_po_item="+alltrim(man_po_item), function( data ) {
                                        //console.log(data)
                                        $( "#workflow_dialog_div" ).html( data );
                                        $( "#dialog_workflow_edit" ).dialog({
                                            autoOpen: false,
                                            height: 480,
                                            width: 550,
                                            modal: true,
                                            buttons: {
                                                "Save": function() {
                                                    var bValid = true;
                                                    if ( bValid ) {
                                                        $("#manstage_from").prop('disabled',false)
                                                        $("#man_jobid").prop('disabled',false)
                                                        var formserial = $("#dialog_workflow_frm_edit").serialize();
                                                        var jqxhr = $.post("/manufacturecont/save_edit_dialog_workflow?"+formserial, function(data) {
                                                                $("#tbl_active_jjmc_progresslist").find("tr").eq(thisprogressindex).find("td").trigger("click");
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
                                                        clear_form_elements($("#dialog_workflow_frm_edit"));
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
                                        $( "#dialog_workflow_edit" ).dialog("open");
                                        $("#manstage_from").prop('disabled',true);
                                        $("#man_jobid").prop('disabled',true);
                                        $("#man_stages_qty").focus();

                                });

                        });

                    });

                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#tbl_active_jjmc_progresslist").delegate('td','click',function(e){
                  if ($(this).parent().index() != 0){ 
                      //var totalincl = $(this).parent().find("td").eq(4).html();
                      //var orderid = $(this).parent().find("td").eq(0).html();
                      if ($(this).index() == 109898){ 
                            //console.log("notes pressed");
                            var uniqid = Math.random()
                            var scopeid = $(this).parent().find("td").eq(0).html();
                            var jqxhr = $.post("/manufacturecont/ajaxToggleManufacturingProduction?orderitem_id="+parseInt(scopeid), function(data) {
                                    $("#ui-tabs-1").empty();
                                    var selected = $("#manufacture_orders_tabs").tabs('option', 'selected');
                                    $("#manufacture_orders_tabs").tabs('load', selected);
                                    return false;
                                })
                      };
                  };
            });

        }, 
        disable: function(event,ui){
            console.log("Disable pressed");
       },
       add: function(event,ui){
            console.log("Tab Added");
            $("#fileupload_tabs").tabs('select', '#' + ui.panel.id);
       },
       beforeActivate: function(event,ui){
            //if (ui.oldPanel){
            //console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
            //}
            console.log("beforeActivate pressed new tab is:" +ui.panel) 
       },
       select: function(event,ui){
            console.log("select pressed old tab is:" +ui.oldPanel) 
            console.log("select pressed new tab is:" +ui.panel.id) 
            console.log(ui.panel.id);
       },
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
    $("#component_factory").load("/manufacturecont/get_skeleton_component_factory",function(data){
        $("#tbl_component_list").css('width','100%');
        $("#item_name").css('width','100%');
        $("#button_add_item_to_list").button();
        $("#button_add_item_to_list").hide();
        $("#item_name").hide();
    });
    $("#choose_material_group") .load("/manufacturecont/get_raw_mat_data",function(data){
        $("#id_mat_dropdown").change(function(){
            var thislistweight = $("#id_mat_dropdown").attr("weight");
            //console.log(thislistweight);
        });
        $("#select_raw_mat_group") .change(function(){
            var thismatgroup = $(this).val();
            //var mattype = $(this).attr('mattype');
            //console.log(mattype);
            $("#choose_material_each") .load("/manufacturecont/get_raw_mat_data_each?groupid="+thismatgroup,function(data){
                $("#tbl_component_list").delegate('tr','mouseover mouseleave click',function(e) {
                    e.preventDefault();
                    if (e.type == 'mouseover') {
                        $(this).addClass("hover");
                    } else if ( e.type == 'click' ) {
                        var values = '';
                        var tds = $(this).find('td');
                    }else   {
                        $(this).removeClass("hover");
                    }
                });
                $("#tbl_component_list").delegate('td','click',function(e){
                    var itemid = $(this).parent().find("td").eq(0).html();
                    var itemdescr = $(this).parent().find("td").eq(1).html();
                    var itemunit = $(this).parent().find("td").eq(2).html();
                    var itemqty = $(this).parent().find("td").eq(3).html();
                    if ($(this).parent().index() != 0){ 
                        if ($(this).index() == 4){ 
                        };
                        if ($(this).index() == 5){ 
                        };
                    };
                });
                //var thislistweight = $("#id_mat_dropdown").attr('weight');
                $("#diameter").css('width','50px');
                $("#mass_kg").css('width','50px');
                $("#width").css('width','50px');
                $("#height").css('width','50px');
                $("#length").css('width','50px');
                $("#quantity").css('width','50px');
                $("#thickness").css('width','50px');
                $("#stand_len").css('width','50px');
                $("#button_add_component_to_item").button();
                $("#id_mat_dropdown").change(function(){
                    var thislistid = $(this).val();
                    //console.log(thislistid);
                    jqxhr = $.get("/manufacturecont/get_material_item_weight?listid="+thislistid+"&groupid="+thismatgroup,function(data){
                        //var thislistweight = $("#id_mat_dropdown").attr("weight");
                        //console.log(thislistweight);
                        var thislistweight = data;
                        $("#mass_kg").val(parseFloat(thislistweight).toFixed(3));
                    });
                });
                $("#diameter").change(function(){
                    var thisdiameter = $(this).val();
                    if (thismatgroup==7 || thismatgroup==9 || thismatgroup==10){
                        jqxhr = $.get("/manufacturecont/get_material_solids_weight?diameter="+thisdiameter+"&groupid="+thismatgroup,function(data){
                            var thislistweight = data;
                            $("#mass_kg").val(parseFloat(thislistweight).toFixed(3));
                        });
                    };
                    if (thismatgroup==8){
                        var thisthickness = $("#thickness").val();
                        //console.log(thisthickness);
                        jqxhr = $.get("/manufacturecont/get_material_solids_weight?diameter="+thisdiameter+"&groupid="+thismatgroup+"&thickness="+thisthickness,function(data){
                            var thislistweight = data;
                            $("#mass_kg").val(parseFloat(thislistweight).toFixed(3));
                        });
                    };
                });
                $("#thickness").change(function(){
                    if (thismatgroup == 1 || thismatgroup == 2){
                        if (thismatgroup == 2){ //square rect convert to round
                            var this_height = parseFloat($("#height").val());
                            var this_width = parseFloat($("#width").val());
                            var thisdiameter = (((this_height*2)+(this_width*2))/4)/0.7874;
                            $("#diameter").val(parseFloat(thisdiameter).toFixed(3));
                            $("#diameter").blur();
                         
                        };
                        var thickness = $("#thickness").val();
                        var diameter = $("#diameter").val();
                        jqxhr = $.get("/manufacturecont/get_material_rounds_weight?diameter="+diameter+"&thickness="+thickness,function(data){
                            $("#mass_kg").val(parseFloat(data).toFixed(3));
                        });
                    };
                    if (thismatgroup == 11 || thismatgroup == 12){
                        var this_height = parseFloat($("#height").val());
                        var this_width = parseFloat($("#width").val());
                        var thickness = $("#thickness").val();
                        jqxhr = $.get("/manufacturecont/get_material_sheets_weight?groupid="+thismatgroup+"&height="+this_height+"&thickness="+thickness+'&width='+this_width,function(data){
                            $("#mass_kg").val(parseFloat(data).toFixed(3));
                        });

                    };
                });
                $("#button_add_component_to_item").click(function(){
                        var formserial = $("#material_calc_form").serialize();
                        //console.log(formserial);
                        //var thislistweight = $("#id_mat_dropdown").attr('weight');
                        var sel_raw_mat_group = $("#select_raw_mat_group").val();
                        var sel_raw_mat_grouptext = $("#select_raw_mat_group option:selected").text();
                        var id_mat_dropdown = $("#id_mat_dropdown").val();
                        var id_mat_dropdowntext = $("#id_mat_dropdown option:selected").text();
                        //console.log(id_mat_dropdowntext)
                        if (id_mat_dropdowntext == '' ){
                            id_mat_dropdowntext = id_mat_dropdown; 
                        };
                        //console.log(id_mat_dropdowntext)
                        var diameter = $("#diameter").val();
                        var mass_kg = $("#mass_kg").val();
                        var width = $("#width").val();
                        var height = $("#height").val();
                        var length = $("#length").val();
                        var quantity = $("#quantity").val();
                        var thickness = $("#thickness").val();
                        var stand_len = $("#stand_len").val();
                        $("#tbl_component_list tbody").append('<tr><td>'+sel_raw_mat_group+'</td><td>'+sel_raw_mat_grouptext+'</td><td>'+id_mat_dropdown+'</td><td>'+id_mat_dropdowntext+'</td><td>'+diameter+'</td><td>'+thickness+'</td><td>'+width+'</td><td>'+height+'</td><td>'+length+'</td><td>'+mass_kg+'</td><td>'+stand_len+'</td><td>'+quantity+'</td><td></td></tr>');
                        $("#button_add_item_to_list").show();
                        $("#item_name").show();
                        return false;
                     
                });
                $("#button_add_item_to_list").click(function(){
                    var object_name = $("#item_name").val();  
                    if (object_name == ''){
                         $("#warningdiv").html("Give the Item a Name Please !!!!")
                         $("#warningdiv").fadeIn(2000,function(){
                            $("#warningdiv").fadeOut('slow')    
                         });
                        return false;
                    };
                    $("#button_add_item_to_list").hide();
                    //$("#tbl_component_list", "tr").each(function(index, tr) {
                    //      var lines = $('td', tr).map(function(index, td) {
                    //       console.log($(td).text());
                    //       return $(td).text();
                    //        });
                    //});
                    $("#tbl_component_list").delegate('td','click',function(e){
                        var itemid = $(this).parent().find("td").eq(0).html();
                    });
                    var headers = $("th",$("#tbl_component_list")).map(function() { 
                        return this.innerHTML;
                    }).get();
                      
                    var rows = $("tbody tr",$("#tbl_component_list")).map(function() { 
                        return [$("td",this).map(function() { 
                          return this.innerHTML;     
                        }).get()];
                    }).get();
                    var tr_rows = $("tbody tr",$("#tbl_component_list")).map(function() { 
                          return this.innerHTML;     
                    }).get();
                    var table_contents = $("tbody table",$("#tbl_component_list")).map(function() { 
                          return this.innerHTML;     
                    }).get();

                    $('#tbl_component_list tr').each(function(index, tr) {
                        var lines = $('td', tr).map(function(index, td) {
                            return $(td).text();
                        });
                        //console.log(lines);
                    });
                    var jqxhr = $.post("/manufacturecont/post_table_data_manufacturing_item?headers="+headers+'&rows='+tr_rows+'&item_name='+object_name, function(data) {
                        window.location.reload();
                    });
                   //console.log(headers);
                   //console.log(rows);
                });

            });
        });
    });
    $("#manufacture_orders_tabs").tabs('select', 1);
    $("#manufacture_raw_mat_tabs").tabs('select', 1);
    $("#manufacture_process_tabs").tabs('select', 1);
});

