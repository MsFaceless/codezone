//Handels the buying and grv pages
//Dec 2012-12-31
$(function(){
    $("#req-new-form-buttons").hide();
    $("#req-holding-items-form").hide();
    $("#add-req-done").hide();
    $("#add-req-done-cancel").hide();
    $("#grv_console_tabs" ).tabs({ heightStyle: "fill" });
    $("#buying_linking_tabs" ).tabs({ 
        heightStyle: "fill",
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
       select: function(event,ui){
            if (ui.panel.id=='ui_tabs_Rentals'){
                $("#link_all_suppliers_rentals_div").load("/logisticscont/get_suppliers_minus_rentals_active_html",function(data){
                    $("#tbl_active_suppliers_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var fleet_id = alltrim(col0text); 
                            var selectedtab = $("#buying_linking_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/logisticscont/link_buying_to_rentals/"+fleet_id, function(data) {
                                $("#buying_linking_tabs").tabs('select', selectedtab-1);
                                $("#buying_linking_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
                $("#link_all_rentals_div").load("/logisticscont/get_rentals_resources_active_html",function(data){
                    $("#tbl_active_rentals_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var rentals_id = alltrim(col0text); 
                            var selectedtab = $("#buying_linking_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/logisticscont/delink_supplier_from_rentals/"+rentals_id, function(data) {
                                $("#buying_linking_tabs").tabs('select', selectedtab-1);
                                $("#buying_linking_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
            };
            if (ui.panel.id=='ui_tabs_Maintenance'){
                $("#link_all_suppliers_maintenance_div").empty()
                $("#link_all_suppliers_maintenance_div").load("/logisticscont/get_suppliers_minus_maintenance_active_html",function(data){
                    $("#tbl_active_suppliers_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var fleet_id = alltrim(col0text); 
                            var selectedtab = $("#buying_linking_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/logisticscont/link_buying_to_maintenance/"+fleet_id, function(data) {
                                $("#buying_linking_tabs").tabs('select', selectedtab-1);
                                $("#buying_linking_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
                $("#link_all_maintenance_div").empty();
                $("#link_all_maintenance_div").load("/logisticscont/get_maintenance_resources_active_html",function(data){
                    $("#tbl_active_maintenance_resources").delegate('tr','mouseover mouseleave click',function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (e.type == 'mouseover') {
                            $(this).addClass("hover");
                        } else if ( e.type == 'click' ) {
                            var col0text = $(this).find("td").eq(0).html();
                            var maintenance_id = alltrim(col0text); 
                            var selectedtab = $("#buying_linking_tabs").tabs('option', 'selected');
                            var jqxhr = $.post("/logisticscont/delink_supplier_from_maintenance/"+maintenance_id, function(data) {
                                $("#buying_linking_tabs").tabs('select', selectedtab-1);
                                $("#buying_linking_tabs").tabs('select', selectedtab);

                            });

                        }else   {
                            $(this).removeClass("hover");
                        }
                    });
                    return false;
                });
            };
            if (ui.panel.id=='ui-tabs-2'){
                $("#purchase_req_trolley_active_div").empty();
            };
            if (ui.panel.id=='ui-tabs-3'){
                $("#purchase_req_trolley_approval_div").empty();
            };
        }
    });
    $("#rental_console_tabs" ).tabs({ 
        heightStyle: "fill",
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
       select: function(event,ui){
            if (ui.panel.id=='tabs_rental_index'){
            };
            if (ui.panel.id=='ui-tabs-3'){
                $("#purchase_req_trolley_approval_div").empty();
            };
        },
        load: function( event, ui ) {
            $("#tbl_active_rentals_resources").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var thisid = alltrim(col0text); 
                    $("#ui_tabs_Last100POs").load( "/logisticscont/purchase_orders_for_supplier_tracked/"+ thisid, function(data) {
                        $("#tbl_supplier_last_100_pos").delegate('tr','mouseover mouseleave click',function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            if (e.type == 'mouseover') {
                                $(this).addClass("hover");
                            } else if ( e.type == 'click' ) {
                                var values = '';
                                var tds = $(this).find('td');
                                var col0text = $(this).find("td").eq(0).html();
                                var thisid = alltrim(col0text); 

                                $( "#rental_console_tabs" ).tabs("option","active", 2 );
                            }else   {
                                $(this).removeClass("hover");
                            }
                        });
                        $( "#rental_console_tabs" ).tabs("option","active", 1 );
                        return false;
                    });

                }else   {
                    $(this).removeClass("hover");
                }
            });
            return false;
       }
    });
    $( "#buying_console_tabs" ).tabs({ 
        heightStyle: "fill",
        beforeLoad: function( event, ui ) {
            ui.jqXHR.error(function() {
                ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
            });
        },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            $("#open_po_orders_table").delegate('tr','mouseover mouseleave click',function(e) {
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
                    $("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,4);
                    $("#myjistconsole_tabs").tabs('select', 4);
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#purchase_req_contract_all_table").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                //e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#purchase_req_contract_all_table").delegate('td','click',function(e){
                if ($(this).parent().index() != 0){ 
                    if ($(this).index() == 9){ 
                        //console.log("delete pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var jqxhr = $.post("/logisticscont/ajaxDeactivateBuyingSideReq/"+uniqid+"/"+col0text, function(data) {
                            var activejcno = $("#activesiteid").val();
                        });
                        $(this).parent().remove();

                    };
                    if ($(this).index() == 12){ 
                        //console.log("add trolley pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_add_to_trolley/"+uniqid+"/"+alltrim(col0text), function(data) {
                            //var activejcno = $("#activesiteid").val();
                            //console.log("CAll Back from add trolley");
                            var selectedtab = $("#buying_console_tabs").tabs('option', 'selected');
                            $("#buying_console_tabs").tabs("load",selectedtab);
                        });
                    };
                    if ($(this).index() == 14){ 
                        //console.log("notes pressed");
                        var reqitemid = $(this).parent().find("td").eq(0).html();
                        var uniqid = Math.random();
                        $("#activereqitemid_buying").val(reqitemid);
                        $( "#dialog_purchasereq_notes_buying" ).dialog("open");
                        $( "#purchasereq_notes_all_buying" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+reqitemid);
                    };
                };return false;
            });
            $("#supplier_open_po_orders_table").delegate('tr','mouseover mouseleave click',function(e) {
                if (e.type == 'mouseover') {
                    $(this).addclass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                    $("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"req id"+col2text,4);
                    $("#myjistconsole_tabs").tabs('select', 4);
                }else   {
                    $(this).removeclass("hover");
                }
            });
            $("#purchase_req_trolley_all_table").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                //e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#purchase_req_trolley_all_table").delegate('td','click',function(e){
                if ($(this).parent().index() != 0){ 
                    if ($(this).index() == 119){ 
                        //console.log("delete pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var jqxhr = $.post("/logisticscont/ajaxDeactivateBuyingSideReq/"+uniqid+"/"+col0text, function(data) {
                            var activejcno = $("#activesiteid").val();
                        });
                        $(this).parent().remove();
                    };
                    if ($(this).index() == 9){ 
                        //console.log("notes pressed");
                        var reqitemid = $(this).parent().find("td").eq(1).html();
                        var uniqid = Math.random();
                        $("#activereqitemid_buying").val(reqitemid);
                        $( "#dialog_purchasereq_notes_buying" ).dialog("open");
                        $( "#purchasereq_notes_all_buying" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+alltrim(reqitemid));
                    };
                    if ($(this).index() == 10){ 
                        //console.log("prices pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var col1text = $(this).parent().find("td").eq(1).html();
                        var col4text = $(this).parent().find("td").eq(4).html();
                        var col5text = $(this).parent().find("td").eq(5).html();
                        var col6text = $(this).parent().find("td").eq(6).html();
                        var col7text = $(this).parent().find("td").eq(7).html();
                        //console.log(col0text)
                        $( "#active_shopping_req_prices_list" ).load("/logisticscont/ajaxpurchase_reqs_get_quotation_prices/"+uniqid+"/"+alltrim(col0text),function(){
                            $("#supp_shopping_quote_form").css("float","right");
                            $("#supp_shopping_quote_form").css("margin-right","100px");
                            $( "#supp_name_shopping" ).css("width","300px");
                            $( "#supp_description_shopping" ).css("width","400px");
                            $( "#supp_description_shopping" ).val(col4text);
                            $( "#supp_unit_shopping" ).val(col5text);
                            $( "#supp_quantity_shopping" ).val(col6text);
                            $( "#supp_name_shopping" ).focus();
                            $( "#supp_quantity_shopping" ).css("text-align","right");
                            $( "#supp_price_shopping" ).css("text-align","right");
                            $( "#supp_total_shopping" ).css("text-align","right");
                            $( "#supp_price_shopping" ).change(function(e){
                                if (col6text && $(this).val()){
                                    var supp_total = parseFloat(col6text)*parseFloat($(this).val());
                                    //console.log(supp_total);
                                    $( "#supp_total_shopping" ).val(supp_total.toFixed(2));
                                };

                            });
                            //$( "#supp_shopping_quote_form" ).hide();
                            $("#supp_shopping_price_submit_button").on('click',function(e){
                                //console.log("Clicked");
                                //console.log(col0text);
                                $("#shoppinglist_id").val(col1text);
                                e.preventDefault();
                                var formserial = $("#supp_shopping_quote_form").serialize();
                                //console.log(formserial);
                                var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_add_new_quote_price/"+uniqid+"/"+col0text+"?"+formserial, function(data) {
                                    $( "#active_shopping_req_prices_list" ).load("/logisticscont/ajaxpurchase_reqs_get_quotation_prices/"+uniqid+"/"+alltrim(col0text),function(data){
                                        $("#supp_shopping_quote_form").hide();
                                    });
                                });

                                //thissupplier = $( "#search_supplier_name" ).val();
                                //$("#outputsupplier_search").load("/logisticscont/do_search_supplier/"+thissupplier)
                                //$("#dialog_newbudget").dialog("open");
                            });
                        });
                    };
                };return false;
            });
            $("#purchase_req_trolley_all_table").delegate('td','mouseleave mouseover',function(e){
                if ($(this).parent().index() != 0){ 
                    if ($(this).index() == 100){ 
                        //console.log("notes pressed");
                        var reqitemid = $(this).parent().find("td").eq(1).html();
                        var uniqid = Math.random();
                        $("#activereqitemid_buying").val(reqitemid);
                        //$( "#dialog_purchasereq_notes_buying" ).dialog("open");
                        $( "#purchasereq_notes_all_buying" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+alltrim(reqitemid),function(){
                            var thisnote = $("#purchasereq_notes_all_buying").val();
                            //console.log(thisnote);
                            $("#toggle_item_add").attr("title",function(){
                                //$(document).tooltip();
                                //$("#toggle_item_add").tooltip({
                                //    track: true
                                //});
                                return thisnote
                            });
                            //$(document).tooltip({
                            //    track: true    
                            //});
                            $("#toggle_item_add").tooltip({
                                track: true
                            });
                        });

                    };
                };
            });
            $("#purchase_req_trolley_for_approval").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                //e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    var values = '';
                    var tds = $(this).find('td');
                    var col0text = $(this).find("td").eq(0).html();
                    var col1text = $(this).find("td").eq(1).html();
                    var col2text = $(this).find("td").eq(2).html();
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#purchase_req_trolley_for_approval").delegate('td','click',function(e){
                if ($(this).parent().index() != 0){ 
                    if ($(this).index() == 19){ 
                        //console.log("delete pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        //console.log(col0text)
                        var jqxhr = $.post("/logisticscont/ajaxDeactivateBuyingSideReq/"+uniqid+"/"+col0text, function(data) {
                            var activejcno = $("#activesiteid").val();
                        });
                        $(this).parent().remove();
                    };
                    if ($(this).index() == 10){ 
                        //console.log("notes pressed on approval");
                        var reqitemid = $(this).parent().find("td").eq(1).html();
                        var uniqid = Math.random();
                        $("#activereqitemid_buying").val(reqitemid);
                        $( "#dialog_purchasereq_notes_buying" ).dialog("open");
                        $( "#purchasereq_notes_all_buying" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+alltrim(reqitemid));
                    };
                    if ($(this).index() == 11){ 
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var col1text = $(this).parent().find("td").eq(1).html();
                        var col2text = $(this).parent().find("td").eq(2).html();
                        var col5text = $(this).parent().find("td").eq(5).html();
                        var col6text = $(this).parent().find("td").eq(6).html();
                        $("#purchase_approve_panel").hide();
                        $("#active_shopping_req_prices_budget").show()
                            $("#active_shopping_req_prices_list_approval").show()
                            $( "#active_shopping_req_prices_budget" ).load("/mngntcont/ajaxgetbudget_byreq_id/"+alltrim(col2text)+"/"+alltrim(col1text));
                        $( "#active_shopping_req_prices_list_approval" ).load("/logisticscont/ajaxpurchase_reqs_get_quotation_prices_only/"+uniqid+"/"+alltrim(col0text),function(){
                            //$(this).empty();
                            $("#purchase_req_quotation_suppliers_approval").delegate('tr','mouseover mouseleave click',function(e) {
                                e.preventDefault();
                                //e.stopPropagation();
                                if (e.type == 'mouseover') {
                                    $(this).addClass("hover");
                                } else if ( e.type == 'click' ) {
                                    //var values = '';
                                    //var tds = $(this).find('td');
                                }else   {
                                    $(this).removeClass("hover");
                                };
                            });
                            $("#purchase_req_quotation_suppliers_approval").delegate('td','click',function(e){
                                if ($(this).parent().index() != 0){ 
                                    if ($(this).index() == 10){ 
                                        //console.log("delete pressed");
                                        var uniqid = Math.random()
                                var priceid = $(this).parent().find("td").eq(0).html();
                            $("#active_shopping_req_approval_compare").
                                load("/logisticscont/ajaxpurchase_reqs_do_price_comparison_budget/"+uniqid+"/"+alltrim(col0text)+"/"+alltrim(col1text)+"/"+alltrim(priceid), function(data) {
                                    //  var activejcno = $("#activesiteid").val();
                                    $("#active_shopping_req_prices_budget").hide()
                                    $("#active_shopping_req_prices_list_approval").hide()
                                    $( "#appr_name_shopping" ).css("width","300px");
                                $( "#appr_description_shopping" ).css("width","400px");
                                $( "#appr_description_shopping" ).val(col5text);
                                $( "#appr_unit_shopping" ).val(col6text);
                                $( "#appr_name_shopping" ).focus();
                                $( "#appr_quantity_shopping" ).css("text-align","right");
                                $( "#appr_price_shopping" ).css("text-align","right");
                                $( "#appr_total_shopping" ).css("text-align","right");
                                $( "#appr_budget_total_shopping" ).css("text-align","right");
                                $( "#appr_purchases_total_shopping" ).css("text-align","right");
                                $("#appr_shopping_price_submit_button").on('click',function(e){
                                    //console.log("Clicked");
                                    //console.log(col0text);
                                    //$("#shoppinglist_id").val(col1text);
                                    e.preventDefault();
                                    //var formserial = $("#supp_shopping_quote_form").serialize();
                                    //console.log(formserial);
                                    var uniqid = Math.random();
                                    var jqxhr = $.post("/logisticscont/ajaxApproveReqQuotation/"+uniqid+"/"+alltrim(priceid), function(data) {
                                        $("#purchase_approve_panel").hide();
                                        $("#active_shopping_req_prices_budget").show()
                                        $("#active_shopping_req_prices_list_approval").show()
                                    });

                                });

                                })
                            //$(this).parent().remove();

                                    };
                                };
                            });

                            $( "#supp_name_shopping" ).css("width","300px");
                            $( "#supp_description_shopping" ).css("width","400px");
                            $( "#supp_description_shopping" ).val(col5text);
                            $( "#supp_unit_shopping" ).val(col6text);
                            $( "#supp_name_shopping" ).focus();
                            //$( "#supp_shopping_quote_form" ).hide();
                            $("#supp_shopping_price_submit_button").on('click',function(e){
                                //console.log("Clicked");
                                //console.log(col0text);
                                $("#shoppinglist_id").val(col0text);
                                e.preventDefault();
                                var formserial = $("#supp_shopping_quote_form").serialize();
                                //console.log(formserial);
                                var uniqid = Math.random();
                                var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_add_new_quote_price/"+uniqid+"/"+col1text+"?"+formserial, function(data) {
                                    $( "#active_shopping_req_prices_list" ).load("/logisticscont/ajaxpurchase_reqs_get_quotation_prices_only/"+uniqid+"/"+alltrim(col1text),function(){

                                    });
                                });

                            });
                        });
                    };
                    if ($(this).index() == 13){ 
                        //console.log("prices pressed on approval");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var col1text = $(this).parent().find("td").eq(1).html();
                        $(this).parent().remove();
                        var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_deactivate_trolley/"+alltrim(col1text), function(data) {
                            return false;
                        });

                    };

                };return false;
            });
            $("#purchase_reqs_approved_table").delegate('tr','mouseover mouseleave click',function(e) {
                e.preventDefault();
                //e.stopPropagation();
                if (e.type == 'mouseover') {
                    $(this).addClass("hover");
                } else if ( e.type == 'click' ) {
                    //var values = '';
                    //var tds = $(this).find('td');
                }else   {
                    $(this).removeClass("hover");
                }
            });
            $("#purchase_reqs_approved_table").delegate('td','click',function(e){
                if ($(this).parent().index() != 0){ 
                    if ($(this).index() == 12){ 
                        //console.log("delete pressed");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var col1text = $(this).parent().find("td").eq(1).html();
                        if ($("#activepoid_buying").val()){
                            var ponumber = $("#activepoid_buying").val();
                            $("#activepodisplay").html(ponumber);
                            $(this).parent().remove();
                            //console.log("col0text"+col0text);
                            //console.log("col1text"+col1text);
                            var jqxhr = $.post("/logisticscont/ajaxWriteOrderItemToPO/"+uniqid+"/"+alltrim(ponumber)+"/"+alltrim(col1text)+"/"+alltrim(col0text), function(data) {
                                var activesupplier = $("#activesupplierid_buying").val();
                                $("#ui_tabs_ThisOrder").load("/logisticscont/po_order_one_details/"+alltrim(ponumber), function(data) {
                                    $("#purchase_order_items_table").delegate('tr','mouseover mouseleave click',function(e) {
                                        e.preventDefault();
                                        //e.stopPropagation();
                                        if (e.type == 'mouseover') {
                                            $(this).addClass("hover");
                                            //console.log($(this).index());
                                        } else if ( e.type == 'click' ) {
                                            //var values = '';
                                            //var tds = $(this).find('td');
                                        }else   {
                                            $(this).removeClass("hover");
                                        }
                                    });

                                });                          
                            });
                        }else{
                            $("#warningdiv").html("Choose an existing order or create a New One!!!!");
                            $("#warningdiv").fadeIn(2000,function(){
                                $("#warningdiv").fadeOut('slow');    
                            });
                            return false;
                        };
                    };
                        //$(this).parent().remove();
                    if ($(this).index() == 13){ 
                        //console.log("Delete pressed on approval");
                        var uniqid = Math.random();
                        var col0text = $(this).parent().find("td").eq(0).html();
                        var col1text = $(this).parent().find("td").eq(1).html();
                        $(this).parent().remove();
                        var jqxhr = $.post("/logisticscont/ajaxUnapprovePrice/"+alltrim(col1text)+"/"+alltrim(col0text), function(data) {
                        });

                    };
                };return false;
            });
        },
       select: function(event,ui){
            if (ui.panel.id=='ui-tabs-1'){
                $("#purchase_req_contract_all_div").empty();
            };
            if (ui.panel.id=='ui-tabs-2'){
                $("#purchase_req_trolley_active_div").empty();
            };
            if (ui.panel.id=='ui-tabs-3'){
                $("#purchase_req_trolley_approval_div").empty();
            };
        },
        //disabled: [2,4]
    }),
        //*************comboboxes start*****************************
        //**********************************************************
        //(function( $ ) {
        $.widget( "ui.combobox_contracts_grv", {
            _create: function() {
                         var input,
        that = this,
        select = this.element.hide(),
        selected = select.children( ":selected" ),
        value = selected.val() ? selected.text() : "",
        wrapper = this.wrapper = $( "<span>" )
            .addclass( "ui-combobox" )
            .insertafter( select );

        function removeifinvalid(element) {
            var value = $( element ).val(),
        matcher = new regexp( "^" + $.ui.autocomplete.escaperegex( value ) + "$", "i" ),
        valid = false;
        select.children( "option" ).each(function() {
            if ( $( this ).text().match( matcher ) ) {
                this.selected = valid = true;
                return false;
            }
        });
        if ( !valid ) {
            // remove invalid value, as it didn't match anything
            $( element )
                .val( "" )
                .attr( "title", value + " didn't match any item" )
                .tooltip( "open" );
            select.val( "" );
            settimeout(function() {
                input.tooltip( "close" ).attr( "title", "" );
            }, 2500 );
            input.data( "autocomplete" ).term = "";
            return false;
        }
        }

        input = $( "<input>" )
            .appendto( wrapper )
            .val( value )
            .attr( "title", "" )
            .addclass( "ui-state-default ui-combobox-input" )
            .autocomplete({
                delay: 0,
            minlength: 0,
            height: 250,
            source: function( request, response ) {
                var matcher = new regexp( $.ui.autocomplete.escaperegex(request.term), "i" );
                response( select.children( "option" ).map(function() {
                    var text = $( this ).text();
                    if ( this.value && ( !request.term || matcher.test(text) ) )
                    return {
                        label: text.replace(
                                   new regexp(
                                       "(?![^&;]+;)(?!<[^<>]*)(" +
                                       $.ui.autocomplete.escaperegex(request.term) +
                                       ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                       ), "<strong>$1</strong>" ),
                            value: text,
                    option: this
                    };
                }) );
            },
            select: function( event, ui ) {
                        ui.item.option.selected = true;
                        that._trigger( "selected", event, {
                            item: ui.item.option
                        });
                        //loadpurchaseorderitemsperjcno(ui.item.option.value,"ui-tabs-purchasereqscontract");
                        //loadpurchaseorderitemsperjcno(ui.item.option.value,"req-new-form");
                        var active_supplierid = $( "#activesupplierid" ).val();
                        $("#ui-tabs-purchasereqscontract").load("/logisticscont/purchase_reqs_per_jcno/"+ui.item.option.value);
                        $("#req-new-form").load("/logisticscont/purchase_reqs_items_add_form/"+ui.item.option.value+"/"+active_supplierid,callback_load_req_jcno_budget);
                        $("#req-new-form-buttons").fadein(3500);
                        $("#req-holding-items-form").fadein(4500);
                        $("#activesiteid").val(ui.item.option.value);
                        $( "#purchase_req_new_tabs" ).tabs("option","active", 1 );
                        //ready_new_req()
                    },
            change: function( event, ui ) {
                        if ( !ui.item )
                            return removeifinvalid( this );
                    }
            })
        .addclass( "ui-widget ui-widget-content ui-corner-left" );

        input.data( "autocomplete" )._renderitem = function( ul, item ) {
            return $( "<li>" )
                .data( "item.autocomplete", item )
                .append( "<a>" + item.label + "</a>" )
                .appendto( ul );
        };

        $( "<a>" )
            .attr( "tabindex", -1 )
            .attr( "title", "show all contracts" )
            .tooltip()
            .appendto( wrapper )
            .button({
                icons: {
                           primary: "ui-icon-triangle-1-s"
                       },
                text: false
            })
        .removeclass( "ui-corner-all" )
            .addclass( "ui-corner-right ui-combobox-toggle" )
            .click(function() {
                // close if already visible
                if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                    input.autocomplete( "close" );
                    removeifinvalid( input );
                    return;
                }

                // work around a bug (likely same cause as #5265)
                $( this ).blur();

                // pass empty string as value to search for, displaying all results
                input.autocomplete( "search", "" );
                input.focus();
            });

        input
            .tooltip({
                position: {
                              of: this.button
                          },
                tooltipclass: "ui-state-highlight"
            });
                     },

            destroy: function() {
                         this.wrapper.remove();
                         this.element.show();
                         $.widget.prototype.destroy.call( this );
                     }
        });
    $.widget( "ui.combobox_req_description_old", {
        _create: function() {
                     var input,
        that = this,
        select = this.element.hide(),
        selected = select.children( ":selected" ),
        value = selected.val() ? selected.text() : "",
        wrapper = this.wrapper = $( "<span>" )
        .addclass( "ui-combobox" )
        .insertafter( select );

    function removeifinvalid(element) {
        var value = $( element ).val(),
        matcher = new regexp( "^" + $.ui.autocomplete.escaperegex( value ) + "$", "i" ),
        valid = false;
    select.children( "option" ).each(function() {
        if ( $( this ).text().match( matcher ) ) {
            this.selected = valid = true;
            return false;
        }
    });
    if ( !valid ) {
        // remove invalid value, as it didn't match anything
        $( element )
            //.val( "" )
            .attr( "title", value + " didn't match any item" )
            //.tooltip( "open" );
            $("#req_description").val(value);
        select.val( "" );
        settimeout(function() {
            input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        input.data( "autocomplete" ).term = "";
        return false;
    };
    };

    input = $( "<input>" )
        .appendto( wrapper )
        .val( value )
        .attr( "title", "" )
        .addclass( "ui-state-default ui-combobox-input" )
        .autocomplete({
            delay: 0,
            minlength: 0,
            height: 250,
            source: function( request, response ) {
                var matcher = new regexp( $.ui.autocomplete.escaperegex(request.term), "i" );
                response( select.children( "option" ).map(function() {
                    var text = $( this ).text();
                    if ( this.value && ( !request.term || matcher.test(text) ) )
                    return {
                        label: text.replace(
                                   new regexp(
                                       "(?![^&;]+;)(?!<[^<>]*)(" +
                                       $.ui.autocomplete.escaperegex(request.term) +
                                       ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                       ), "<strong>$1</strong>" ),
                            value: text,
                    option: this
                    };
                }) );
            },
            select: function( event, ui ) {
                        ui.item.option.selected = true;
                        that._trigger( "selected", event, {
                            item: ui.item.option
                        });
                        $("#req_description").val(ui.item.option.value)
                            //$("#activesiteid").val(ui.item.option.value);
                            //$( "#purchase_req_new_tabs" ).tabs("option","active", 1 );
                            //ready_new_req()
                    },
            change: function( event, ui ) {
                        if ( !ui.item )
                            return removeifinvalid( this );
                    }
        })
    .addclass( "ui-widget ui-widget-content ui-corner-left" );

    input.data( "autocomplete" )._renderitem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendto( ul );
    };

    $( "<a>" )
        .attr( "tabindex", -1 )
        .attr( "title", "show all items from supplier" )
        .tooltip()
        .appendto( wrapper )
        .button({
            icons: {
                       primary: "ui-icon-triangle-1-s"
                   },
            text: false
        })
    .removeclass( "ui-corner-all" )
        .addclass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
            // close if already visible
            if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                input.autocomplete( "close" );
                removeifinvalid( input );
                return;
            }

            // work around a bug (likely same cause as #5265)
            $( this ).blur();

            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
            input.focus();
        });

    input
        .tooltip({
            position: {
                          of: this.button
                      },
            tooltipclass: "ui-state-highlight"
        });
                 },

            destroy: function() {
                         this.wrapper.remove();
                         this.element.show();
                         $.widget.prototype.destroy.call( this );
                     }
    })
    $.widget( "ui.combobox_contracts_buying", {
        _create: function() {
                     var input,
    that = this,
    select = this.element.hide(),
    selected = select.children( ":selected" ),
    value = selected.val() ? selected.text() : "",
    wrapper = this.wrapper = $( "<span>" )
        .addClass( "ui-combobox" )
        .insertAfter( select );

    function removeIfInvalid(element) {
        var value = $( element ).val(),
    matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( value ) + "$", "i" ),
    valid = false;
    select.children( "option" ).each(function() {
        if ( $( this ).text().match( matcher ) ) {
            this.selected = valid = true;
            return false;
        }
    });
    if ( !valid ) {
        // remove invalid value, as it didn't match anything
        $( element )
            .val( "" )
            .attr( "title", value + " didn't match any item" )
            .tooltip( "open" );
        select.val( "" );
        setTimeout(function() {
            input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        input.data( "autocomplete" ).term = "";
        return false;
    }
    }

    input = $( "<input>" )
        .appendTo( wrapper )
        .val( value )
        .attr( "title", "" )
        .addClass( "ui-state-default ui-combobox-input" )
        .autocomplete({
            delay: 0,
        minLength: 0,
        height: 250,
        source: function( request, response ) {
            var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
                var text = $( this ).text();
                if ( this.value && ( !request.term || matcher.test(text) ) )
                return {
                    label: text.replace(
                               new RegExp(
                                   "(?![^&;]+;)(?!<[^<>]*)(" +
                                   $.ui.autocomplete.escapeRegex(request.term) +
                                   ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                   ), "<strong>$1</strong>" ),
                        value: text,
                option: this
                };
            }) );
        },
        select: function( event, ui ) {
                    ui.item.option.selected = true;
                    that._trigger( "selected", event, {
                        item: ui.item.option
                    });
                    //loadPurchaseOrderItemsPerJCNO(ui.item.option.value,"ui-tabs-PurchaseReqsContract");
                    //loadPurchaseOrderItemsPerJCNO(ui.item.option.value,"req-new-form");
                    var active_supplierid = $( "#activesupplierid" ).val();
                    $("#ui-tabs-PurchaseReqsContract").load("/logisticscont/purchase_reqs_per_jcno/"+ui.item.option.value);
                    $("#req-new-form-buttons").fadeIn(3500);
                    $("#req-holding-items-form").fadeIn(4500);
                    $("#activesiteid").val(ui.item.option.value);
                    $("#purchase_req_new_tabs" ).tabs("option","active", 1);
                    //ready_new_req()
                },
        change: function( event, ui ) {
                    if ( !ui.item )
                        return removeIfInvalid( this );
                }
        })
    .addClass( "ui-widget ui-widget-content ui-corner-left" );

    input.data( "autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
    };

    $( "<a>" )
        .attr( "tabIndex", -1 )
        .attr( "title", "Show All Contracts" )
        .tooltip()
        .appendTo( wrapper )
        .button({
            icons: {
                       primary: "ui-icon-triangle-1-s"
                   },
            text: false
        })
    .removeClass( "ui-corner-all" )
        .addClass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
            // close if already visible
            if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                input.autocomplete( "close" );
                removeIfInvalid( input );
                return;
            }

            // work around a bug (likely same cause as #5265)
            $( this ).blur();

            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
            input.focus();
        });

    input
        .tooltip({
            position: {
                          of: this.button
                      },
            tooltipClass: "ui-state-highlight"
        });
                 },

        destroy: function() {
                     this.wrapper.remove();
                     this.element.show();
                     $.Widget.prototype.destroy.call( this );
                 }
    })
    $.widget( "ui.combobox_suppliers_buying", {
        _create: function() {
                     var input,
    that = this,
    select = this.element.hide(),
    selected = select.children( ":selected" ),
    value = selected.val() ? selected.text() : "",
    wrapper = this.wrapper = $( "<span>" )
        .addClass( "ui-combobox" )
        .insertAfter( select );

    function removeIfInvalid(element) {
        var value = $( element ).val(),
    matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( value ) + "$", "i" ),
    valid = false;
    select.children( "option" ).each(function() {
        if ( $( this ).text().match( matcher ) ) {
            this.selected = valid = true;
            return false;
        }
    });
    if ( !valid ) {
        // remove invalid value, as it didn't match anything
        $( element )
            .val( "" )
            .attr( "title", value + " didn't match any item" )
            .tooltip( "open" );
        select.val( "" );
        setTimeout(function() {
            input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        input.data( "autocomplete" ).term = "";
        return false;
    }
    }

    input = $( "<input>" )
        .appendTo( wrapper )
        .val( value )
        .attr( "title", "" )
        .addClass( "ui-state-default ui-combobox-input" )
        .autocomplete({
            delay: 0,
        minLength: 0,
        height: 250,
        source: function( request, response ) {
            var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
                var text = $( this ).text();
                if ( this.value && ( !request.term || matcher.test(text) ) )
                return {
                    label: text.replace(
                               new RegExp(
                                   "(?![^&;]+;)(?!<[^<>]*)(" +
                                   $.ui.autocomplete.escapeRegex(request.term) +
                                   ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                   ), "<strong>$1</strong>" ),
                        value: text,
                option: this
                };
            }) );
        },
        select: function( event, ui ) {
                    ui.item.option.selected = true;
                    that._trigger( "selected", event, {
                        item: ui.item.option
                    });

                    var suppliertext = $( "#combobox_suppliers_buying :selected").text();
                    //alert(suppliertext)
                    $("#activesupplierid_buying").val(ui.item.option.value);
                    $("#add-new-porder").fadeIn('slow');
                    $("#view-old-porder").fadeIn('slow');
                    //$("#prefered_supplier").val(suppliertext)
                    //$("#log").load("/mngntcont/ajaxgetproductioncontractbudget/500",callback_load_contract_other_reqs); return false;
                    //$("#open_order_list").load("/logisticscont/get_supplier_open_orders/"+ui.item.option.value,callback_load_po_supplier); return false;
                },
        change: function( event, ui ) {
                    if ( !ui.item )
                        return removeIfInvalid( this );
                }
        })
    .addClass( "ui-widget ui-widget-content ui-corner-left" );

    input.data( "autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
    };

    $( "<a>" )
        .attr( "tabIndex", -1 )
        .attr( "title", "Show All Suppliers" )
        .tooltip()
        .appendTo( wrapper )
        .button({
            icons: {
                       primary: "ui-icon-triangle-1-s"
                   },
            text: false
        })
    .removeClass( "ui-corner-all" )
        .addClass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
            // close if already visible
            if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                input.autocomplete( "close" );
                removeIfInvalid( input );
                return;
            }

            // work around a bug (likely same cause as #5265)
            $( this ).blur();

            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
            input.focus();
        });

    input
        .tooltip({
            position: {
                          of: this.button
                      },
            tooltipClass: "ui-state-highlight"
        });
                 },

        destroy: function() {
                     this.wrapper.remove();
                     this.element.show();
                     $.Widget.prototype.destroy.call( this );
                 }
    })
    $.widget( "ui.combobox_suppliers_grv_old", {
        _create: function() {
                     var input,
    that = this,
    select = this.element.hide(),
    selected = select.children( ":selected" ),
    value = selected.val() ? selected.text() : "",
    wrapper = this.wrapper = $( "<span>" )
        .addclass( "ui-combobox" )
        .insertafter( select );

    function removeifinvalid(element) {
        var value = $( element ).val(),
    matcher = new regexp( "^" + $.ui.autocomplete.escaperegex( value ) + "$", "i" ),
    valid = false;
    select.children( "option" ).each(function() {
        if ( $( this ).text().match( matcher ) ) {
            this.selected = valid = true;
            return false;
        }
    });
    if ( !valid ) {
        // remove invalid value, as it didn't match anything
        $( element )
            .val( "" )
            .attr( "title", value + " didn't match any item" )
            .tooltip( "open" );
        select.val( "" );
        settimeout(function() {
            input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        input.data( "autocomplete" ).term = "";
        return false;
    }
    }

    input = $( "<input>" )
        .appendto( wrapper )
        .val( value )
        .attr( "title", "" )
        .addclass( "ui-state-default ui-combobox-input" )
        .autocomplete({
            delay: 0,
        minlength: 0,
        height: 250,
        source: function( request, response ) {
            var matcher = new regexp( $.ui.autocomplete.escaperegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
                var text = $( this ).text();
                if ( this.value && ( !request.term || matcher.test(text) ) )
                return {
                    label: text.replace(
                               new regexp(
                                   "(?![^&;]+;)(?!<[^<>]*)(" +
                                   $.ui.autocomplete.escaperegex(request.term) +
                                   ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                   ), "<strong>$1</strong>" ),
                        value: text,
                option: this
                };
            }) );
        },
        select: function( event, ui ) {
                    ui.item.option.selected = true;
                    that._trigger( "selected", event, {
                        item: ui.item.option
                    });

                    var suppliertext = $( "#combobox_suppliers_grv :selected").text();
                    //alert(suppliertext)
                    $("#activesupplierid_grv").val(ui.item.option.value)
                        //$("#prefered_supplier").val(suppliertext)
                        //$("#log").load("/mngntcont/ajaxgetproductioncontractbudget/500",callback_load_contract_other_reqs); return false;
                        $("#open_order_list").load("/logisticscont/get_supplier_open_orders/"+ui.item.option.value,callback_load_po_supplier); return false;
                },
        change: function( event, ui ) {
                    if ( !ui.item )
                        return removeifinvalid( this );
                }
        })
    .addclass( "ui-widget ui-widget-content ui-corner-left" );

    input.data( "autocomplete" )._renderitem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendto( ul );
    };

    $( "<a>" )
        .attr( "tabindex", -1 )
        .attr( "title", "show all suppliers" )
        .tooltip()
        .appendto( wrapper )
        .button({
            icons: {
                       primary: "ui-icon-triangle-1-s"
                   },
            text: false
        })
    .removeclass( "ui-corner-all" )
        .addclass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
            // close if already visible
            if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                input.autocomplete( "close" );
                removeifinvalid( input );
                return;
            }

            // work around a bug (likely same cause as #5265)
            $( this ).blur();

            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
            input.focus();
        });

    input
        .tooltip({
            position: {
                          of: this.button
                      },
            tooltipclass: "ui-state-highlight"
        });
                 },

        destroy: function() {
                     this.wrapper.remove();
                     this.element.show();
                     $.widget.prototype.destroy.call( this );
                 }
    })
    $.widget( "ui.combobox_suppliers_grv", {
        _create: function() {
                     var input,
    that = this,
    select = this.element.hide(),
    selected = select.children( ":selected" ),
    value = selected.val() ? selected.text() : "",
    wrapper = this.wrapper = $( "<span>" )
        .addClass( "ui-combobox" )
        .insertAfter( select );

    function removeIfInvalid(element) {
        var value = $( element ).val(),
    matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( value ) + "$", "i" ),
    valid = false;
    select.children( "option" ).each(function() {
        if ( $( this ).text().match( matcher ) ) {
            this.selected = valid = true;
            return false;
        }
    });
    if ( !valid ) {
        // remove invalid value, as it didn't match anything
        $( element )
            .val( "" )
            .attr( "title", value + " didn't match any item" )
            .tooltip( "open" );
        select.val( "" );
        setTimeout(function() {
            input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        input.data( "autocomplete" ).term = "";
        return false;
    }
    }

    input = $( "<input>" )
        .appendTo( wrapper )
        .val( value )
        .attr( "title", "" )
        .addClass( "ui-state-default ui-combobox-input" )
        .autocomplete({
            delay: 0,
        minLength: 0,
        height: 250,
        source: function( request, response ) {
            var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
                var text = $( this ).text();
                if ( this.value && ( !request.term || matcher.test(text) ) )
                return {
                    label: text.replace(
                               new RegExp(
                                   "(?![^&;]+;)(?!<[^<>]*)(" +
                                   $.ui.autocomplete.escapeRegex(request.term) +
                                   ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                   ), "<strong>$1</strong>" ),
                        value: text,
                option: this
                };
            }) );
        },
        select: function( event, ui ) {
                    ui.item.option.selected = true;
                    that._trigger( "selected", event, {
                        item: ui.item.option
                    });
                    var suppliertext = $( "#combobox_suppliers_grv :selected").text();
                    $("#activesupplierid_grv").val(ui.item.option.value)
                        $("#open_order_list").load("/logisticscont/get_supplier_open_orders/"+ui.item.option.value,callback_load_po_supplier); return false;
                },
        change: function( event, ui ) {
                    if ( !ui.item )
                        return removeIfInvalid( this );
                }
        })
    .addClass( "ui-widget ui-widget-content ui-corner-left" );

    input.data( "autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
    };

    $( "<a>" )
        .attr( "tabIndex", -1 )
        .attr( "title", "Show All Suppliers" )
        .tooltip()
        .appendTo( wrapper )
        .button({
            icons: {
                       primary: "ui-icon-triangle-1-s"
                   },
            text: false
        })
    .removeClass( "ui-corner-all" )
        .addClass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
            // close if already visible
            if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                input.autocomplete( "close" );
                removeIfInvalid( input );
                return;
            }

            // work around a bug (likely same cause as #5265)
            $( this ).blur();

            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
            input.focus();
        });

    input
        .tooltip({
            position: {
                          of: this.button
                      },
            tooltipClass: "ui-state-highlight"
        });
                 },

        destroy: function() {
                     this.wrapper.remove();
                     this.element.show();
                     $.Widget.prototype.destroy.call( this );
                 }
    });
    //})
    //( jQuery );
    //*************Comboboxes end*******************************
    //**********************************************************
    function callback_load_po_supplier(){
        $("#grv_open_orders_table").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                $("#activepoid_grv").val(col0text);
                $( "#grv_console_tabs" ).tabs("option","active", 1 );
                $("#grv_details").empty()
            $("#grv_items").empty()
            $("#grv_details").load("/logisticscont/grv_order_one_details/"+parseInt(col0text),callback_load_order_items_grv);
            }else   {
                $(this).removeClass("hover");
            }
        });
    };
    function callback_load_order_items_grv(){
        $("#grv_order_items_table").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                var col1text = $(this).find("td").eq(1).html();
                $("#grv_items").empty()
            $("#grv_items").load("/logisticscont/grv_order_one_item/"+parseInt(col0text)+"/"+parseInt(col1text),callback_load_form_grv);
        $( "#grv_console_tabs" ).tabs("option","active", 2 );
        $("#activepoitemid_grv").val(col0text)
            }else   {
                $(this).removeClass("hover");
            }
        });
    };
    function callback_load_form_grv(){
        $( "#grv_date" ).datepicker();
        $( "#grv_date" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
        //var values = $delqty 
        $( "#add-grv-to-list" ).click(function(e) {
            e.preventDefault();
            var uniqid4 = Math.random()
            var deldate = $("#grv_date").val();
        var delnote = $("#grv_del_num").val();
        var delqty = $("#grv_qty").val();
        var delstore = $("#grv_store").val();
        var poitemid = $("#grv_order_item_one_table").find("td").eq(0).html();
        var activepoid =  $("#activepoitemid_grv").val();
        var jqxhr = $.post("/logisticscont/grv_save_new_item/"+uniqid4+"/"+parseInt(poitemid)+"/"+deldate+"/"+delnote+"/"+delqty+"/"+delstore, function(data) {
            $( "#grv_console_tabs" ).tabs("option","active", 1 );
            var activepo = $("#activepoid_grv").val();
            $("#grv_details").empty()
            $("#grv_items").empty()
            $("#grv_details").load("/logisticscont/grv_order_one_details/"+parseInt(activepo),callback_load_order_items_grv);
        })
        });
    };
    $("#add-new-porder").click(function(e) {
        e.preventDefault();
        var activesupplier = $("#activesupplierid_buying").val();
        $("#add-new-porder").fadeOut(1500);
        $("#combobox_suppliers_buying_form").fadeOut(1500);
        $("#view-old-porder").fadeOut(1500);
        $(".ui-combobox").fadeOut(1500);
        $("#reset-porder").fadeIn(2500);
        var uniqid9 = Math.random();
        $("#supplier_open_order_list").load("/logisticscont/new_po_order_supplier/"+uniqid9+"/"+activesupplier,callback_load_form_buying_old_po); return false;
        return false;
    });
    $("#view-old-porder").click(function(e) {
        e.preventDefault();
        var activesupplier = $("#activesupplierid_buying").val();
        $("#add-new-porder").fadeOut(1500);
        $("#view-old-porder").fadeOut(1500);
        $("#combobox_suppliers_buying_form").fadeOut(1500);
        $(".ui-combobox").fadeOut(1500);
        $("#reset-porder").fadeIn(2500);
        $("#supplier_open_order_list").load("/logisticscont/get_po_order_supplier_open_orders/"+activesupplier,callback_load_form_buying_old_po); return false;
        //webkitRequestFullScreen();
        //window.location.reload();
        return false;
    });
    $("#reset-porder").click(function(e) {
        window.location.reload(true);
    });
    function callback_load_form_buying_new_po(){
        $( "#grv_date" ).datepicker();
        $( "#grv_date" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
        //var values = $delqty 
        $( "#add-grv-to-list" ).click(function(e) {
            e.preventDefault();
            var uniqid4 = Math.random()
            var deldate = $("#grv_date").val();
        var delnote = $("#grv_del_num").val();
        var delqty = $("#grv_qty").val();
        var delstore = $("#grv_store").val();
        var poitemid = $("#grv_order_item_one_table").find("td").eq(0).html();
        var activepoid =  $("#activepoitemid_grv").val();
        var jqxhr = $.post("/logisticscont/grv_save_new_item/"+uniqid4+"/"+parseInt(poitemid)+"/"+deldate+"/"+delnote+"/"+delqty+"/"+delstore, function(data) {
            $( "#grv_console_tabs" ).tabs("option","active", 1 );
            var activepo = $("#activepoid_grv").val();
            $("#grv_details").empty()
            $("#grv_items").empty()
            $("#grv_details").load("/logisticscont/grv_order_one_details/"+parseInt(activepo),callback_load_order_items_grv);
        })
        });
    };
    function callback_load_form_buying_old_po(){
        $("#po_order_open_orders_table").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                $( "#buying_console_tabs" ).tabs("enable", 4 );
            }else   {
                $(this).removeClass("hover");
            }
        });

        $("#po_order_open_orders_table").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 4){ 
                    var uniqid = Math.random();
                    var col0text = $(this).parent().find("td").eq(0).html();
                    $("#activepoid_buying").val(alltrim(col0text));
                    activepoid = $("#activepoid_buying").val();
                    if (activepoid !== null){
                        $("#activepodisplay").html(activepoid);
                        $("#ui_tabs_ThisOrder").load("/logisticscont/po_order_one_details/"+alltrim(col0text), function(data) {
                            $( "#buying_console_tabs" ).tabs("option","active", 5 );
                            $("#purchase_order_items_table").delegate('tr','mouseover mouseleave click',function(e) {
                                e.preventDefault();
                                //e.stopPropagation();
                                if (e.type == 'mouseover') {
                                    $(this).addClass("hover");
                                } else if ( e.type == 'click' ) {
                                    //var values = '';
                                    //var tds = $(this).find('td');
                                }else   {
                                    $(this).removeClass("hover");
                                }
                            });
                            $("#purchase_order_items_table").delegate('td','click',function(e){
                                if ($(this).parent().index() != 0){ 
                                    //console.log($(this).index());
                                    if ($(this).index() == 13){ 
                                        //console.log("notes pressed");
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
                                        $( "#edit_description" ).css("width","400px");
                                        $("#edit_orderno").val(alltrim(col1text)); 
                                        $("#edit_orderid").val(alltrim(col0text)); 
                                        $("#edit_description").val(alltrim(col4text)); 
                                        $("#edit_unit").val(alltrim(col5text)); 
                                        $("#edit_qty").val(alltrim(col7text)); 
                                        $("#edit_price").val(alltrim(col8text)); 
                                        $("#edit_total").val(alltrim(col9text)); 
                                        $("#edit_description").focus(); 
                                        $( "#dialog_edit_buying_item" ).dialog("open");
                                        $( "#edit_qty" ).change(function(e){
                                            if (col8text && $(this).val()){
                                                var supp_price = $("#edit_price").val();
                                                var supp_total = parseFloat(supp_price)*parseFloat($(this).val());
                                                //console.log(supp_total);
                                                $( "#edit_total" ).val(supp_total.toFixed(2));
                                            };
                                        });
                                        $( "#edit_price" ).change(function(e){
                                            if (col7text && $(this).val()){
                                                var supp_qty = $("#edit_qty").val();
                                                var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
                                                //console.log(supp_total);
                                                $( "#edit_total" ).val(supp_total.toFixed(2));
                                            };
                                        });
                                        //$( "#purchasereq_notes_all_buying" ).load("/logisticscont/ajaxpurchase_reqs_notes_all/"+alltrim(reqitemid),function(){
                                        //    var thisnote = $("#purchasereq_notes_all_buying").val();
                                        //});
                                    };
                                };
                            });


                        });                          
                    }else{
                        //$(this).parent().remove();
                        $("#warningdiv").html("No Budget, No Requisition, No Order")
                            $("#warningdiv").fadeIn(2000,function(){
                                $("#warningdiv").fadeOut('slow')    
                            });return false;

                    };
                };
                if ($(this).index() == 65){ 
                    //console.log("prices pressed on approval");
                    var uniqid = Math.random()
                        var col0text = $(this).parent().find("td").eq(0).html();
                    var col1text = $(this).parent().find("td").eq(1).html();
                    var col5text = $(this).parent().find("td").eq(5).html();
                    var col6text = $(this).parent().find("td").eq(6).html();
                    var col7text = $(this).parent().find("td").eq(7).html();
                    //console.log(col0text)
                };
            };
        });
        //disabled: [2,4]
    };
    $( "#dialog_purchasereq_notes" ).dialog({
        autoOpen: false,
        height: 670,
        width: 600,
        modal: true,
        buttons: {
            "Add Note": function() {
                var bValid = true;
                //allsiteFields.removeClass( "ui-state-error" );
                //bValid = bValid && checkLength( sitename, "site name", 3, 120 );
                //bValid = bValid && checkLength( email, "email", 6, 80 );

                //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );

                if ( bValid ) {
                    var reqitemid = $("#activereqitemid").val();
                    var uniqid = Math.random()
        var formserial = $("#dialog_purchasereq_notes_form").serialize();
    var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_add_new_note/"+uniqid+"/"+reqitemid+"?"+formserial, function(data) {
        var activejcno = $("#activesiteid").val();
        //$("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
    })
    //LoadNewSiteData(sitename.val(),description.val(),area.val(),wonumber.val(),supervisor.val())
    //$( this ).find('textarea').val('');
    $("#purchasereq_notes_new").val('');
    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                        $("#purchasereq_notes_new").val('');
                        $( this ).dialog( "close" );
                    }
        },
        close: function() {
                   //allsiteFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $( "#dialog_purchasereq_notes_buying" ).dialog({
        autoOpen: false,
        height: 670,
        width: 600,
        modal: true,
        buttons: {
            "Add Note": function() {
                var bValid = true;
                if ( bValid ) {
                    var reqitemid = $("#activereqitemid_buying").val();
                    var uniqid = Math.random();
                    var formserial = $("#dialog_purchasereq_notes_form_buying").serialize();
                    var jqxhr = $.post("/logisticscont/ajaxpurchase_reqs_add_new_note_buyingside/"+uniqid+"/"+reqitemid+"?"+formserial, function(data) {
                        $("#ui_tabs_ThisOrder").load("/logisticscont/po_order_one_details/"+alltrim(col0text), function(data) {
                            $( "#buying_console_tabs" ).tabs("option","active", 5 );
                        });
                    });
                    $("#purchasereq_notes_new_buying").val('');
                    $( this ).dialog( "close" );
                };
            },
        Cancel: function() {
                    $("#purchasereq_notes_new_buying").val('');
                    $( this ).dialog( "close" );
                }
        },
        close: function() {
                   //allsiteFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    function replaceforward2back(dataStr) {
        //console.log(dataStr.replace(/\//g, "-"));
        return dataStr.replace(/\//g, "-");
    };
    function alltrim(str) {
        return str.replace(/^\s+|\s+$/g, '');
    };
    $("#btn_get_supplier_time_view").click(function(){
        //console.log("Button Pressed");
        var formserial = $("#form_supplier_view_dates").serialize();
        $("#divSupplierView").empty();
        $("#divSupplierView").load("/logisticscont/get_supplier_po_orders_time?"+formserial); 
        return false;
    });
    $("#btn_get_grv_time_view").click(function(){
        //console.log("Button Pressed");
        var formserial = $("#form_poitem_view_grv").serialize();
        $("#buying_items_grv").empty();
        $("#buying_items_grv").addClass("spinner");
        $("#buying_items_grv").load("/logisticscont/get_poitems_grv_info?"+formserial); 
            $("#buying_items_grv").removeClass("spinner");
        return false;
    });
    $("#btn_get_searchphrase").click(function(){
        var formserial = $("#form_supplier_view_items").serialize();
        //console.log(formserial);
        $("#divSupplierItems").load("/logisticscont/do_search_description?"+formserial); 
        return false;
    });
    $( "#dialog_edit_buying_item" ).dialog({
        autoOpen: false,
        height: 350,
        width: 450,
        //modal: true,
        buttons: {
            "Edit Buying Item": function() {
                var bValid = true;
                   if ( bValid ) {
                    var formserial = $("#dialog_edit_buying_item_form").serialize();
                    var editorderno = alltrim($("#edit_orderno").val());
                    var orderitemid = alltrim($("#edit_orderid").val());
                    var jqxhr = $.post("/logisticscont/ajaxEditBuyingItem?"+formserial+"&edit_orderno="+editorderno+"&edit_orderid="+orderitemid, function(data) {

                        $("#ui_tabs_ThisOrder").load("/logisticscont/po_order_one_details/"+alltrim(editorderno), function(data) {
                            $( "#buying_console_tabs" ).tabs("option","active", 5 );
                        });
                    });
                    //$( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                        $( this ).find('input').val('');
                        $( this ).dialog( "close" );
                    }
        },
        close: function() {
                   //allreqitemFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $("#btn_supplier_edit").click(function(event) {
        var formserial = $("#supplier_edit_form").serialize();
        var jqxhr = $.post("/logisticscont/save_edit_buying_supplier?"+formserial, function(data) {
            window.location="/logisticscont/search_supplier";

        });
        return false;
    });
    $( "li", $("#buying_gallery") ).click(function(event) {
        var target = $( event.target );
        var person = $(this);    
        personid = person.children('div').html(),
        $("#buying_reqs_per_user").load("/logisticscont/purchase_reqs_items_all_active_by_user/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
            //alert("External content loaded successfully!");
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
    $("#button_supplier_new").click(function(event) {
        var formserial = $("#new_supplier_form").serialize();
        var jqxhr = $.post("/logisticscont/addsupplier?"+formserial, function(data) {
            window.location="/logisticscont/search_supplier";
        });
        return false;
    });
    $("#button_store_new").click(function(event) {
        var formserial = $("#new_store_form").serialize();
        var jqxhr = $.post("/logisticscont/addstorelocation?"+formserial, function(data) {
            window.location="/logisticscont/showstoresall";
        });
        return false;
    });
    $("#button_store_edit").click(function(event) {
        var formserial = $("#edit_store_form").serialize();
        //console.log(formserial);
        var jqxhr = $.post("/logisticscont/saveeditstores?"+formserial, function(data) {
            window.location="/logisticscont/showstoresall";
        });
        return false;
    });
});
function toggleFullScreen() {
    if (!document.fullscreenElement &&    // alternative standard method
            !document.mozFullScreenElement && !document.webkitFullscreenElement) {  // current working methods
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }
};

$(document).ready(function(){
    $( "#combobox_suppliers_grv" ).combobox_suppliers_grv();
    $( "#combobox_contracts_grv" ).combobox_contracts_grv();
    $( "#combobox_suppliers_buying" ).combobox_suppliers_buying();
    $( "#combobox_contracts_buying" ).combobox_contracts_buying();
    $( "#supplierview_to_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#button_supplier_new" ).button();
    //$(document).tooltip({
    //    track: true
    //});
    $( "#supplierview_from_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#suppliername_edit").css("width","400px");
    $("#supplieraddress_edit").css("width","400px");
    $("#suppliercity_edit").css("width","400px");
    $("#grvview_to_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" )
    $("#grvview_from_date").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" )
});
