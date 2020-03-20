//Handels the invoicing pages
//Dec 2012-12-31
$(function(){
    $( "#invoicing_tabs" ).tabs({ 
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
    $( "#startdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#enddate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#clientstartdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#clientenddate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#clientstartdatepayment" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#clientenddatepayment" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#paymentdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#edit_invoice_payment_form").hide();
    $("#button_get_invoices_dates").click(function(){
      var formserial = $("#startend_form").serialize();
      $( "#output_invoice_dates" ).load("/invoicingcont/do_search_invoices_dates?"+formserial,function(){
            return false;
      }); return false;
    });
    $("#clientbutton_get_invoices_dates").click(function(){
      var formserial = $("#clientstartend_form").serialize();
      clientname = $("#clientlist").val();
      clientname = clientname.replace(/\s/g, '+');
      $( "#clientoutput_invoice_dates" ).load("/invoicingcont/do_search_invoices_clients_dates"+"?"+formserial+"&clientname="+clientname,function(){
            return false;
      }); return false;
    });
    $("#clientbutton_get_payment_dates").click(function(){
      var formserial = $("#clientstartend_paymentform").serialize();
      clientname = $("#clientlistpayment").val();
      clientname = clientname.replace(/\s/g, '+');
      $( "#output_invoice_payments_made" ).load("/invoicingcont/ajax_get_payments_paid_date"+"?"+formserial+"&clientnamepayment="+clientname,function(){
            return false;
      }); return false;
    });
    $("#combo_invoicelist").change(function(){
      var $combo_invoicelist = $("#combo_invoicelist"); 
      var $invoiceid = $("#invoiceid"); 
      var selected_invoicelist = $combo_invoicelist.val();
      $invoiceid.val($combo_invoicelist.val());

      $( "#output_invoice_payment_form" ).load("/invoicingcont/ajax_get_payment_info/"+selected_invoicelist,function(){
        $("#tblpaymentlist").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var col0text = $(this).find("td").eq(0).html();
                var col2text = $(this).find("td").eq(2).html();
                var col3text = $(this).find("td").eq(3).html();
                var col4text = $(this).find("td").eq(4).html();
                $( "#invoice_payment_form").hide();
                $( "#edit_invoice_payment_form").show();
                $( "#edit_activepaymentid").val(alltrim(col2text));
                $( "#edit_paymentdate").val(alltrim(col3text));
                $( "#edit_paymentamount").val(alltrim(col4text));
            }else   {
                $(this).removeClass("hover");
            }
        });
        return false;
      }); return false;

    });
    $("#edit_button_add_new_payment").click(function(){
          var formserial_edit = $("#edit_invoice_payment_form").serialize();
          //console.log(formserial_edit);
          var jrkqxhr = $.post("/invoicingcont/save_edit_invoice_payment?"+formserial_edit, function(data1,status1,xhr1) {
                    $( "#invoice_payment_form").show();
                    $( "#edit_invoice_payment_form").hide();
                    $("#combo_invoicelist").trigger("change");
                  //return false;
                });
    return false; 
    });

    $("#edit_button_cancel_payment").click(function(){
        $( "#invoice_payment_form").show();
        $( "#edit_invoice_payment_form").hide();
        return false;
    });
    $("#button_add_new_payment").click(function(){
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

    function replaceforward2back(dataStr) {
        //console.log(dataStr.replace(/\//g, "-"));
        return dataStr.replace(/\//g, "-");
    };
    function alltrim(str) {
                return str.replace(/^\s+|\s+$/g, '');
    };
    //The production invoicing bit
    $("#clientbutton_get_invoices_all").click(function(){
        //var formserial = $("#startend_form").serialize();
        var clientname = $("#combobox_clients").val();
        $("#inv_client_details_div").hide();
        $("#button_create_new_invclient").hide();
        clientname = clientname.replace(/\s/g, '+');
        $( "#clientoutput_invoice_all_only" ).load("/invoicingcont/do_search_invoices_clients_only?clientname="+clientname,function(){
            $("#oldinvoiceselected").click(function(){
                var invid = $("#oldinvoiceselected").val();
                var contractid = $("#combobox_contractswip").val();
                if (contractid == ''){
                     $("#warningdiv").html("Choose A Contract First !!!!")
                     $("#warningdiv").fadeIn(2000,function(){
                        $("#warningdiv").fadeOut('slow')    
                     });
                    return false;
                };
                $( "#output_invoice_clients_form" ).load("/invoicingcont/get_invoice_client_info?invid="+alltrim(invid)+"&contractid="+alltrim(contractid),function(){
                    $("#inv_client_details_div").show();
                    $( "#inv_client_name" ).css("width","400px");
                    $( "#inv_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                    $("#button_new_invoice_old_info").click(function(){
                        var invdate = alltrim($("#inv_date").val());
                        var client = alltrim($("#inv_client_name").val());
                        var ordernumber = alltrim($("#order_number").val());
                        var contract = alltrim($("#jcno").val());
                        var add1 = alltrim($("#address_line1").val());
                        var add2 = alltrim($("#address_line2").val());
                        var add3 = alltrim($("#address_line3").val());
                        var vatno = alltrim($("#vat_number").val());
                        var delvToname = alltrim($("#delvToname").val());
                        var delvToadd1 = alltrim($("#delvToadd1").val());
                        var delvToadd2 = alltrim($("#delvToadd2").val());
                        var delvTocontperson = alltrim($("#delvTocontperson").val());
                        var delvToconttel = alltrim($("#delvToconttel").val());
                        if ($("#inv_date").val() == ''){return false;};
                        if ($("#inv_client_name").val() == ''){return false;};
                        var jrkqxhr = $.post("/invoicingcont/savenewinvoice?invdate="+invdate+"&contract="+contract+"&client="+client+"&ordernumber="+ordernumber, function(data1,status1,xhr1) {
                            $("#ivn_active_invoice").val(data1);
                            var jrkqxhr = $.post("/invoicingcont/savenewinvoice_clientdata?invoiceid="+data1+"&add1="+add1+"&add2="+add2+"&add3="+add3+"&vatno="+vatno+"&delvToname="+delvToname+"&delvToadd1="+delvToadd1+"&delvToadd2="+delvToadd2+"&delvTocontperson="+delvTocontperson+"&delvToconttel="+delvToconttel, function(data1,status1,xhr1) {
                                  doCreateNewInvoice();
                            });
                        });
                        $("#existing_client_data").hide();
                        $("#button_create_new_invclient").hide();
                        $("#button_new_invoice_old_info").hide();
                        $("#invbutton_get_contract_items").hide();
                        return false;
                    });
                });
            });
        });
    });
    $("#invbutton_get_contract_items").click(function(){
        var clientname = $("#combobox_contractswip").val();
        //console.log(clientname);
        var $itemstab = $("#ui-tabs-Invoicing-ContractItems");
        var $inv_per_contract = $("#ui-tabs-InvByContract");
        $("#ui-tabs-Invoicing-ContractItems").load("/invoicingcont/toggleorderitemsbalances/"+clientname,function(){
            $('#invoicing_tabs ul:first li:eq(2) a').text("Order Items For JCNo: "+clientname);
            $("#invoicing_tabs").tabs('select', 2);
        });
        $inv_per_contract.load("/invoicingcont/toggleinvoicescontract/"+clientname,function(){
            $('#invoicing_tabs ul:first li:eq(4) a').text("Invoices For JCNo: "+clientname);
            $("#tblinvoices_contract").delegate('tr','mouseover mouseleave click',function(e) {
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
                    $('#invoicing_tabs ul:first li:eq(5) a').text("Invoice: "+alltrim(col0text));
                    $("#invoicing_tabs").tabs('select', 5);
                    $("#inv_single_item_table").load("/invoicingcont/toggleinvoiceitems/"+alltrim(col0text),function(){
                            $("#invs_totalexcl_edit").css("text-align","right");
                            $("#invs_totalvat_edit").css("text-align","right");
                            $("#invs_totalincl_edit").css("text-align","right");
                            $("#ivn_price_edit").css("text-align","right");
                            $("#ivn_qty_edit").css("text-align","right");
                            $("#ivn_total_edit").css("text-align","right");
                            $("#ivn_item_edit").css("width","80px");
                            $("#ivn_description_edit").css("width","280px");
                            $("#ivn_active_invoice").val(alltrim(col0text));
                            $("#ivn_qty_edit").change(function(){
                                $inv_qty = $("#ivn_qty_edit");
                                $inv_price = $("#ivn_price_edit");
                                $inv_total = $("#ivn_total_edit");
                                var thistotal = parseFloat($inv_qty.val())*parseFloat($inv_price.val());
                                $inv_total.val(thistotal.toFixed(2));
                            });
                            $("#ivn_price_edit").change(function(){
                                $inv_qty = $("#ivn_qty_edit");
                                $inv_price = $("#ivn_price_edit");
                                $inv_total = $("#ivn_total_edit");
                                var thistotal = parseFloat($inv_qty.val())*parseFloat($inv_price.val());
                                $inv_total.val(thistotal.toFixed(2));
                            });
                            $("#button_change_sums_invoice").click(function(){
                                var formserial = $("#inv_new_totals_edit").serialize();
                                var invitemid = alltrim(col0text);
                                var jrkqxhr = $.post("/invoicingcont/savetotalsinvoice_data?"+formserial+"&ivn_invid_edit="+invitemid, function(data1,status1,xhr1) {
                                     clear_form_elements($("#inv_new_totals_edit"));
                                     $("#inv_single_item_table").empty();
                                     $("#dialog_invoice_item_edit").hide();
                                     $("#invbutton_get_contract_items").trigger("click");
                                     return false;
                                });
                                return false;
                                
                            });
                            $("#tblinv_single_item_table").delegate('tr','mouseover mouseleave click',function(e) {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    if (e.type == 'mouseover') {
                                        $(this).addClass("hover");
                                    } else if ( e.type == 'click' ) {
                                        var values = '';
                                        var tds = $(this).find('td');
                                        var colid = alltrim($(this).find("td").eq(0).html());
                                        var colitem = alltrim($(this).find("td").eq(1).html());
                                        var coldescription =alltrim( $(this).find("td").eq(2).html());
                                        var colunit =alltrim( $(this).find("td").eq(3).html());
                                        var colqty =alltrim( $(this).find("td").eq(4).html());
                                        var colprice =alltrim( $(this).find("td").eq(5).html());
                                        var coltotal =alltrim( $(this).find("td").eq(6).html());
                                        $("#dialog_invoice_item_edit").show();
                                        $("#inv_new_totals_edit").show();
                                        $("#ivn_invid_edit").val(alltrim(col0text));
                                        $("#ivn_id_edit").val(colid);
                                        $("#ivn_item_edit").val(colitem);
                                        $("#ivn_description_edit").val(coldescription);
                                        $("#ivn_unit_edit").val(colunit);
                                        $("#ivn_qty_edit").val(colqty);
                                        $("#ivn_price_edit").val(colprice);
                                        $("#ivn_total_edit").val(coltotal);
                                        // This is where the invoice item gets
                                        // edited
                                    }else {
                                        $(this).removeClass("hover");
                                    };
                            });

                    });
                }else {
                    $(this).removeClass("hover");
                }
            });
        });
    });
    $("#button_create_new_invclient").click(function(){
        var clientname = $("#combobox_contractswip").val();
        //console.log(clientname);
        var $itemstab = $("#ui-tabs-Invoicing-ContractItems");
        var $inv_per_contracttab = $("#ui-tabs-InvByContract");
        if (clientname == ''){
             $("#warningdiv").html("Choose A Contract First !!!!")
             $("#warningdiv").fadeIn(2000,function(){
                $("#warningdiv").fadeOut('slow')    
             });
            return false;
        };
        var $inv_jcno = $("#jcno_new");
        $inv_jcno.val(clientname);
        $("#inv_client_details_new").show();
        $("#existing_client_data").hide();
        $("#button_create_new_invclient").hide();
        $("#invbutton_get_contract_items").hide();
    });
    $("#invbutton_reset").click(function(){
        window.location.reload(true);
    });
    $("#button_edit_client_data").click(function(){
        $("#inv_client_details_edit").show()
        var $inv_c = $("#inv_client_details_edit")
        var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
        $("#inv_client_details_edit").load("/invoicingcont/get_invoice_client_edit_info?invid="+alltrim($ivn_active_invoice),function(){
            $("#button_edit_client_data_edit").click(function(){
                var formserial = $("#inv_client_details_form_edit").serialize();
                var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
                var jrkqxhr = $.post("/invoicingcont/saveeditinvoice_clientdata?"+formserial+"&invid="+$ivn_active_invoice, function(data1,status1,xhr1) {
                     clear_form_elements($("#inv_client_details_form_edit"));
                     //$("#inv_single_item_table").empty();
                     //$("#dialog_invoice_item_edit").hide();
                     //$("#invbutton_get_contract_items").trigger("click");
                     return false;
                });
                $("#inv_client_details_edit").hide()
                return false;
            });
        });
        return false;
    });
    $("#button_new_invoice_new_info").click(function(){
        //console.log("New Info");
        var invdate = alltrim($("#inv_date_new").val());
        var client = alltrim($("#inv_client_name_new").val());
        var ordernumber = alltrim($("#order_number_new").val());
        var contract = alltrim($("#jcno_new").val());
        var add1 = alltrim($("#address_line1_new").val());
        var add2 = alltrim($("#address_line2_new").val());
        var add3 = alltrim($("#address_line3_new").val());
        var vatno = alltrim($("#vat_number_new").val());
        var delvToname = alltrim($("#delvToname_new").val());
        var delvToadd1 = alltrim($("#delvToadd1_new").val());
        var delvToadd2 = alltrim($("#delvToadd2_new").val());
        var delvTocontperson = alltrim($("#delvTocontperson_new").val());
        var delvToconttel = alltrim($("#delvToconttel_new").val());
        if ($("#inv_date_new").val() == ''){return false;};
        if ($("#inv_client_name_new").val() == ''){return false;};
        var jrkqxhr = $.post("/invoicingcont/savenewinvoice?invdate="+invdate+"&client="+client+"&ordernumber="+ordernumber+"&contract="+contract, function(data1,status1,xhr1) {
            $("#ivn_active_invoice").val(data1);
            var jrkqxhr = $.post("/invoicingcont/savenewinvoice_clientdata?invoiceid="+data1+"&add1="+add1+"&add2="+add2+"&add3="+add3+"&vatno="+vatno+"&delvToname="+delvToname+"&delvToadd1="+delvToadd1+"&delvToadd2="+delvToadd2+"&delvTocontperson="+delvTocontperson+"&delvToconttel="+delvToconttel, function(data1,status1,xhr1) {
                 doCreateNewInvoice();
            });
        });
        $("#button_new_invoice_new_info").hide();
        return false;
    });
    $("#button_add_to_invoice_items_edit").click(function(){
        var formserial = $("#form_invoice_item_edit").serialize();
        var jrkqxhr = $.post("/invoicingcont/saveeditinvoice_data?"+formserial, function(data1,status1,xhr1) {
             clear_form_elements($("#form_invoice_item_edit"));
             $("#inv_single_item_table").empty();
             $("#dialog_invoice_item_edit").hide();
             $("#invbutton_get_contract_items").trigger("click");
             return false;
        });
        return false;
    });
    $("#button_add_new_to_invoice_items_edit").click(function(){
        var formserial = $("#form_invoice_item_edit").serialize();
        var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
        var jrkqxhr = $.post("/invoicingcont/saveaddinvoiceitem_data?"+formserial+"&invid="+$ivn_active_invoice, function(data1,status1,xhr1) {
             clear_form_elements($("#form_invoice_item_edit"));
             $("#inv_single_item_table").empty();
             $("#dialog_invoice_item_edit").hide();
             $("#invbutton_get_contract_items").trigger("click");
             return false;
        });
        return false;
    });
    $("#button_delete_item_data").click(function(){
        var formserial = $("#form_invoice_item_edit").serialize();
        var jrkqxhr = $.post("/invoicingcont/savedeleteinvoice_data?"+formserial, function(data1,status1,xhr1) {
             clear_form_elements($("#form_invoice_item_edit"));
             $("#inv_single_item_table").empty();
             $("#dialog_invoice_item_edit").hide();
             $("#invbutton_get_contract_items").trigger("click");
             return false;
        });
        return false;
    });
    function doCreateNewInvoice(){
        var $itemstab = $("#ui-tabs-Invoicing-ContractItems");
        var $inv_per_contracttab = $("#ui-tabs-InvByContract");
        $('#invoicing_tabs ul:first li:eq(3) a').text("Active New Invoice");
        $("#invoicing_tabs").tabs('select', 3);
        $("#tblinvoices_orderitems").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
                var values = '';
                var tds = $(this).find('td');
                var trs = $(this);
                var col0text = $(this).find("td").eq(0).html();
                var col1text = $(this).find("td").eq(1).html();
                var col2text = $(this).find("td").eq(2).html();
                //$('#invoicing_tabs ul:first li:eq(4) a').text("Invoice: "+alltrim(col0text));
                $("#invoicing_tabs").tabs('select', 3);
                //$("#ui-tabs-InvSingleView").load("/invoicingcont/toggleinvoiceitems/"+alltrim(col0text),function(){
                    //$('#invoicing_tabs ul:first li:eq(2) a').text("Order Items For JCNo: "+clientname);
                    //$("#invoicing_tabs").tabs('select', 2);
                //});
                trsclone = trs.clone();
                //tdrs = trsclone.find('td');
                trsclone.find("td:gt(7)").remove();
                trsclone.find("td:eq(1)").remove();
                //trsclone.find("td:eq(0)").remove();
                //trsclone.removeClass("hover");
                //$("#tblinv_new_items_info").append(trsclone);
                $( "#ivn_orderitemid" ).val(alltrim(trsclone.find("td:eq(0)").html()));
                $( "#ivn_item" ).val(alltrim(trsclone.find("td:eq(1)").html()));
                $( "#ivn_description" ).val(alltrim(trsclone.find("td:eq(2)").html()));
                $( "#ivn_unit" ).val(alltrim(trsclone.find("td:eq(3)").html()));
                $( "#ivn_qty" ).val(alltrim(trsclone.find("td:eq(4)").html()));
                $( "#ivn_price" ).val(alltrim(trsclone.find("td:eq(5)").html()));
                $( "#ivn_total" ).val(alltrim(trsclone.find("td:eq(6)").html()));

            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#tblinv_new_items_info").delegate('tr','mouseover mouseleave click',function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type == 'mouseover') {
                $(this).addClass("hover");
            } else if ( e.type == 'click' ) {
              if ($(this).index() != 0){ 
                var values = '';
                var tds = $(this).find('td');
                var trs = $(this);
                var col0text = $(this).find("td").eq(0).html();
                var col1text = $(this).find("td").eq(1).html();
                var col2text = $(this).find("td").eq(2).html();
                //$(this).remove();
                //$('#invoicing_tabs ul:first li:eq(4) a').text("Invoice: "+alltrim(col0text));
                //$("#invoicing_tabs").tabs('select', 3);
                //tdrs = trsclone.find('td');
              };

            }else   {
                $(this).removeClass("hover");
            }
        });
        $("#ivn_qty").change(function(){
            $inv_qty = $("#ivn_qty");
            $inv_price = $("#ivn_price");
            $inv_total = $("#ivn_total");
            var thistotal = parseFloat($inv_qty.val())*parseFloat($inv_price.val());
            $inv_total.val(thistotal.toFixed(2));
        });
        $("#ivn_price").change(function(){
            $inv_qty = $("#ivn_qty");
            $inv_price = $("#ivn_price");
            $inv_total = $("#ivn_total");
            var thistotal = parseFloat($inv_qty.val())*parseFloat($inv_price.val());
            $inv_total.val(thistotal.toFixed(2));
        });
        $("#button_add_to_invoice_items").click(function(){
            $ivn_orderitemid = alltrim($( "#ivn_orderitemid" ).val());
            $ivn_item =alltrim( $( "#ivn_item" ).val());
            $ivn_description =alltrim( $( "#ivn_description" ).val());
            $ivn_unit =alltrim( $( "#ivn_unit" ).val());
            $ivn_qty =alltrim( $( "#ivn_qty" ).val());
            $ivn_price =alltrim( $( "#ivn_price" ).val());
            $ivn_total =alltrim( $( "#ivn_total" ).val());
            if ($("#ivn_description").val() == '' && $("#ivn_total").val() == ''){return false;};
            var holder = "</td><td>"
            var holderR = "</td><td align='right'>"
            var trs = "<tr><td width='20px'>"+$ivn_orderitemid+holder+ $ivn_item +holder +$ivn_description+holder+$ivn_unit+holderR+$ivn_qty+holderR+$ivn_price+holderR+$ivn_total+"</td></tr>"
            $("#tblinv_new_items_info").append(trs);
            clear_form_elements($("#dialog_invoice_item"));
            $("#button_close_new_invoice").show();
            $("#print_new_invoice").show();
            var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
            //clientname = clientname.replace(/\s/g, '+');
            var jrkqxhr = $.post("/invoicingcont/savenewinvoice_data?orderitemsid="+$ivn_orderitemid+"&invid="+$ivn_active_invoice+"&item="+$ivn_item+"&description="+$ivn_description+"&unit="+$ivn_unit+"&qty="+$ivn_qty+"&price="+$ivn_price+"&total="+$ivn_total, function(data1,status1,xhr1) {
                  var valexcl = data1.split(",")[0]
                  var valvat = data1.split(",")[1]
                  var valincl = data1.split(",")[2]
                  $("#invs_totalexcl").val(valexcl);
                  $("#invs_totalvat").val(valvat);
                  $("#invs_totalincl").val(valincl);
                  return false;
            });
            return false;
        });
        $("#button_close_new_invoice").click(function(){
            var $valexcl = alltrim($("#invs_totalexcl").val());
            var $valvat = alltrim($("#invs_totalvat").val());
            var $valincl = alltrim($("#invs_totalincl").val());
            var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
            var jrkqxhr = $.post("/invoicingcont/savenewinvoice_totals?invid="+$ivn_active_invoice+"&excl="+$valexcl+"&vat="+$valvat+"&incl="+$valincl, function(data1,status1,xhr1) {
                var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
                //window.open('/invoicingcont/export_invoice_single_pdf/'+$ivn_active_invoice, '_blank');
                $("#invbutton_reset").trigger("click");
            });
            return false;
        });
        $("#print_new_invoice").click(function(){
            var $ivn_active_invoice = alltrim($("#ivn_active_invoice").val());
            window.open('/invoicingcont/export_invoice_single_pdf/'+$ivn_active_invoice, '_blank');
            //var jrkqxhr = $.get("/invoicingcont/export_invoice_single_pdf/"+$ivn_active_invoice, function(data1,status1,xhr1) {
                //return false;
            //});
        });
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
    $( "#inv_client_name_new" ).css("width","400px");
    $( "#ivn_description" ).css("width","300px");
    $( "#ivn_item" ).css("width","100px");
    $("#invoicing_tabs").tabs('select', 1);
    $( "#inv_date_new" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $( "#ivn_id_edit" ).css("width","80px");
    $( "#ivn_qty_edit" ).css("width","80px");
    //$("#button_print_new_invoice").button();
    $("#button_close_new_invoice").button();
    $("#button_add_to_invoice_items").button();
    $("#button_add_new_to_invoice_items_edit").button();

    //easy_debug routines
    //$("#combobox_contractswip").val(1787);
    //$("#invbutton_get_contract_items").trigger('click');
    //$("#combobox_clients").val("City of Cape Town");
    //$("#clientbutton_get_invoices_all").trigger('click');
    //$("#oldinvoiceselected").trigger('click');
    //$("#invoicing_tabs").tabs('select', 1);
    //$("#button_new_invoice_old_info").trigger('click');
    //$("#oldinvoiceselected").select(1);
});

