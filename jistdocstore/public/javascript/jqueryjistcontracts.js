//Handels the contracts and purchase req pages
//Dec 2012-12-25
$(function(){
    $("#req-new-form-buttons").hide();
    $("#req-holding-items-form").hide();
    $("#add-req-done").hide();
    $("#add-req-done-cancel").hide();
    $( "#contract_overview_tabs" ).tabs({ heightStyle: "fill" });
    $( "#purchase_req_new_tabs" ).tabs({ 
        heightStyle: "fill",
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {

        }

    });
    $( "#budget-console-tabs" ).tabs({ 
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
                    $("#myjistconsole_tabs").tabs("add","/logisticscont/grv_req_one_items/"+col2text,"Req ID"+col2text,4);
                    $("#myjistconsole_tabs").tabs('select', 4);
                }else   {
                    $(this).removeClass("hover");
                }
            });

        }
    });
    //*************Comboboxes start*****************************
    //**********************************************************
    (function( $ ) {
        $.widget( "ui.combobox_jcno", {
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
                        loadOverviewContractData(ui.item.option.value)

                            $("#ui-tabs-Contractual").load("/contractscont/ajaxsitescontractstatusupdate/"+ui.item.option.value);
                        $("#ui-tabs-POItems").load("/contractscont/ajaxsitescontractorderitems/"+ui.item.option.value,callback_after_main_poitems);
                        $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+ui.item.option.value,callback_after_main_sow);
                        $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+ui.item.option.value,callback_after_main_budget);
                        $("#ui-tabs-PaymentReqs").load("/mngntcont/get_all_payment_reqs_per_contract/"+ui.item.option.value);
                        $("#ui-tabs-POReqs").load("/logisticscont/purchase_reqs_per_jcno/"+ui.item.option.value);
                        $("#activesiteid").val(ui.item.option.value)
                            $( "#contract_overview_tabs" ).tabs("option","active", 1 );
                        //$( "#contract_overview_tabs" ).tabs( "refresh" );
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
        });

        $.widget( "ui.combobox_suppliers", {
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

                        var suppliertext = $( "#combobox_suppliers :selected").text();
                        //alert(suppliertext)
                        $("#activesupplierid").val(ui.item.option.value)
                            $("#prefered_supplier").val(suppliertext)
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

        $.widget( "ui.combobox_contracts_req", {
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
                        //loadContractProductionBudget(ui.item.option.value,"ui-tabs-PurchaseReqsBudgets");
                        $("#ui-tabs-PurchaseReqsBudgets").load("/mngntcont/ajaxgetproductioncontractbudget/"+ui.item.option.value,function(){
                            $("#production_budget_table").delegate('tr','mouseover mouseleave click',function(e) {
                                //e.preventDefault();
                                //e.stopPropagation();
                                if (e.type == 'mouseover') {
                                    $(this).addClass("hover");
                                } else if ( e.type == 'click' ) {
                                    var values = '';
                                    var tds = $(this).find('td');
                                    var col0text = $(this).find("td").eq(0).html();
                                    var col1text = $(this).find("td").eq(1).html();
                                    var col2text = $(this).find("td").eq(2).html();
                                    $("#production_budget_totals").load("/mngntcont/ajaxgetbudget_bybudget_id/"+col0text,function(){$(this).addClass("hoverclicked");});
                                }else if (e.type == 'mouseleave') {
                                    $(this).removeClass("hoverclicked");
                                    $(this).removeClass("hover");
                                }else   {
                                    $(this).removeClass("hover");
                                    $(this).removeClass("hoverclicked");
                                };
                            });
                        });
                        //$("#req-new-form").load("/logisticscont/purchase_reqs_items_add_form/"+ui.item.option.value+"/"+active_supplierid,callback_load_req_jcno_budget);
                        $("#req-new-form").load("/logisticscont/purchase_reqs_items_add_form/"+ui.item.option.value+"/"+active_supplierid,callback_load_req_jcno_budget);
                        $("#activesiteid").val(ui.item.option.value);
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
        });

        $.widget( "ui.combobox_req_description", {
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
                //.val( "" )
                $("#req_description").val(value)
                .attr( "title", value + " didn't match any item" )
                //.tooltip( "open" );
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
                        $("#req_description").val(ui.item.option.value);
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
            .attr( "title", "Show All Items From Supplier" )
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
    })
    ( jQuery );
    //*************Comboboxes end*******************************
    //**********************************************************

    var req_jcno = $( "#req_jcno" ),
        req_budget_item = $( "#req_budget_item" ),
        req_item = $( "#req_item" ),
        req_description = $( "#req_description" ),
        req_unit = $( "#req_unit" ),
        req_qty = $( "#req_qty" ),
        //allreqitemFields = $( [] ).add( scopename ).add( scopeunit ).add( scopeqty ),
        req_musthavedate= $( "#req_musthavedate" ).datepicker();
    $( "#req_musthavedate" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#dialog-newpurchasereqitem" ).dialog({
        autoOpen: false,
        height: 350,
        width: 250,
        //modal: true,
        buttons: {
            "Add New Item To Purchase Req": function() {
                var bValid = true;
                allreqitemFields.removeClass( "ui-state-error" );
                //bValid = bValid && checkLength( scopename, "site name", 3, 80 );
                //bValid = bValid && checkLength( email, "email", 6, 80 );

                //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );

                if ( bValid ) {
                    //LoadNewScopeData(scopename.val(),scopeunit.val(),scopeqty.val())
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
            },
        Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
        },
        close: function() {
                   allreqitemFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $( "#add-new-req" ).click(function(e) {
        //console.log(e)
        var pref_supp = $("#prefered_supplier").val();
        var pref_date = $("#req_musthavedate").val();
        var activejcno = $("#activesiteid").val();
        if (pref_date === '' || pref_supp === '' ){
            //alert("It is null")
            $("#warningdiv").html("No Date, No Supplier, No JCNo ==> No Requisition")
        $("#warningdiv").fadeIn(2000,function(){
            $("#warningdiv").fadeOut('slow')    
        });return false;
        }
        //loadNewReq(activejcno,pref_date,pref_supp,"log")
        var uniqid2 = Math.random();
        $( "#purchase_req_new_tabs" ).tabs("option","active", 1 );
        e.preventDefault(); 
        var jqxhr = $.post("/logisticscont/savenew_requisition/"+uniqid2+"/"+activejcno+"/"+pref_date+"/"+pref_supp,function(data,status,xhr) {
            var newreq_id = parseInt(data);
            //alert (newreq_id)
            //$("#log").prepend(newreq_id)
            //$("#active_disable_inputs").show()
            if (newreq_id !== null){$( "#activenewreqid" ).val(newreq_id);};
            $("#req-new-form-buttons").fadeIn(3500);
            $("#req-holding-items-form").fadeIn(4500);
            $( "#req_jcno" ).val(activejcno);
            $("#add-new-req").fadeOut(1500);
            $( "#purchase_req_new_tabs" ).tabs("option","active", 1 );
            e.preventDefault(); 
            e.stopPropagation();
        });return false;
    });
    $( "#add-req-done" ).click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        var newreq_id = $( "#activenewreqid" ).val();
        var uniqidtable = Math.random();
        var req_jcno = '';
        var req_budget_id = ''; 
        var req_budget_item = ''; 
        var req_item = '' ;
        var req_description = '' ;
        var req_unit = '' ;
        var req_qty = '' ;
        var uniqid = 0;
        $('#req-holding-table tr').each(function(index,item) {
            if (index !== 0){
                uniqid = Math.random()
            req_jcno = $(this).find("td").eq(0).html();
        req_budget_id = $(this).find("td").eq(1).html();
        req_budget_item = $(this).find("td").eq(2).html();
        req_item = $(this).find("td").eq(3).html();
        req_description = $(this).find("td").eq(4).html();
        req_unit = $(this).find("td").eq(5).html();
        req_qty = $(this).find("td").eq(6).html();
            };
        });
        window.location.reload();
    })
    $( "#add-req-to-list" ).click(function(e) {
        e.preventDefault();
        //var txtthis = $("#new_req_form").serialize();
        var req_jcno = $( "#req_jcno" ).val();
        var req_budget_id = $( "#req_budget_item" ).val();
        var req_budget_item = $( "#req_budget_item :selected").text();
        var req_item = $( "#req_item" ).val();
        var newreq_id = $( "#activenewreqid" ).val();
        //$("#log").prepend(req_item.length);
        if (req_item.length === 0 ){
            req_item = "None";
        };
        var req_description = $( "#req_description" ).val();
        if (req_description.length === 0 ){
            req_description = "None";
        };
        var req_unit = $( "#req_unit" ).val();
        if (req_unit.length === 0 ){
            req_unit = "None";
        };
        var req_qty = $( "#req_qty" ).val();
        if (isNaN( $("#req_qty").val() )) {
            // It isn't a number
            $("#warningdiv").html("Qty has to be a number")
                $("#warningdiv").fadeIn(2000,function(){
                    $("#warningdiv").fadeOut('slow');    
                });return false;
        } else {
            // It is a number
            if (req_qty.length === 0 ){
                req_qty = 0;
            };
        };
        var uniqid1 = Math.random()
            var newrow = $("<tr><td>"+ req_jcno + "</td>"
                    +"<td>"+ req_budget_id + "</td>"
                    +"<td>"+ req_budget_item + "</td>"
                    +"<td>"+ req_item + "</td>"
                    +"<td>"+ req_description + "</td>"
                    +"<td>"+ req_unit + "</td>"
                    +"<td>"+ req_qty + "</td>"
                    +"<td><a id='req_delete'><img src='/images/trash-16.png'></img></a></td>"
                    +"</tr>");
        //alert(req_budget_id)

        if (req_budget_id === null){
            $("#warningdiv").html("No Budget, No Requisition, No Order")
                $("#warningdiv").fadeIn(2000,function(){
                    $("#warningdiv").fadeOut('slow')    
                });return false;
        };
        jrkqxhr = $.post("/logisticscont/savenew_requisition_items/"+uniqid1+"/"+parseInt(newreq_id)+"/"+parseInt(req_jcno)+"/"+parseInt(req_budget_id)+"/"+replaceforward2back(req_item)+"/"+replaceforward2back(req_description)+"/"+req_unit+"/"+parseFloat(req_qty), function(data1,status1,xhr1) {
        });
        //$("#log").prepend(req_item);
        $("#req-holding-table").append(newrow);
        $("#add-req-done").fadeIn('slow');
        $("#add-req-done-cancel").hide();
        $("#req_item").val('');
        $("#req_description").val('');
        $("#req_unit").val('');
        $("#req_qty").val('');
    });
    $("#add-req-done-cancel").click(function(e) {
        e.preventDefault();
        window.location.reload();
        return false;
    });
    function callback_load_req_jcno_budget(){
        //var active_jcno = $("#activesiteid").val();
        //var active_supplierid = $( "#activesupplierid" ).val();
        $( "#combobox_req_description" ).combobox_req_description();
        $( "#combobox_req_description" ).css("width","100px");
        //$( "#req_jcno" ).val(active_jcno);
    };
    function callback_load_contract_other_reqs(){
        var message = $('#log');
        var tr = $('#purchase_req_contract_all_table').find('tr');
        tr.hover(
                function() {  // mouseover
                    $(this).addClass('row-highlight');
                    var values = '';
                    var tds = $(this).find('td');

                    $.each(tds, function(index, item) {
                        values = values + 'td' + (index + 1) + ':' + item.innerHTML + '<br/>';
                    });
                    message.html(values);
                },
                function() {  // mouseout
                    $(this).removeClass('row-highlight');
                    message.html('');
                }
                );
    };
    function callback_after_main_budget(){
        $("#cont_main_budget").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            //e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                //$("#activepoid_buying").val(col0text);
                //console.log(col0text);
                var selectedbudgetid = col0text;
                $("#activebudgetitemid").val(selectedbudgetid);
                $("#cont_budgets_seperated").load("/mngntcont/ajaxgetcontractbudgetseperated/"+selectedbudgetid,callback_after_separate_budget);
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#cont_main_budget").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 5){ 
                    var budgetid = $(this).parent().find("td").eq(0).html();
                    var budgetitem = $(this).parent().find("td").eq(1).html();
                    var budgetdescription = $(this).parent().find("td").eq(2).html();
                    var budgetunit = $(this).parent().find("td").eq(3).html();
                    var budgetqty = $(this).parent().find("td").eq(4).html();
                    var budgetprice = $("#cont_budgets_seperated").find("input").eq(0).val();
                    var budgettotal = $(this).parent().find("td").eq(1).html();
                    //console.log(budgetid);
                    $( "#dialog_editbudgets" ).dialog( "open" );
                    $( "#dialog_editbudgets").find("input").eq(0).val(budgetid);
                    $( "#dialog_editbudgets").find("input").eq(1).val(budgetitem);
                    $( "#dialog_editbudgets").find("input").eq(2).val(budgetdescription);
                    $( "#dialog_editbudgets").find("input").eq(3).val(budgetunit);
                };
                if ($(this).index() == 6){ 
                    //console.log("delete pressed");
                    var budgetid = $(this).parent().find("td").eq(0).html();
                    $(this).parent().remove();
                    var jrkqxhr = $.post("/mngntcont/ajaxeditbudgetactive/"+budgetid+"/"+0, function(data1,status1,xhr1) {
                        var activejcno = $("#activesiteid").val();
                        $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
                    });
                };
                if ($(this).index() == 14){ 
                    console.log("notes pressed");
                };
            };
        });
        $("#img_toggle_budget_add").click(function(){
            //console.log("Clicked");
            $("#dialog_newbudget").dialog("open");
        });
    }
    function callback_after_separate_budget(){
        //$("#percent_choose").insertBefore($("#cont_material_budget")) 
        $("#sel_material_budget").focus();
        $("#button_edit_budget").hide();
        $("#sel_material_budget").change(function(e){
            var nextelem = $("#sel_material_budget + input" );
            var qtyelem = $("#sel_material_budget + input + input" );
            var totalelem = $("#sel_material_budget + input + input + input" );
            var prevelem = $("#sel_material_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            $("#sel_matmarkup_budget" ).prev().val(mat_rate);
            $("#sel_matmarkup_budget" ).change();
            checkbudgetitems();
        });

        $("#sel_matmarkup_budget").change(function(e){
            var nextelem = $("#sel_matmarkup_budget + input" );
            var qtyelem = $("#sel_matmarkup_budget + input + input" );
            var totalelem = $("#sel_matmarkup_budget + input + input + input" );
            var prevelem = $("#sel_matmarkup_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_labour_budget").change(function(e){
            var nextelem = $("#sel_labour_budget + input" );
            var qtyelem = $("#sel_labour_budget + input + input" );
            var totalelem = $("#sel_labour_budget + input + input + input" );
            var prevelem = $("#sel_labour_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_transport_budget").change(function(e){
            var nextelem = $("#sel_transport_budget + input" );
            var qtyelem = $("#sel_transport_budget + input + input" );
            var totalelem = $("#sel_transport_budget + input + input + input" );
            var prevelem = $("#sel_transport_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_healthsafety_budget").change(function(e){
            var nextelem = $("#sel_healthsafety_budget + input" );
            var qtyelem = $("#sel_healthsafety_budget + input + input" );
            var totalelem = $("#sel_healthsafety_budget + input + input + input" );
            var prevelem = $("#sel_healthsafety_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_overheads_budget").change(function(e){
            var nextelem = $("#sel_overheads_budget + input" );
            var qtyelem = $("#sel_overheads_budget + input + input" );
            var totalelem = $("#sel_overheads_budget + input + input + input" );
            var prevelem = $("#sel_overheads_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_specialist_budget").change(function(e){
            var nextelem = $("#sel_specialist_budget + input" );
            var qtyelem = $("#sel_specialist_budget + input + input" );
            var totalelem = $("#sel_specialist_budget + input + input + input" );
            var prevelem = $("#sel_specialist_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_specialist_markup_budget").change(function(e){
            var nextelem = $("#sel_specialist_markup_budget + input" );
            var qtyelem = $("#sel_specialist_markup_budget + input + input" );
            var totalelem = $("#sel_specialist_markup_budget + input + input + input" );
            var prevelem = $("#sel_specialist_markup_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        $("#sel_other_budget").change(function(e){
            var nextelem = $("#sel_other_budget + input" );
            var qtyelem = $("#sel_other_budget + input + input" );
            var totalelem = $("#sel_other_budget + input + input + input" );
            var prevelem = $("#sel_other_budget" ).prev();
            var mat_rate = parseFloat(prevelem.val()*($(this).val()/100)).toFixed(2);
            var mat_total = parseFloat(parseFloat(mat_rate)*parseFloat(qtyelem.val())).toFixed(2);
            nextelem.val(mat_rate);
            totalelem.val(mat_total);
            checkbudgetitems();
        });

        function checkbudgetitems(){
            var thisvalue = $("#sel_material_budget option:selected").val();
            var nextelem = $("#sel_material_budget + input" );
            var qtyelem = $("#sel_material_budget + input + input" );
            var totalelem = $("#sel_material_budget + input + input + input" );
            var prevelem = $("#sel_material_budget" ).prev();
            var mat_rate = nextelem.val();;
            var mat_total = totalelem.val();
            //console.log(mat_rate);

            var thisvalue = $("#sel_matmarkup_budget option:selected").val();
            var nextelem = $("#sel_matmarkup_budget + input" );
            var qtyelem = $("#sel_matmarkup_budget + input + input" );
            var totalelem = $("#sel_matmarkup_budget + input + input + input" );
            var prevelem = $("#sel_material_budget + input" );
            var matmarkup_rate = nextelem.val();
            var matmarkup_total = totalelem.val();
            //console.log(matmarkup_rate);

            var thisvalue = $("#sel_labour_budget option:selected").val();
            var nextelem = $("#sel_labour_budget + input" );
            var qtyelem = $("#sel_labour_budget + input + input" );
            var totalelem = $("#sel_labour_budget + input + input + input" );
            var prevelem = $("#sel_labour_budget" ).prev();
            var lab_rate = nextelem.val();
            var lab_total = totalelem.val();
            //console.log(lab_rate);

            var thisvalue = $("#sel_transport_budget option:selected").val();
            var nextelem = $("#sel_transport_budget + input" );
            var qtyelem = $("#sel_transport_budget + input + input" );
            var totalelem = $("#sel_transport_budget + input + input + input" );
            var prevelem = $("#sel_transport_budget" ).prev();
            var transport_rate = nextelem.val();
            var transport_total = totalelem.val();

            var thisvalue = $("#sel_healthsafety_budget option:selected").val();
            var nextelem = $("#sel_healthsafety_budget + input" );
            var qtyelem = $("#sel_healthsafety_budget + input + input" );
            var totalelem = $("#sel_healthsafety_budget + input + input + input" );
            var prevelem = $("#sel_healthsafety_budget" ).prev();
            var healthsafety_rate = nextelem.val();
            var healthsafety_total = totalelem.val();

            var thisvalue = $("#sel_overheads_budget option:selected").val();
            var nextelem = $("#sel_overheads_budget + input" );
            var qtyelem = $("#sel_overheads_budget + input + input" );
            var totalelem = $("#sel_overheads_budget + input + input + input" );
            var prevelem = $("#sel_overheads_budget" ).prev();
            var overheads_rate = nextelem.val();
            var overheads_total = totalelem.val();

            var thisvalue = $("#sel_specialist_budget option:selected").val();
            var nextelem = $("#sel_specialist_budget + input" );
            var qtyelem = $("#sel_specialist_budget + input + input" );
            var totalelem = $("#sel_specialist_budget + input + input + input" );
            var prevelem = $("#sel_specialist_budget" ).prev();
            var specialist_rate = nextelem.val();
            var specialist_total = totalelem.val();

            var thisvalue = $("#sel_specialist_markup_budget option:selected").val();
            var nextelem = $("#sel_specialist_markup_budget + input" );
            var qtyelem = $("#sel_specialist_markup_budget + input + input" );
            var totalelem = $("#sel_specialist_markup_budget + input + input + input" );
            var prevelem = $("#sel_specialist_markup_budget" ).prev();
            var specialist_markup_rate = nextelem.val();
            var specialist_markup_total = totalelem.val();

            var thisvalue = $("#sel_other_budget option:selected").val();
            var nextelem = $("#sel_other_budget + input" );
            var qtyelem = $("#sel_other_budget + input + input" );
            var totalelem = $("#sel_other_budget + input + input + input" );
            var prevelem = $("#sel_other_budget" ).prev();
            var other_rate = nextelem.val();
            var other_total = totalelem.val();

            var total_rates =parseFloat(parseFloat(mat_rate)+parseFloat(matmarkup_rate)+parseFloat(lab_rate)+parseFloat(transport_rate)+parseFloat(healthsafety_rate)+parseFloat(overheads_rate)+parseFloat(specialist_rate)+parseFloat(specialist_markup_rate)+parseFloat(other_rate))
                var total_totals =parseFloat(parseFloat(mat_total)+parseFloat(matmarkup_total)+parseFloat(lab_total)+parseFloat(transport_total)+parseFloat(healthsafety_total)+parseFloat(overheads_total)+parseFloat(specialist_total)+parseFloat(specialist_markup_total)+parseFloat(other_total))
                $("#cont_check_budget_percent").val(total_rates);
            $("#cont_check_budget_total").val(total_totals);
            //console.log($("#cont_total_budget").val());
            //console.log($("#cont_total_budget").val()< total_rates);
            if ($("#cont_total_budget").val() < total_rates){
                $("#button_edit_budget").hide();
            }
            else{

                $("#button_edit_budget").show();
            }
        }
        $("#button_edit_budget").click(function(e){
            var formserial = $("#cont_main_budget_seperated").serialize();
            //console.log(formserial);
            var uniqid1 = Math.random()
            var selectedbudgetid = $("#activebudgetitemid").val();
        var jrkqxhr = $.post("/mngntcont/ajaxeditbudgetitem/"+uniqid1+"/"+selectedbudgetid+"?"+formserial, function(data1,status1,xhr1) {
            $("#button_edit_budget").hide();
        });
        e.preventDefault();
        });
    }
    function callback_after_main_sow(){
        //$("#contractheader").hide();
        $("#button_space_sow").append( "<button id='add_sow_to_budgets'>Add SOW To Budgets</button>" );
        $( "#add_sow_to_budgets" ).click(function() {
            //console.log("SOW Here");
            var activejcno = $("#activesiteid").val();
            var uniqid1 = Math.random()
            jrkqxhr = $.post("/contractscont/ajaxContractScopeAttachToBudgetContract/"+uniqid1+"/"+activejcno, function(data1,status1,xhr1) {
                var activejcno = $("#activesiteid").val();
                $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
                $("#contract_overview_tabs").tabs('select', 4);
            });
        });
        $("#table_contracts_sow").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                var selectedbudgetid = col0text;
            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#table_contracts_sow").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                if ($(this).index() == 7){ 
                    //console.log("edit pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var scopeitem = $(this).parent().find("td").eq(1).text();
                    var scopedescription = $(this).parent().find("td").eq(2).html();
                    var scopeunit = $(this).parent().find("td").eq(3).html();
                    var scopeqty = $(this).parent().find("td").eq(4).html();
                    var scopeprice = $(this).parent().find("td").eq(5).html();
                    var scopetotal = $(this).parent().find("td").eq(6).html();
                    //var uniqid = Math.random()
                    $( "#dialog_editcontractscope").find("input").eq(0).val(alltrim(scopeid));
                    $( "#dialog_editcontractscope").find("input").eq(1).val(alltrim(scopeitem));
                    $( "#dialog_editcontractscope").find("input").eq(2).val(alltrim(scopedescription));
                    $( "#dialog_editcontractscope").find("input").eq(3).val(alltrim(scopeunit));
                    $( "#dialog_editcontractscope").find("input").eq(4).val(alltrim(scopeqty));
                    $( "#dialog_editcontractscope").find("input").eq(5).val(alltrim(scopeprice));
                    $( "#dialog_editcontractscope").find("input").eq(6).val(alltrim(scopetotal));
                    $("#activescopeid").val(scopeid);
                    $("#dialog_editcontractscope").dialog("open");
                };
                if ($(this).index() == 8){ 
                    //console.log("delete pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random()
                        $(this).parent().remove();
                    var jqxhr = $.post("/contractscont/ajaxDeleteContractScope/"+uniqid+"/"+scopeid, function(data) {
                        var activejcno = $("#activesiteid").val();
                        $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
                    })
                };
                if ($(this).index() == 9){ 
                    //console.log("notes pressed");
                    var scopeid = $(this).parent().find("td").eq(0).html();
                    var uniqid = Math.random()
                        var jqxhr = $.post("/contractscont/ajaxAttachSingleScopeToBudgets/"+uniqid+"/"+String(scopeid), function(data) {
                            var activejcno = $("#activesiteid").val();
                            $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
                            $("#contract_overview_tabs").tabs('select', 4);
                        })
                };
            };
        });
        $("#deletecontractscope").click(function(e){
            //console.log("Got Here")
            var uniqid = Math.random()
            var jqxhr = $.post("/contractscont/ajaxDeleteContractScope/"+uniqid+"/"+scopeid, function(data) {
                var activejcno = $("#activesiteid").val();
                $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
                //loadXMLBQItems(scopeid)
                //$("#grv_items").empty()
                //$("#grv_details").load("/logisticscont/grv_order_one_details/"+parseInt(activepo),callback_load_order_items_grv);
            })
        });
        $("#addcontractscope").click(function(e){
            //console.log("Got Here")
            $("#dialog_newcontractscope").dialog("open");
            var uniqid = Math.random()
        });
    }
    function callback_after_main_poitems(){
        //$("#contractheader").hide();
        $("#button_space_orderitems").append( "<button id='add_orderitems_to_budgets'>Add PO Items To Budgets</button>" );
        $("#button_space_orderitems").append( "<button id='add_orderitems_to_scope'>Add PO Items To Scope</button>" );
        $( "#add_orderitems_to_budgets" ).click(function() {
            //console.log("SOW Here");
            var activejcno = $("#activesiteid").val();
            var uniqid1 = Math.random()
            jrkqxhr = $.post("/contractscont/ajax3yrOrderItemsAttachToBudgetContract/"+uniqid1+"/"+activejcno, function(data1,status1,xhr1) {
                var activejcno = $("#activesiteid").val();
                $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
                $("#contract_overview_tabs").tabs('select', 4);
            });
        });
        $( "#add_orderitems_to_scope" ).click(function() {
            //console.log("SOW Here");
            var uniqid1 = Math.random()
            var activejcno = $("#activesiteid").val();
        jrkqxhr = $.post("/contractscont/ajax3yrOrderItemsAttachToScopeContract/"+uniqid1+"/"+activejcno, function(data1,status1,xhr1) {
            var activejcno = $("#activesiteid").val();
            $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
            $("#contract_overview_tabs").tabs('select', 3);
        });
        });
    }
    function debug_easy_calls() {
        $("#header").hide();
        $("body").css('width','1900px');
        $("#myjistconsole_tabs").css('height','800px');
        $("#contract_overview_tabs").css('height','800px').tabs('refresh');
        $("#buying_console_tabs").css('height','800px');
        $("#grv_console_tabs").css('height','800px');
    }
    //debug_easy_calls() 
    $( "#dialog_editbudgets" ).dialog({
        autoOpen: false,
    height: 580,
    width: 550,
    modal: true,
    buttons: {
        "Edit Budget": function() {
            var bValid = true;
            //allscopeFields.removeClass( "ui-state-error" );
            //bValid = bValid && checkLength( editscopename, "site name", 3, 80 );
            //bValid = bValid && checkLength( email, "email", 6, 80 );
            //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
            if ( bValid ) {
                var uniqid = Math.random()
        var formserial = $("#edit_budgets_form").serialize();
    var jrkqxhr = $.post("/mngntcont/ajaxeditbudgetdescription/"+uniqid+"?"+formserial, function(data1,status1,xhr1) {
        var activejcno = $("#activesiteid").val();
        $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
    });
    $( this ).dialog( "close" );
    $( this ).find('input').val('');
            }
        },
        Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
    },
    close: function() {
               alleditbudgetFields.val( "" ).removeClass( "ui-state-error" );
           }
    });
    $( "#dialog_newbudget" ).dialog({
        autoOpen: false,
        height: 580,
        width: 550,
        modal: true,
        buttons: {
            "New Budget": function() {
                var bValid = true;
                //allscopeFields.removeClass( "ui-state-error" );
                //bValid = bValid && checkLength( editscopename, "site name", 3, 80 );
                //bValid = bValid && checkLength( email, "email", 6, 80 );
                //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                if ( bValid ) {
                    var uniqid = Math.random()
        var activejcno = $("#activesiteid").val();
    var formserial = $("#new_budgets_form").serialize();
    var jrkqxhr = $.post("/mngntcont/ajaxnewbudgetcontract/"+uniqid+"/"+activejcno+"?"+formserial, function(data1,status1,xhr1) {
        var activejcno = $("#activesiteid").val();
        $("#ui-tabs-Budgets").load("/mngntcont/ajaxgetcontractbudgetitems/"+activejcno,callback_after_main_budget);
    });
    $( this ).find('input').val('');
    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                        $( this ).find('input').val('');
                        $( this ).dialog( "close" );
                    }
        },
        close: function() {
                   allnewbudgetFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $( "#dialog_newcontractscope" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "New Contract Scope": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    var activejcno = $("#activesiteid").val();
                    var formserial = $("#new_contracts_scope_form").serialize();
                    var jqxhr = $.post("/contractscont/ajaxAddContractScope/"+uniqid+"/"+activejcno+"?"+formserial, function(data) {
                        var activejcno = $("#activesiteid").val();
                        $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
                    })
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
            },
        Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
        },
        close: function() {
                   allnewbudgetFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $( "#dialog_editcontractscope" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "Edit Contract Scope": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
        var activescopeno = $("#activescopeid").val();
    var formserial = $("#edit_contracts_scope_form").serialize();
    var jqxhr = $.post("/contractscont/ajaxEditContractScope/"+uniqid+"/"+activescopeno+"?"+formserial, function(data) {
        var activejcno = $("#activesiteid").val();
        $("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
    })
    $( this ).find('input').val('');
    $( this ).dialog( "close" );
                }
            },
        Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
        },
        close: function() {
                   //allnewbudgetFields.val( "" ).removeClass( "ui-state-error" );
               }
    });
    $("#button_search_supplier_name").click(function(e){
        //console.log("Clicked");
        e.preventDefault();
        thissupplier = $( "#search_supplier_name" ).val();
        $("#outputsupplier_search").load("/logisticscont/do_search_supplier/"+thissupplier);
        //$("#dialog_newbudget").dialog("open");
    });
    $("#btn_invoices_balances" ).click(function(event) {
        $("#output").load("/invoicingcont/do_search_invoices_balances",function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success")
            //alert("External content loaded successfully!");
            if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
        return false;
    });
    $("#btn_invoices_outstanding" ).click(function(event) {
        $("#output").load("/invoicingcont/do_search_invoices_unpaid",function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success")
            //alert("External content loaded successfully!");
            if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
        return false;
    });
    $("#combobox_points" ).change(function(event) {
        var elem = $("#combobox_points" ).val();
        //console.log(elem);
        $("#output").load("/mngntcont/ajax_invoices_per_point/"+elem,function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success")
            //alert("External content loaded successfully!");
            if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
        return false;
    });
    $("#combobox_wip" ).change(function(event) {
        var elem = $("#combobox_wip" ).val();
        //console.log(elem);
        //$("#output").load("/invoicingcont/toggleinvoicescontract/"+elem,function(responseTxt,statusTxt,xhr){
        $("#output").load("/invoicingcont/do_search_invoices_contracts?contract_name="+elem,function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success")
            //alert("External content loaded successfully!");
            if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
        return false;
    });
    $( "#budgetid" ).css("enable","False");
    $( "#budgetitem" ).css("width","300px");
    $( "#budgetdescription" ).css("width","400px");
    $( "#newscopedescription" ).css("width","400px");
    $( "#editcontractscopedescription" ).css("width","400px");
    $( "#editcontractscopeitem" ).css("width","300px");
    $( "#newscopeitem" ).css("width","300px");
    $( "#newbudgetid" ).css("enable","False");
    $( "#newbudgetitem" ).css("width","300px");
    $( "#newbudgetdescription" ).css("width","400px");
    $( "#editbudgetitem" ).css("width","300px");
    $( "#editbudgetdescription" ).css("width","400px");
    $( "#search_supplier_name" ).css("width","400px");
    function replaceforward2back(dataStr) {
        //console.log(dataStr.replace(/\//g, "-"));
        return dataStr.replace(/\//g, "-");
    };
    function alltrim(str) {
        return str.replace(/^\s+|\s+$/g, '');
    };
    });


    $(document).ready(function(){
        $( "#combobox_overview" ).combobox_jcno();
        $( "#combobox_completed" ).combobox_jcno();
        $( "#combobox_suppliers" ).combobox_suppliers();
        $( "#combobox_contracts_req" ).combobox_contracts_req();
        //Load the CCTV Model Stuff
        $("#btn_size_cams").click(function(e){
            console.log("pressed")
            var docwidth = $(window).width();
        console.log(docwidth)
            var camwidth = docwidth / 3 
            console.log(camwidth)
            var camwidthstr = (camwidth -155) + 'px'
            $("#imgages_sortable").css("width",docwidth);
        $("#imgages_sortable img").css("width",camwidthstr);

        });
    });
