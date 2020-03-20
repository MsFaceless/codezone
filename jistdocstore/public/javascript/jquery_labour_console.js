$(function(){
    $( "#labour_employees_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#active_labour_tbl").delegate('tr','mouseover mouseleave click',function(e) {
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
        },
       select: function(event,ui){
            if (ui.panel.id=='ui-tabs-1'){
                $("#this_div").empty();
            };
        },
        //disabled: [2,4]
    });
    $( "#labour_teams_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#active_labour_tbl").delegate('tr','mouseover mouseleave click',function(e) {
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
        },
       select: function(event,ui){
            if (ui.panel.id=='ui-tabs-Labour_Force'){
                $("#div_labour_list").load("/labourcont/export_labour_list_active_html",function(responseTxt,statusTxt,xhr){
                    //console.log("printed");
                });
                $("#div_subcons_list").load("/labourcont/export_subcon_list_active_html",function(responseTxt,statusTxt,xhr){
                });
                $("#div_point_list").load("/labourcont/export_point_list_active_html",function(responseTxt,statusTxt,xhr){
                });
                $("#div_staff_list").load("/labourcont/export_staff_list_active_html",function(responseTxt,statusTxt,xhr){
                });
            };
            if (ui.panel.id=='ui-tabs-Labour_Divisions'){
                $("#div_labour_divisions_all").load("/labourcont/export_labour_divisions_active_html",function(responseTxt,statusTxt,xhr){
                    var icons = {
                          header: "ui-icon-circle-arrow-e",
                          activeHeader: "ui-icon-circle-arrow-s"
                        };
                    $("#division_accordion" ) .accordion({
                        header: "h3",
                        heightStyle: 'content', 
                        icons: icons,
                        active: 'false',
                        collapsible:'true',
                      }).sortable({
                        axis: "y",
                        handle: "h3",
                        collapsible:true,
                        stop: function( event, ui ) {
                          // IE doesn't register the blur when sorting
                          // so trigger focusout handlers to remove .ui-state-focus
                          ui.item.children( "h3" ).triggerHandler( "focusout" );
                        }
                      });
                    $("#button_division_add").button();
                    $("#button_division_add").click(function(event) {
                        $("#dialog_divisions").load( "/labourcont/get_dialog_add_division", function( data ) {
                            $( "#dialog_add_division_item" ).dialog({
                                autoOpen: true,
                                height: 280,
                                width: 550,
                                modal: true,
                                buttons: {
                                    "Save": function() {
                                        var bValid = true;

                                        if ( bValid ) {
                                            //$("#listid").prop('disabled',false)
                                            var formserial = $("#dialog_add_division_item_frm").serialize();
                                            var jqxhr = $.post("/labourcont/savenewdivision?"+formserial, function(data) {
                                                    var selected = $("#labour_teams_tabs").tabs('option', 'selected');
                                                    $("#labour_teams_tabs").tabs('select', selected-1);
                                                    $("#labour_teams_tabs").tabs('select', selected);
                                                    //return false 
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
                            $( "#dialog_add_division_item" ).dialog("open");
                            //$("#listid").prop('disabled',true)
                            //$("#matname").focus();
                        });
                    });
                    $("#tbl_division_list").delegate('tr','mouseover mouseleave click',function(e) {
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
                    $("#tbl_division_list").delegate('td','click',function(e){
                        var itemid = $(this).parent().find("td").eq(0).html();
                        var main_category_list_id = $(this).index();
                        var main_division = $(this).index();
                        var parent_main_category_list_id = $(this).parent().index();
                        if ($(this).parent().index() != 0){ 
                            if ($(this).index() == 2){ 
                                $.get( "/labourcont/get_dialog_change_division_name?division_id="+alltrim(itemid), function( data ) {
                                    //console.log("Printed from async");
                                    $( "#dialog_divisions" ).html( data );
                                    $("#from_id").prop('disabled',true)
                                    $( "#dialog_division_change" ).dialog({
                                        autoOpen: true,
                                        height: 280,
                                        width: 550,
                                        modal: true,
                                        buttons: {
                                            "Save": function() {
                                                var bValid = true;
                                                if ( bValid ) {
                                                    $("#from_id").prop('disabled',false)
                                                    var formserial = $("#dialog_division_change_frm").serialize();
                                                    //console.log(formserial);
                                                    var jqxhr = $.post("/labourcont/save_dialog_change_division_name?"+formserial, function(data) {
                                                            window.location.reload();
                                                    });
                                                    $( this ).dialog( "close" );
                                                }
                                            },
                                            Cancel: function() {
                                                        $( this ).dialog( "close" );
                                                    }
                                        },
                                        close: function() {
                                                    $( this ).find('input').val('');
                                                    $(this).remove();
                                               }
                                    });
                                });

                            };
                            if ($(this).index() == 3){ 
                                $("#div_labour_divisions").load("/labourcont/get_table_data_labour_divisions?itemid="+itemid,function(data){
                                    $("#tbl_labour_division_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                            
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_labour_division_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 3){ 
                                                $.get( "/labourcont/get_dialog_change_labour_division?labour_id="+alltrim(thisitemid), function( data ) {
                                                    //console.log("Printed from async");
                                                    $( "#dialog_divisions" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_division_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_division_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_labour_division?"+formserial, function(data) {
                                                                            $("#tbl_division_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                });
                                            }
                                        }
                                    });
                                });
                                $("#div_point_divisions").load("/labourcont/get_table_data_point_divisions?itemid="+itemid,function(data){
                                    $("#tbl_point_division_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                            
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_point_division_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_point_division?point_id="+alltrim(thisitemid), function( data ) {
                                                    //console.log("Printed from async");
                                                    $( "#dialog_divisions" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_division_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_division_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_point_division?"+formserial, function(data) {
                                                                            $("#tbl_division_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                });
                                            }
                                        }
                                    });
                                });
                                $("#div_staff_divisions").load("/labourcont/get_table_data_staff_divisions?itemid="+itemid,function(data){
                                    $("#tbl_staff_division_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                            
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_staff_division_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_staff_division?staff_id="+alltrim(thisitemid), function( data ) {
                                                    //console.log("Printed from async");
                                                    $( "#dialog_divisions" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_division_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_division_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_staff_division?"+formserial, function(data) {
                                                                            $("#tbl_division_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                });
                                            }
                                        }
                                    });
                                });
                                $("#div_subcons_divisions").load("/labourcont/get_table_data_subcon_divisions?itemid="+itemid,function(data){
                                    $("#tbl_subcon_division_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                            
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_subcon_division_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_subcon_division?subcon_id="+alltrim(thisitemid), function( data ) {
                                                    //console.log("Printed from async");
                                                    $( "#dialog_divisions" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_division_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_division_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_subcon_division?"+formserial, function(data) {
                                                                            $("#tbl_division_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                });
                                            }
                                        }
                                    });
                                    //console.log("Called point divs");
                                });
                            };
                            if ($(this).index() == 4){ 
                                return false;
                            };
                            if ($(this).index() == 600){ 
                                return false;
                            };
                            return false;
                        };
                    });
                });
                $("#div_labour_categories_all").load("/labourcont/export_labour_categories_active_html",function(responseTxt,statusTxt,xhr){
                    $("#tbl_categories_list").delegate('tr','mouseover mouseleave click',function(e) {
                        //e.preventDefault();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var values = '';
                            var tds = $(this).find('td');
                            var itemid = $(this).find("td").eq(0).html();

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    $("#tbl_categories_list").delegate('td','click',function(e){
                        var itemid = $(this).parent().find("td").eq(0).html();
                        if ($(this).parent().index() != 0){ 
                            if ($(this).index() == 3){ 
                                var main_category_list_id = $(this).index();
                                var parent_main_category_list_id = $(this).parent().index();
                                $("#div_labour_categories").load("/labourcont/get_table_data_labour_categories?itemid="+itemid,function(responseTxt,statusTxt,xhr){
                                    $("#tbl_labour_category_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        //e.preventDefault();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_labour_category_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 3){ 
                                                $.get( "/labourcont/get_dialog_change_labour_category?labour_id="+alltrim(thisitemid), function( data ) {
                                                    $( "#dialog_category" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_category_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_category_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_labour_category?"+formserial, function(data) {
                                                                            $("#tbl_categories_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                    $("#dialog_category_change").dialog("open");
                                                });
                                            }
                                        }
                                    });
                                    return false;

                                });
                                $("#div_point_categories").load("/labourcont/get_table_data_point_categories?itemid="+itemid,function(responseTxt,statusTxt,xhr){
                                    $("#tbl_point_category_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        //e.preventDefault();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_point_category_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_point_category?labour_id="+alltrim(thisitemid), function( data ) {
                                                    $( "#dialog_category" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_category_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_category_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_point_category?"+formserial, function(data) {
                                                                            $("#tbl_categories_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                    $("#dialog_category_change").dialog("open");
                                                });
                                            }
                                        }
                                    });
                                });
                                $("#div_staff_categories").load("/labourcont/get_table_data_staff_categories?itemid="+itemid,function(responseTxt,statusTxt,xhr){
                                    $("#tbl_staff_category_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        //e.preventDefault();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_staff_category_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_labour_category?labour_id="+alltrim(thisitemid), function( data ) {
                                                    $( "#dialog_category" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_category_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_category_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_staff_category?"+formserial, function(data) {
                                                                            $("#tbl_categories_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                    $("#dialog_category_change").dialog("open");
                                                });
                                            }
                                        }
                                    });
                                });
                                $("#div_subcon_categories").load("/labourcont/get_table_data_subcon_categories?itemid="+itemid,function(responseTxt,statusTxt,xhr){
                                    $("#tbl_subcon_category_list").delegate('tr','mouseover mouseleave click',function(e) {
                                        //e.preventDefault();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                        } else if ( e.type == 'click' ) {
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });
                                    $("#tbl_subcon_category_list").delegate('td','click',function(e){
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        if ($(this).parent().index() != 0){ 
                                            if ($(this).index() == 2){ 
                                                $.get( "/labourcont/get_dialog_change_subcon_category?labour_id="+alltrim(thisitemid), function( data ) {
                                                    $( "#dialog_category" ).html( data );
                                                    $("#from_id").prop('disabled',true)
                                                    $( "#dialog_category_change" ).dialog({
                                                        autoOpen: true,
                                                        height: 280,
                                                        width: 550,
                                                        modal: true,
                                                        buttons: {
                                                            "Save": function() {
                                                                var bValid = true;
                                                                if ( bValid ) {
                                                                    $("#from_id").prop('disabled',false)
                                                                    var formserial = $("#dialog_category_change_frm").serialize();
                                                                    //console.log(formserial);
                                                                    var jqxhr = $.post("/labourcont/save_dialog_change_subcon_category?"+formserial, function(data) {
                                                                            $("#tbl_categories_list").find("tr").eq(parent_main_category_list_id).find("td").eq(main_category_list_id).trigger("click");
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
                                                                    $( this ).find('input').val('');
                                                                    $(this).remove();
                                                               }
                                                    });
                                                    $("#dialog_category_change").dialog("open");
                                                });
                                            }
                                        }
                                    });
                                });
                            }
                        };
                    });
                });
            };
            if (ui.panel.id=='ui-tabs-Labour_DivViews'){
                $("#div_divisions_accordion").load("/labourcont/get_labour_division_people_html",function(responseTxt,statusTxt,xhr){
                    var icons = {
                          header: "ui-icon-circle-arrow-e",
                          activeHeader: "ui-icon-circle-arrow-s"
                        };
                    $("#labour_divisions_people_accordion" ) .accordion({
                        header: "h3",
                        heightStyle: 'content', 
                        icons: icons,
                        collapsible:true,
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
                });
                $("#div_categories_accordion").load("/labourcont/get_labour_categories_people_html",function(responseTxt,statusTxt,xhr){
                    var icons = {
                          header: "ui-icon-circle-arrow-e",
                          activeHeader: "ui-icon-circle-arrow-s"
                        };
                    $("#labour_categories_people_accordion" ) .accordion({
                        header: "h3",
                        heightStyle: 'content', 
                        icons: icons,
                        collapsible:true,
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
                });
            };
            if (ui.panel.id=='ui-tabs-Labour_TeamsCreate'){
                //$("#div_current_team").empty();
                callback_load_new_team_app();
            };
            if (ui.panel.id=='ui-tabs-Labour_TeamsView'){
                $("#div_labour_teams_accordion").load("/labourcont/get_labour_teams_accordion_html",function(responseTxt,statusTxt,xhr){
                    var icons = {
                          header: "ui-icon-circle-arrow-e",
                          activeHeader: "ui-icon-circle-arrow-s"
                        };
                    $("#labour_teams_accordion" ) .accordion({
                        header: "h3",
                        heightStyle: 'content', 
                        icons: icons,
                        collapsible:true,
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
                });
            };
        },
        //disabled: [2,4]
    });
    $( "#labour_teams_schedule_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                console.log(ui.id);
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            //$("#trip_sheet_fleet_id").css('width','400px');
            console.log("I'm Here");
        },
       select: function(event,ui){
            //console.log(ui.panel.id);
            if (ui.panel.id=='ui-tabs-Teams_DoSchedule'){
                $("#warningdiv").hide();
                $("#div_all_teams").load("/labourcont/get_labour_teams_picture_by_division_html",function(responseTxt,statusTxt,xhr){
                    //console.log("Made it");
                    $(".div_leader_accord_team_pic").css('width','50px');
                    $(".div_leader_accord_team_pic").css('height','50px');
                    $(".div_leader_accord_team_pic").click(function(event) {
                        $("#labour_teams_schedule_tabs").tabs('select', 2);
                        //$("#div_contract_section").empty();
                        $("#div_form_schedule_section").empty();
                        //$("#div_form_schedule_section").hide();
                        $("#div_this_team_section").empty();
                        $("#jist_contract_gantt_div").empty();
                        $("#div_schedule_task_section").empty();
                         $("#div_this_team_section").hide();
                         $("#div_schedule_task_section").hide();
                         $("#div_printing_menu").hide();
                         //$("#div_dialog_unschedule_date_team").hide();
                        var teamid = $(this).attr('myid')
                        $("#div_this_team_section").load("/labourcont/get_labour_team_people_html?teamid="+teamid,function(responseTxt,statusTxt,xhr){
                                    return false;
                        });
                        $("#jist_team_gantt_div").load("/labourcont/get_labour_schedule_team_gantt_div",function(responseTxt,statusTxt,xhr){
                                ajqhr = $.get( "/labourcont/get_schedule_labour_for_teams_dates_json?teamid="+teamid, function(date_data) {
                                    var gridx = 35;
                                    var gridy = 35;
                                    var startx = gridx*5;
                                    var starty = gridy;
                                    var date_list = $.parseJSON(date_data);
                                    var div_width = date_list[0].totaldays * (gridy/2) + (gridy*23);
                                    var allstart = date_list[0].startdate;
                                    var allend = date_list[0].enddate;
                                    ajqhr = $.get( "/labourcont/get_labour_schedule_teams_json_daily_data?teamid="+teamid+"&allstart="+allstart+"&allend="+allend, function(data) {
                                        var jsondata = $.parseJSON(data);
                                        var cont_no = jsondata.length
                                        var div_height = cont_no * gridx + startx;
                                        var str_div_height = div_height + 'px';
                                        var str_div_width = div_width + 'px';
                                        // Get bounds of dates to create gantt view
                                        //$("#jist_team_gantt_div").css('height',div_height + 20 + 'px');
                                        $("#jist_team_gantt_div").css('width',str_div_width);
                                        jist_gantt_view = new JistGanttView('jist_team_gantt_canvas');
                                        //jist_gantt_view.drawGrid('lightgray',0,0,gridx,gridy);
                                        jist_gantt_view.drawGrid('lightgray',gridx*20,gridy*2.5,gridx/2,gridy/2);
                                        //jist_gantt_view.drawRect(x,y,width,height);
                                        jist_gantt_view.context.font = '20pt Helvetica';
                                        jist_gantt_view.drawText('Schedule:'+jsondata[0].teamname,startx-gridx*4,starty,gridy*20,'start','bottom');
                                        jist_gantt_view.context.font = '10pt Helvetica';
                                        jist_gantt_view.drawText('From:'+' '+jsondata[0].allplanstart,startx-gridx*3,starty,gridy*4,'start','bottom');
                                        jist_gantt_view.drawText('To:'+' '+jsondata[0].allplanend,startx-gridx*3,starty*4,gridy*4,'start','bottom');
                                        jist_gantt_view.context.font = '10pt Helvetica';
                                        //Do Headers
                                        jist_gantt_view.drawText('JCNo',startx-gridx,starty,gridy*2,'start','bottom');
                                        jist_gantt_view.drawText('Site Name',startx-gridx,starty*2,gridy*5,'start','bottom');
                                        jist_gantt_view.drawText('Description',startx-gridx,starty*8,gridy*7,'start','bottom');
                                        jist_gantt_view.drawText('To Start',startx-gridx,starty*15,gridy*2,'start','bottom');
                                        jist_gantt_view.drawText('To End',startx-gridx,starty*17,gridy*2,'start','bottom');
                                        // Done Headers
                                        var rgba = 'rgba(120,120,120,0.1)'
                                        var rgba2 = 'rgba(120,120,120,0.5)'
                                        jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.8)';
                                        jist_gantt_view.drawRect(gridx,gridy*2.5,gridx*18.5,gridy*1,rgba2); // header left top
                                        jist_gantt_view.context.fillRect(gridx,gridy*2.5,gridx*18.5,gridy*1,rgba2);
                                        jist_gantt_view.context.fillStyle = 'rgba(120,120,120,0.1)';
                                        jist_gantt_view.drawRect(gridx,gridy*4,gridy*18.5,div_height-gridy/2,rgba); //contract info table
                                        jist_gantt_view.context.fillRect(gridx*20,gridy*2.5,div_width,gridy*1.5);
                                        //Write the contracts table
                                        for (var i = 0; i < jsondata.length; i += 1) {
                                            //console.log(startx,starty);
                                            jist_gantt_view.drawText(jsondata[i].jno,startx,starty,gridy*2,'start','bottom');
                                            jist_gantt_view.drawText(jsondata[i].site,startx,starty*2,gridy*5,'start','bottom');
                                            jist_gantt_view.drawText(jsondata[i].description,startx,starty*8,gridy*7,'start','bottom');
                                            jist_gantt_view.drawText(jsondata[i].planstart,startx,starty*15,gridy*2,'start','bottom');
                                            jist_gantt_view.drawText(jsondata[i].planend,startx,starty*17,gridy*2,'start','bottom');
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
                                        $("#jist_team_gantt_div").css('width','76%');
                                    });
                                });
                                     return false;
                        });
                        $("#div_printing_menu").load("/labourcont/get_labour_printing_form?teamid="+teamid+"&contractid=None",function(responseTxt,statusTxt,xhr){
                                     return false;
                        });
                        $("#div_form_schedule_section").load("/labourcont/get_labour_team_schedule_form?teamid="+teamid,function(responseTxt,statusTxt,xhr){
                            $( "#startdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                            //$("#teamid").prop('disabled',true);
                            $("#teamid").hide();
                            $("#button_schedule_team").button();
                            $("#button_unschedule_date").button();
                            $("#button_toggle_team_faces").button();
                            $("#button_toggle_contract_tasks").button();
                            $("#button_toggle_printing").button();
                            $("#button_toggle_team_faces").click(function(){
                                 //if ($("#div_this_team_section:hidden")){$("#div_this_team_section").show()};       
                                 //if ($("#div_this_team_section:visible")){$("#div_this_team_section").hide()};       
                                 $("#div_this_team_section").fadeToggle('fast');
                                 $("#jist_team_gantt_div").css('width','76%');
                                 $("#jist_team_gantt_div").css('float','left');
                            });
                            $("#button_toggle_contract_tasks").click(function(){
                                 $("#div_schedule_task_section").fadeToggle('fast');
                                 //$("#div_schedule_task_section").hide();
                                 $("#jist_team_gantt_div").css('width','76%');
                                 $("#jist_team_gantt_div").css('float','left');
                            });
                            $("#button_toggle_printing").click(function(){
                                 $("#div_printing_menu").fadeToggle('fast');
                            });
                            $("#button_schedule_team").click(function(){
                                //console.log("Made it");
                                //$("#teamid").prop('disabled',false);
                                $("#teamid").show();
                                var formserial = $("#team_schedule_frm").serialize();
                                var current_teamid = $("#teamid").val();
                                var jno = $("#jcno_listbox").val();
                                var thisdate = $("#startdate").val();
                                var thiscount = $("#days_count").val();
                                var thistask = $("#taskname").val();
                                if (jno == '' || thisdate == '' || thistask == '' || thiscount == '0'){return false;};
                                var jqxhr = $.get("/labourcont/check_schedule_team?"+formserial, function(data) {
                                    var check_list = $.parseJSON(data);
                                    //console.log(check_list.response)
                                    if (check_list.response=='success'){
                                        var jqxhr = $.post("/labourcont/schedule_team?"+formserial, function(data) {
                                            //callback to refresh screen
                                              $("#div_all_teams").find('img').each(function(e,htmlelement){
                                                  if ($(this).attr('myid')==current_teamid){
                                                    $(this).trigger('click'); 
                                                  };
                                              });
                                            return false;
                                        });
                                    }
                                    else if (check_list.response=='fail'){
                                         var thisdate = check_list.date
                                         $("#warningdiv").html(thisdate + " - Scheduled Already")
                                         $("#warningdiv").fadeIn(2000,function(){
                                            $("#warningdiv").fadeOut('slow')    
                                            $("#teamid").hide();
                                         });
                                        return false;
                                    };
                                });
                                return false;
                            });
                            $("#button_unschedule_date").button();
                            $("#button_unschedule_date").click(function(){
                                $("#div_dialog_unschedule_date_team" ).load("/labourcont/get_dialog_unschedule_date_team", function(data) {
                                        //$("#userid").prop('disabled',true);
                                        //$("#triggerUpload").button();
                                        $( "#un_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                                        $( "#dialog_unschedule_team_date_frm" ).dialog({
                                            autoOpen: true,
                                            height: 280,
                                            width: 350,
                                            modal: true,
                                            buttons: {
                                                "Save": function() {
                                                    var bValid = true;
                                                    if ( bValid ) {
                                                        var un_schedule_date = $("#un_date").val();
                                                        var jqxhr = $.post("/labourcont/delete_labour_schedule_date?thisdate="+alltrim(un_schedule_date)+"&teamid="+alltrim(teamid), function(data) {
                                                            //$("#button_create_new_team").prop('disabled',false);
                                                            //window.location.reload();
                                                              $("#div_all_teams").find('img').each(function(e,htmlelement){
                                                                  if ($(this).attr('myid')==teamid){
                                                                    $(this).trigger('click'); 
                                                                  };
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
                                                        $( this ).find('input').val('');
                                                        $(this).remove();
                                                   }
                                        });
                                        $("#dialog_unschedule_date_team_frm").dialog("open");
                                });
                            });
                            $("#jcno_listbox").change(function(){
                                var jcno = $(this).val();
                                $("#div_printing_menu").load("/labourcont/get_labour_printing_form?teamid="+teamid+"&contractid="+alltrim(jcno),function(responseTxt,statusTxt,xhr){
                                             return false;
                                });
                                $("#div_schedule_task_section").load("/labourcont/export_schedule_contract_tasks_html?contractid="+alltrim(jcno),function(responseTxt,statusTxt,xhr){
                                });
                                $("#jist_contract_gantt_div").load("/labourcont/get_labour_schedule_contract_gantt_div",function(responseTxt,statusTxt,xhr){
                                        ajqhr = $.get( "/labourcont/get_schedule_labour_for_contracts_dates_json?contractid="+jcno, function(date_data) {
                                            var gridx = 35;
                                            var gridy = 35;
                                            var startx = gridx*5;
                                            var starty = gridy;
                                            var date_list = $.parseJSON(date_data);
                                                if (date_list == null){
                                                     $("#warningdiv").html("Not Scheduled")
                                                     $("#warningdiv").fadeIn(2000,function(){
                                                        $("#warningdiv").fadeOut('slow')    
                                                        $("#teamid").hide();
                                                        return false;
                                                     });
                                                    return false;
                                                };
                                            var allstart = date_list[0].startdate;
                                            var allend = date_list[0].enddate;
                                            var div_width = date_list[0].totaldays * (gridy/2) + (gridy*23);
                                            ajqhr = $.get( "/labourcont/get_labour_schedule_contracts_json_daily_data?contractid="+jcno+"&teamid="+teamid+"&allstart="+allstart+"&allend="+allend, function(data) {
                                                var jsondata = $.parseJSON(data);
                                                var cont_no = jsondata.length
                                                var div_height = cont_no * gridx + startx;
                                                var str_div_height = div_height + 'px';
                                                var str_div_width = div_width + 'px';
                                                // Get bounds of dates to create gantt view
                                                //$("#jist_contract_gantt_div").css('height',str_div_height);
                                                $("#jist_contract_gantt_div").css('width',str_div_width);
                                                jist_gantt_view = new JistGanttView('jist_contract_gantt_canvas');
                                                //jist_gantt_view.drawGrid('lightgray',0,0,gridx,gridy);
                                                jist_gantt_view.drawGrid('lightgray',gridx*20,gridy*2.5,gridx/2,gridy/2);
                                                //jist_gantt_view.drawRect(x,y,width,height);
                                                //Do Headers
                                                jist_gantt_view.context.font = '20pt Helvetica';
                                                jist_gantt_view.drawText('Labour Schedule Site:'+' ' +jsondata[0].site,startx-gridx*4,starty,gridy*20,'start','bottom');
                                                jist_gantt_view.context.font = '10pt Helvetica';
                                                jist_gantt_view.drawText('Description:'+' ' +jsondata[0].description,gridx*2.,starty,gridy*20,'start','bottom');
                                                jist_gantt_view.drawText('From:'+' '+jsondata[0].allplanstart,gridx*3,starty,gridy*4,'start','bottom');
                                                jist_gantt_view.drawText('To:'+' '+jsondata[0].allplanend,gridx*3,starty*4,gridy*4,'start','bottom');
                                                jist_gantt_view.drawText('JCNo',startx-gridx,starty,gridy*2,'start','bottom');
                                                jist_gantt_view.drawText('Team Name',startx-gridx,starty*3,gridy*5,'start','bottom');
                                                jist_gantt_view.drawText('Tasks',startx-gridx,starty*6,gridy*5,'start','bottom');
                                                jist_gantt_view.drawText('To Start',startx-gridx,starty*15,gridy*2,'start','bottom');
                                                jist_gantt_view.drawText('To End',startx-gridx,starty*17,gridy*2,'start','bottom');
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
                                                    jist_gantt_view.drawText(jsondata[i].teamname,startx,starty*3,gridy*5,'start','bottom');
                                                    jist_gantt_view.drawText(jsondata[i].taskname,startx,starty*6,gridy*5,'start','bottom');
                                                    jist_gantt_view.drawText(jsondata[i].planstart,startx,starty*15,gridy*2,'start','bottom');
                                                    jist_gantt_view.drawText(jsondata[i].planend,startx,starty*17,gridy*2,'start','bottom');
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
                                                $("#jist_contract_gantt_div").css('width','98%');
                                            });
                                        });
                                            return false;
                                });

                            });
                            return false;
                        });
                        return false;
                    });
                    return false;
                });
            };
            if (ui.panel.id=='ui-tabs-Teams_Schedule'){
                //console.log("Made it");
                var thisdate = $("#schedule_view_date").val();
                $("#div_day_date_schedule").empty();
                $("#div_day_date_nonschedule").empty();
                $("#div_day_date_schedule").load("/labourcont/export_schedule_labour_list_scheduled_by_date?thisdate="+thisdate,function(responseTxt,statusTxt,xhr){
                 });
                $("#div_day_date_nonschedule").load("/labourcont/export_schedule_labour_list_nonscheduled_by_date?thisdate="+thisdate,function(responseTxt,statusTxt,xhr){
                    $(".div_leader_accord_team_pic").css('width','50px');
                    $(".div_leader_accord_team_pic").css('height','50px');
                 });
            };
        },
       load: function(event,ui){
            console.log("Made it to tabs load event ");
        },
        //disabled: [2,4]
    });
    $( "#contact_employees_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#active_labour_tbl").delegate('tr','mouseover mouseleave click',function(e) {
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
        },
       select: function(event,ui){
            if (ui.panel.id=='ui-tabs-1'){
                $("#this_div").empty();
            };
            if (ui.panel.id=='ui-tabs-ContactDetails'){
                $("#button_search_name_staff").button();
                $("#button_search_name_labour").button();
                $("#button_search_name_subcon").button();
                $("#div_contact_details").empty();
                $("#div_contact_details").load("/labourcont/get_contact_details_by_division_people_html",function(responseTxt,statusTxt,xhr){
                    var icons = {
                          header: "ui-icon-circle-arrow-e",
                          activeHeader: "ui-icon-circle-arrow-s"
                        };
                    $("#labour_divisions_people_accordion" ) .accordion({
                        header: "h3",
                        heightStyle: 'content', 
                        icons: icons,
                        active: 'false',
                        collapsible:'true',
                      }).sortable({
                        axis: "y",
                        handle: "h3",
                        stop: function( event, ui ) {
                          // IE doesn't register the blur when sorting
                          // so trigger focusout handlers to remove .ui-state-focus
                          ui.item.children( "h3" ).triggerHandler( "focusout" );
                        }
                      })
                    $(".div_staff_pic").click(function(){
                        staffid = $(this).attr('data-jist-userid');
                        groupid = $(this).attr('data-jist-labourgroup');
                        $("#div_contact_data").load("/labourcont/get_contact_data_by_person_id?staffid="+staffid+"&groupid="+groupid,function(responseTxt,statusTxt,xhr){
                            $("#staffid").prop('disabled',true);
                            $("#button_edit_contact").button();
                            $("#button_edit_save_contact").button();
                            $("#button_edit_save_contact").hide();
                            $("#button_edit_contact").click(function(){
                                $(this).hide();
                                $("#button_edit_save_contact").show();
                            });
                            $("#button_edit_save_contact").click(function(){
                                $("#staffid").prop('disabled',false);
                                var formserial = $("#employee_contact_data_frm").serialize();
                                var jqxhr = $.post("/labourcont/save_contact_data_by_person_id?"+formserial, function(data) {
                                    $("#button_edit_save_contact").hide();
                                    $("#button_edit_contact").show();
                                    return false;
                                });
                                return false;
                            });

                        });
                    });
                    $(".div_lab_pic").click(function(){
                        staffid = $(this).attr('data-jist-userid');
                        groupid = $(this).attr('data-jist-labourgroup');
                        $("#div_contact_data").load("/labourcont/get_contact_data_by_person_id?staffid="+staffid+"&groupid="+groupid,function(responseTxt,statusTxt,xhr){
                            $("#staffid").prop('disabled',true);
                            $("#button_edit_contact").button();
                            $("#button_edit_save_contact").button();
                            $("#button_edit_save_contact").hide();
                            $("#button_edit_contact").click(function(){
                                $(this).hide();
                                $("#button_edit_save_contact").show();
                            });
                            $("#button_edit_save_contact").click(function(){
                                $("#staffid").prop('disabled',false);
                                var formserial = $("#employee_contact_data_frm").serialize();
                                var jqxhr = $.post("/labourcont/save_contact_data_by_person_id?"+formserial, function(data) {
                                    $("#button_edit_save_contact").hide();
                                    $("#button_edit_contact").show();
                                    return false;
                                });
                                return false;
                            });

                        });
                    });
                    $(".div_subcon_pic").click(function(){
                        staffid = $(this).attr('data-jist-userid');
                        groupid = $(this).attr('data-jist-labourgroup');
                        $("#div_contact_data").load("/labourcont/get_contact_data_by_person_id?staffid="+staffid+"&groupid="+groupid,function(responseTxt,statusTxt,xhr){
                            $("#staffid").prop('disabled',true);
                            $("#button_edit_contact").button();
                            $("#button_edit_save_contact").button();
                            $("#button_edit_save_contact").hide();
                            $("#button_edit_contact").click(function(){
                                $(this).hide();
                                $("#button_edit_save_contact").show();
                            });
                            $("#button_edit_save_contact").click(function(){
                                $("#staffid").prop('disabled',false);
                                var formserial = $("#employee_contact_data_frm").serialize();
                                var jqxhr = $.post("/labourcont/save_contact_data_by_person_id?"+formserial, function(data) {
                                    $("#button_edit_save_contact").hide();
                                    $("#button_edit_contact").show();
                                    return false;
                                });
                                return false;
                            });

                        });
                    });

                });


            };
        },
        //disabled: [2,4]
    });

    $("#button_view_active_labour").click(function(event) {
        $("#div_employee_list").load("/labourcont/export_labour_list_active_html",function(responseTxt,statusTxt,xhr){
            //callback_load_labour_table();
                    $("#tbl_labourlist").delegate('tr','mouseover mouseleave click',function(e) {
                        //e.preventDefault();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var values = '';
                            var tds = $(this).find('td');
                            var userid = $(this).find("td").eq(0).html();
                            var jqxhr = $.get("/labourcont/get_dialog_add_labourpic?userid="+userid, function(data) {
                                    $("#div_dialog_pic_place" ).html( data );
                                    $("#userid").prop('disabled',true);
                                    $("#triggerUpload").button();
                                    $( "#dialog_labour_pic" ).dialog({
                                        autoOpen: false,
                                        height: 380,
                                        width: 550,
                                        modal: true,
                                        buttons: {
                                            "Save": function() {
                                                var bValid = true;
                                                if ( bValid ) {
                                                    $("#button_view_active_labour").trigger('click'); 
                                                    $( this ).dialog( "close" );
                                                }
                                            },
                                            Cancel: function() {
                                                        $( this ).dialog( "close" );
                                                    }
                                        },
                                        close: function() {
                                                    $( this ).find('input').val('');
                                                    $(this).remove();
                                               }
                                    });
                                    var jqueryuploader = $('#jquery-fine-uploader').fineUploader({
                                        request: {
                                                     endpoint: '/labourcont/save_dialog_labourpic'
                                                 },
                                        autoUpload: false,
                                        validation: {
                                            allowedExtensions: ['png'],
                                        sizeLimit: 1048576, // 5M = 5 * 1024 * 1024 bytes
                                        //sizeLimit: 51200, // 50 kB = 50 * 1024 bytes
                                        itemLimit: 1,
                                        },
                                        text: {
                                                  uploadButton: 'Click To Upload Labour Photo - 200x200.png'
                                              },
                                        editFilename:  true,
                                    }).on('submit',function(event,id,name){
                                        $(this).fineUploader('setParams',{
                                           userid : $("#userid").val(),
                                        });
                                    }).on('complete',function(event,id,name,response){
                                        //console.log(response); 
                                    });
                                    $('#triggerUpload').click(function() {
                                        $("#userid").prop('disable',false);
                                        jqueryuploader.fineUploader('uploadStoredFiles');
                                        var formserial = $("#dialog_labour_pic").serialize();
                                        return false;
                                    });
                                    $('#triggerClose').click(function() {
                                        close();
                                        return false;
                                    });
                                    $('#triggerReset').click(function() {
                                        jqueryuploader.fineUploader('reset');
                                        //$("#fileupload_tabs").tabs( "refresh" );
                                        clear_form_elements($("#dialog_labour_pic"));
                                        return false;
                                    });
                                    $("#dialog_labour_pic").dialog("open");
                                    //document.getElementById('picname').addEventListener('change', handleSimpleSelect, false);
                                
                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
        });
    });
    function handleSimpleSelect(evt) {
        var files = evt.target.files;
        var file = files[0]
        var img = document.createElement("img");
        img.classList.add("obj");
        img.file = file;
        document.getElementById('dialog_labour_pic_frm').insertBefore(img, null);

        var reader = new FileReader();
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
        reader.readAsDataURL(file);
    };
    function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object
    // Loop through the FileList and render image files as thumbnails.
        for (var i = 0, f; f = files[i]; i++) {

          // Only process image files.
          if (!f.type.match('image.*')) {
            continue;
          }

          var reader = new FileReader();

          // Closure to capture the file information.
          reader.onload = (function(theFile) {
            return function(e) {
              // Render thumbnail.
              var span = document.createElement('span');
              span.innerHTML = ['<img class="thumb" src="', e.target.result,
                                '" title="', escape(theFile.name), '"/>'].join('');
              document.getElementById('dialog_labour_pic_frm').insertBefore(span, null);
              var canvas = document.getElementById('canvas_labpic');
              var context = canvas.getContext("2d"); 
              //context.drawImage(f,0,0);
              context.beginPath();
              context.moveTo(100, 150);
              context.lineTo(450, 50);
              context.stroke();
            };
          })(f);

          // Read in the image file as a data URL.
          reader.readAsDataURL(f);
        }
    }
    function callback_load_new_team_app(){
        $("#div_categories_people_accordion").load("/labourcont/get_labour_categories_people_for_teams_html",function(responseTxt,statusTxt,xhr){
            var icons = {
                  header: "ui-icon-circle-arrow-e",
                  activeHeader: "ui-icon-circle-arrow-s"
                };
            $("#labour_categories_people_accordion" ) .accordion({
                header: "h3",
                heightStyle: 'content', 
                icons: icons,
                collapsible:'true',
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
        });
        $("#div_teams_choice_box").load("/labourcont/get_labour_teams_choice_box",function(responseTxt,statusTxt,xhr){
            $("#button_create_new_team").button();
            $("#button_team_reset").button();
            $("#button_create_new_team").prop('disabled',false);
            $("#edit_labour_teams").change(function() {
                var teamid = $(this).val();
                $("#div_current_team").load("/labourcont/get_edit_labour_current_team?teamid="+teamid,function(responseTxt,statusTxt,xhr){
                      $("#div_current_team").css('display','block');
                      $("<button id='button_edit_team' class='ui-widget ui-widget-content ui-state-default'>Edit Team</button>").appendTo("#div_current_team");
                      $("#button_edit_team").button();
                      $("#edit_team_id").prop('disabled',true);
                      $("#div_current_team").find('img').each(function(e,htmlelement){
                          console.log($(this));
                          $(this).addClass("lab_team_pic");
                      });
                      $(".div_lab_mem_pic").dblclick(function(event,ui) {
                          var thisdata = $(this).data();
                          $(this).addClass("lab_team_pic");
                          $(this).parent().parent().clone().appendTo("#div_current_team");
                          $(this).parent().parent().remove();
                           $(".lab_team_pic").dblclick(function(){
                              $(this).parent().parent().remove();
                           }); 
                      });
                      $(".div_staff_mem_pic").dblclick(function(event,ui) {
                          var thisdata = $(this).data();
                          $(this).addClass("lab_team_pic");
                          $(this).parent().parent().clone().appendTo("#div_current_team");
                          $(this).parent().parent().remove();
                           $(".lab_team_pic").dblclick(function(){
                              $(this).parent().parent().remove();
                           }); 
                      });
                      $(".div_subcon_mem_pic").dblclick(function(event,ui) {
                          var thisdata = $(this).data();
                          $(this).addClass("lab_team_pic");
                          $(this).parent().parent().clone().appendTo("#div_current_team");
                          $(this).parent().parent().remove();
                      });
                      $("#button_edit_team").click(function(event,ui) {
                            if ($("#edit_team_name").val() == '' ){
                                $("#warningdiv").html("Add a Name for the team.")
                                    $("#warningdiv").fadeIn(2000,function(){
                                        $("#warningdiv").fadeOut('slow')    
                                    });return false;
                            };
                            $("#edit_team_id").prop('disabled',false);
                            var teamname = $("#edit_team_name").val()
                            var teamid = $("#edit_team_id").val()
                            var teamdescription = $("#edit_team_description").val()
                            var teamfleetid = $("#edit_team_vehicle_id").val()
                            var datalist = new Array();
                            $("#div_current_team").find('img').each(function(e,htmlelement){
                                var thisdata=$(this).data();
                                 datalist.push(thisdata)
                            });
                            var jqxhr = $.post("/labourcont/saveeditlabour_team?teamdata="+
                                JSON.stringify(datalist)+'&teamname='+alltrim(teamname)+'&teamid='+alltrim(teamid)+'&teamfleetid='+alltrim(teamfleetid)+'&teamdescription='+alltrim(teamdescription), function(data) {
                                $("#div_current_team").empty();
                                $("#div_current_team").hide();
                                $("#button_create_new_team").prop('disabled',false);
                                window.location.reload();
                            });
                      });
                       $(".lab_team_pic").dblclick(function(){
                          var thisdata=$(this).data();
                          var jqxhr = $.post("/labourcont/delete_labour_from_team?teamdata="+ JSON.stringify(thisdata), function(data) {
                          });
                          $(this).parent().parent().remove();

                       }); 
                  
                });


            });
            $("#button_create_new_team").click(function() {
              $("#div_current_team").css('display','block');
              $("#div_current_team").empty();
              $("#button_create_new_team").prop('disabled',true);
              $("<label for='team_name'>Add a Team Name(Required)</label>").appendTo("#div_current_team");
              $("<input id='team_name'></input>").appendTo("#div_current_team");
              $("<h6>1. Add a name for the new team.</h6>").appendTo("#div_current_team");
              $("<h6>2. Double Click on the faces on the left to add to the team.</h6>").appendTo("#div_current_team");
              $("<h6>3. The First Person Added is the Team Leader.</h6>").appendTo("#div_current_team");
              $("<h6>4. Double Click on  the face on the right to remove from the list if added in error.</h6>").appendTo("#div_current_team");
              $("<h6>5. Click on 'Add New Team' to save team.</h6>").appendTo("#div_current_team");
              $("<button id='button_add_new_team' class='ui-widget ui-widget-content ui-state-default'>Add New Team</button>").appendTo("#div_current_team");
              $("#button_add_new_team").button();
              $(".div_lab_mem_pic").dblclick(function(event,ui) {
                  var thisdata = $(this).data();
                  $(this).addClass("lab_team_pic");
                  $(this).parent().parent().clone().appendTo("#div_current_team");
                  $(this).parent().parent().remove();
                   $(".lab_team_pic").dblclick(function(){
                      $(this).parent().parent().remove();
                   }); 
              });
              $(".div_staff_mem_pic").dblclick(function(event,ui) {
                  var thisdata = $(this).data();
                  $(this).addClass("lab_team_pic");
                  $(this).parent().parent().clone().appendTo("#div_current_team");
                  $(this).parent().parent().remove();
                   $(".lab_team_pic").dblclick(function(){
                      $(this).parent().parent().remove();
                   }); 
              });
              $(".div_subcon_mem_pic").dblclick(function(event,ui) {
                  var thisdata = $(this).data();
                  $(this).addClass("lab_team_pic");
                  $(this).parent().parent().clone().appendTo("#div_current_team");
                  $(this).parent().parent().remove();
                   $(".lab_team_pic").dblclick(function(){
                      $(this).parent().parent().remove();
                   }); 
              });
              $("#button_add_new_team").click(function(event,ui) {
                    if ($("#team_name").val() == '' ){
                        $("#warningdiv").html("Add a Name for the team.")
                            $("#warningdiv").fadeIn(2000,function(){
                                $("#warningdiv").fadeOut('slow')    
                            });return false;
                    };
                    var teamname = $("#team_name").val()
                    var datalist = new Array();
                    $("#div_current_team").find('img').each(function(e,htmlelement){
                        var thisdata=$(this).data();
                         datalist.push(thisdata)
                    });
                    var jqxhr = $.post("/labourcont/savenewlabour_team?teamdata="+ JSON.stringify(datalist)+'&teamname='+teamname, function(data) {
                        $("#div_current_team").empty();
                        $("#div_current_team").hide();
                        $("#button_create_new_team").prop('disabled',false);
                        window.location.reload();
                    });
              });
            });
        });
    };
    function getOriginalElementData(domElementJQueryObject){
        var originalElementData = new Array();
        $.each(domElementJQueryObject.data(),function(name,value) {
           originalElementData.push({"name":name,"value":value});
        });
        return originalElementData;
    };
    $("#button_team_view_active_labour").click(function(event) {
        $("#div_staff_list").load("/labourcont/export_labour_list_active_html",function(responseTxt,statusTxt,xhr){
            //callback_load_labour_table();
        });
    });
    $("#button_search_labour_idno").click(function(event) {
        var formserial = $("#search_employee_id").val();
        $("#div_employee_list").load("/labourcont/search_labour_by_idno?"+alltrim(formserial),function(responseTxt,statusTxt,xhr){
            callback_load_labour_table();
        });
    });
    $("#button_search_employee_first_name").click(function(event) {
        var formserial = $("#search_employee_first_name").val();
        $("#div_employee_list").load("/labourcont/search_labour_by_first_name?"+alltrim(formserial),function(responseTxt,statusTxt,xhr){
            callback_load_labour_table();
        });
    });
    $("#button_search_employee_last_name").click(function(event) {
        var formserial = $("#search_employee_last_name").val();
        $("#div_employee_list").load("/labourcont/search_labour_by_last_name?"+alltrim(formserial),function(responseTxt,statusTxt,xhr){
            callback_load_labour_table();
        });
    });
    $("#button_employee_new").click(function(event) {
                $( "#new_employee_div" ).load("/labourcont/get_new_labour_form",function(responseTxt,statusTxt,xhr){
                    $("#new_employee_date_started").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                    $("#button_save_employee_new").button();
                    $("#button_save_employee_new").click(function(event) {
                        var formserial = $("#new_employee_form").serialize();
                        var firstname = $("#new_employee_first_name").val();
                        var jqxhr = $.post("/labourcont/savenewlabour?"+formserial, function(data) {
                             $("#search_employee_first_name").val(firstname);       
                             $("#new_employee_form").empty();       
                            $( "#labour_employees_tabs" ).tabs("option","active", 1 );
                             $("#button_search_employee_first_name").trigger("click");       
                        });
                        return false;

                    });
                    $( "#labour_employees_tabs" ).tabs("option","active", 2 );
                });
        return false;

    });
    function callback_load_labour_table(){
        $("#active_labour_tbl").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                $( "#edit_employee_div" ).load("/labourcont/get_labour_by_edit_id/"+alltrim(col0text),function(responseTxt,statusTxt,xhr){
                    var dateval = $("#edit_employee_date_started").val();
                    $("#edit_employee_date_started").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate", dateval);
                    $("#button_employee_edit").button();
                    $("#button_employee_edit").click(function(event) {
                        var formserial = $("#edit_employee_form").serialize();
                        var firstname = $("#edit_employee_first_name").val();
                        var jqxhr = $.post("/labourcont/saveeditlabour?"+formserial, function(data) {
                             $("#search_employee_first_name").val(firstname);       
                             $("#edit_employee_form").empty();       
                            $( "#labour_employees_tabs" ).tabs("option","active", 1 );
                             $("#button_search_employee_first_name").trigger("click");       
                        });
                        return false;
                    });
                });
                $( "#employee_payment_history_div" ).load("/labourcont/get_labour_history_by_id/"+alltrim(col0text),function(responseTxt,statusTxt,xhr){
                    console.log("Got here");    
                    return false;
                });

                $( "#labour_employees_tabs" ).tabs("option","active", 2 );
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#active_labour_tbl").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
            };
        });
    };
    $("#button_view_active_labour").button();
    $("#button_search_labour_idno").button();
    $("#button_search_employee_first_name").button();
    $("#button_search_employee_last_name").button();
    $("#button_employee_new").button();
    $( "#labour_employees_tabs" ).tabs("option","active", 1 );
    $( "#contact_employees_tabs" ).tabs("option","active", 1 );
    $( "#labour_teams_tabs" ).tabs("option","active", 4 );
    $( "#labour_teams_schedule_tabs" ).tabs("option","active", 1 );
    var thisdate = new Date();
    $("#schedule_view_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" ).datepicker().datepicker("setDate",thisdate );
    $("#schedule_view_date").change(function(){
        var selected = $("#labour_teams_schedule_tabs").tabs('option', 'selected');
        $("#labour_teams_schedule_tabs").tabs('select', selected-1);
        $("#labour_teams_schedule_tabs").tabs('select', selected);
    });
    function replaceforward2back(dataStr) {
        //console.log(dataStr.replace(/\//g, "-"));
        return dataStr.replace(/\//g, "-");
    };
    function alltrim(str) {
        return str.replace(/^\s+|\s+$/g, '');
    };
});
$(document).ready(function(){

});

