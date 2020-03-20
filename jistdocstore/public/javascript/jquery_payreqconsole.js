//Handels the payment requisition pages
//Dec 2012-12-31
$(function(){
    $( "#payreq_tabs" ).tabs({ 
        heightStyle: "fill", 
        beforeLoad: function( event, ui ) {
                    ui.jqXHR.error(function() {
                        ui.panel.html("Couldn't load this tab." + "Its you or the program.... Try Again." );
                    });
                },
        spinner: "<img src ='/images/ui-anim_basic_16x16.gif'></img>",
        load: function( event, ui ) {
            //$( "#grv_console_tabs" ).tabs("option","deactive", 2 );
            var VATRATE = 0.14
            $("#grv_back_button").click(function(){
                var selected = $("#payreq_tabs").tabs('option', 'selected');
                $("#payreq_tabs").tabs('remove', selected);
                $("#payreq_tabs").tabs('select', selected - 1);
            });
             // close icon: removing the tab on click
            $( "#payreq_tabs span.ui-icon-close" ).live( "click", function() {
                var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
                $( "#" + panelId ).remove();
                $("#payreq_tabs").tabs( "refresh" );
            });
             // actual addTab function: adds new tab using the input from the form above
            function addTab(jcno,index) {
                var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>",
                    tabCounter = 2;
                var label = "JCNo " + jcno,
                    id = "ui-tabs-JCContract",
                    li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) );
                    //tabContentHtml = tabContent.val() || "Tab " + tabCounter + " content.";
                //$("#payreq_tabs").find( ".ui-tabs-nav" ).append( li );
                //$("ul li:eq(1)").after($("<li>Pink Panther</li>"));
                $("#payreq_tabs").find( ".ui-tabs-nav li:eq(1)" ).after( li );
                //$("#payreq_tabs").append( "<div id='" + id + "'></div>" );
                tabCounter++;
                //$("#contract_status_update").load("/contractscont/ajaxsitescontractstatusupdate/"+parseInt(jcno));
                //$("#payreq_tabs").tabs( "refresh" );
                //var thislen = $("#payreq_tabs").tabs( "length" );
                $("#payreq_tabs").tabs('select', 2);
            }
            $("#tbl_pay_reqs_notapproved").delegate('tr','mouseover mouseleave click',function(e) {
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
            $("#tbl_pay_reqs_notapproved").delegate('td','click',function(e){
                  if ($(this).parent().index() != 0){ 
                      var totalincl = $(this).parent().find("td").eq(4).html();
                      if ($(this).index() == 6){ 
                          //$(this).attr('flipped','flipped');
                          //var staff_face = $("#staff_face_pic");
                          //rotate_and_flip(staff_face,90);
                      };
                      if ($(this).index() == 7){ 
                            //console.log("notes pressed");
                            var uniqid = Math.random()
                            var scopeid = $(this).parent().find("td").eq(0).html();
                            var jqxhr = $.post("/accountscont/toggle_payreq_approved?payreqid="+parseInt(scopeid), function(data) {
                                //myuser = $("#activemyuser").val();
                                //$("#ui-tabs-MyPOReqs").load("/logisticscont/purchase_reqs_items_per_user/"+myuser)
                                $("#payreq_tabs").tabs("select",5)
                                return false;
                                })
                      };
                      if ($(this).index() == 8){ 
                            var activesplitreqid = $(this).parent().find("td").eq(0).html();
                            $("#activesplitreqid").val(activesplitreqid);
                            $("#split_req_total_incl").val(alltrim(totalincl)); 
                            $( "#split_req_must_pay_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                            $( "#dialog_pay_req_split_payment" ).dialog("open");
                            $(this).addClass("hover");
                      };
                      if ($(this).index() == 9){ 
                            var activereqid = $(this).parent().find("td").eq(0).html();
                            $(this).addClass("hover");
                            $("#payreq_edit").load("/accountscont/get_edit_paymentreq?payreqid="+parseInt(activereqid),function(responseTxt,statusTxt,xhr){
                                $("#payreq_edit").show()
                                //$( "#pay_req_date_edit" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                                //$( "#pay_req_must_pay_edit" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                                $( "#pay_req_description_edit" ).css("width","450px");
                                $("#button_do_add_payreq_edit").click(function(){
                                    var formserial = $("#frm_payreq_edit").serialize();
                                    var jqxhr = $.post("/accountscont/save_edit_payreq?"+formserial, function(data) {
                                        clear_form_elements("#frm_payreq_edit")
                                        $("#add_new_payee").hide();
                                        var selected = $("#payreq_tabs").tabs('option', 'selected');
                                        $("#payreq_tabs").tabs('select', selected - 1);
                                        $("#payreq_tabs").tabs('select', selected);
                                    });
                                    return false;
                                });
                                $("#button_do_cancel_payreq_edit").click(function(){
                                    clear_form_elements("#frm_payreq_edit")
                                    $("#frm_payreq_edit").hide();
                                    var selected = $("#payreq_tabs").tabs('option', 'selected');
                                    $("#payreq_tabs").tabs('select', selected - 1);
                                    $("#payreq_tabs").tabs('select', selected);
                                    return false;
                                });
                                return false;
                            });
                            //$( "#split_req_must_pay_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                            //$(this).addClass("hover");
                      };
                  };
            });
            $("#tbl_pay_reqs_unpaid_approved").delegate('tr','mouseover mouseleave click',function(e) {
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
            $("#tbl_pay_reqs_unpaid_approved").delegate('td','click',function(e){
                  if ($(this).parent().index() != 0){ 
                      if ($(this).index() == 7){ 
                            //console.log("notes pressed");
                            var scopeid = $(this).parent().find("td").eq(0).html();
                            var uniqid = Math.random()
                            var jqxhr = $.post("/accountscont/toggle_payreq_approved?payreqid="+parseInt(scopeid), function(data) {
                                $("#payreq_tabs").tabs("select",4)
                                return false;
                                })
                      };
                      if ($(this).index() == 8){ 
                            var activereqid = $(this).parent().find("td").eq(0).html();
                            $("#activereqid").val(alltrim(activereqid));
                            $( "#dialog_payreq_set_paymentdate" ).dialog("open");
                      };
                  };
            });
            $(".tblpaymentlist").delegate('tr','mouseover mouseleave click',function(e) {
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
            $(".tblpaymentlist").delegate('td','click',function(e){
                  if ($(this).parent().index() != 0){ 
                      if ($(this).index() == 12){ 
                            var reqid = $(this).parent().find("td").eq(0).html();
                            var uniqid = Math.random()
                            var jqxhr = $.post("/accountscont/set_req_payment_unpaid?payreqid="+parseInt(reqid), function(data) {
                                var selected = $("#payreq_tabs").tabs('option', 'selected');
                                $("#payreq_tabs").tabs('select', selected - 1);
                                $("#payreq_tabs").tabs('select', selected);
                                return false;
                                })
                      };
                  };
            });
            $(".paymentreq_paid").click(function(){
                console.log($(this).attr('value'));
                var thisvalue = alltrim($(this).attr('value'));
                var jqxhr = $.post("/accountscont/set_req_paymentpaid?&payreqdate="+thisvalue, function(data) {
                    var selected = $("#payreq_tabs").tabs('option', 'selected');
                    $("#payreq_tabs").tabs('select', selected - 1);
                    $("#payreq_tabs").tabs('select', selected);
                    
                });
            });
        }, 
        
        disable: function(event,ui){
            console.log("Disable pressed");
       },
       add: function(event,ui){
            console.log("Tab Added");
            $("#payreq_tabs").tabs('select', '#' + ui.panel.id);
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
    var VATRATE = 0.14
    $( "#dialog_pay_req_split_payment" ).dialog({
        autoOpen: false,
        height: 270,
        width: 650,
        modal: true,
        title: 'Split This Payment',
        buttons: {
            "Split Payment": function() {
                var bValid = true;
                //allsiteFields.removeClass( "ui-state-error" );
                //bValid = bValid && checkLength( sitename, "site name", 3, 120 );
                //bValid = bValid && checkLength( email, "email", 6, 80 );

                //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );

                if ( bValid ) {
                    var uniqid = Math.random()
                    var activereqsplitid = $("#activesplitreqid").val();
                    var formserial = $("#dialog_pay_req_split_payment").serialize();
                    var jqxhr = $.post("/accountscont/do_split_payment_req_unapproved"+"?"+formserial+"&payreqid="+activereqsplitid, function(data) {
                            var selected = $("#payreq_tabs").tabs('option', 'selected');
                            $("#payreq_tabs").tabs('select', selected - 1);
                            $("#payreq_tabs").tabs('select', selected);
                        })
                    clear_form_elements("#dialog_pay_req_split_payment");
                    $("#tbl_pay_reqs_notapproved").find('td').removeClass('hover');
                    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                //$( this ).find('input').val('');
                clear_form_elements("#dialog_pay_req_split_payment")
                $("#tbl_pay_reqs_notapproved").find('td').removeClass('hover');
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            //allsiteFields.val( "" ).removeClass( "ui-state-error" );
        }
    });
    $( "#dialog_payreq_set_paymentdate" ).dialog({
        autoOpen: false,
        height: 230,
        width: 350,
        modal: true,
        title: 'Set Payment Date',
        buttons: {
            "Set Date": function() {
                var bValid = true;
                //allsiteFields.removeClass( "ui-state-error" );
                //bValid = bValid && checkLength( sitename, "site name", 3, 120 );
                //bValid = bValid && checkLength( email, "email", 6, 80 );

                //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                
                if ( bValid ) {
                    var uniqid = Math.random()
                    var activereqid = $("#activereqid").val();
                    var formserial = $("#dialog_payreq_set_paymentdate").serialize();
                    var jqxhr = $.post("/accountscont/set_req_paymentdate?payreqid="+alltrim(activereqid)+"&"+formserial, function(data) {
                            $("#payreq_tabs").tabs('load', 5);
                    });
                    clear_form_elements("#dialog_payreq_set_paymentdate");
                    //$("#tbl_pay_reqs_notapproved").find('td').removeClass('hover');
                    $( this ).dialog( "close" );
                }
            },
            Cancel: function() {
                //$( this ).find('input').val('');
                clear_form_elements("#dialog_payreq_set_paymentdate")
                //$("#tbl_pay_reqs_notapproved").find('td').removeClass('hover');
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            //allsiteFields.val( "" ).removeClass( "ui-state-error" );
        },
        create: function(){
            $( "#payreq_paymentdate" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        }
    });
    $("#split_payment_percent").change(function(){
        //$pay_req_qty = $("#pay_req_qty");
        $balance = $("#split_req_total_incl_balance");
        $paynow = $("#split_req_total_incl_paynow");
        $split_incl = $("#split_req_total_incl");
        $percent = $("#split_payment_percent");
        var percentval = parseFloat($split_incl.val())*parseFloat($percent.val()/100);
        $paynow.val(percentval.toFixed(2));
        var thistotal = parseFloat($split_incl.val()-percentval)
        $balance.val(thistotal.toFixed(2));
    });
    $("#button_view_all_payees").click(function(){
        $("#div_payee_list").load("/accountscont/get_payees_list?switch=All",function(responseTxt,statusTxt,xhr){
            activate_table_payee();
            return false;
        });
    });
    $("#button_search_payee").click(function(){
        var searchphrase = $("#search_payeename").val()
        $("#div_payee_list").load("/accountscont/get_payees_list?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_payee();
            return false;
        });
    });
    $("#button_add_new_payee").click(function(){
        $("#add_new_payee").show();
    });
    $("#button_do_add_payee").click(function(){
        var formserial = $("#frm_new_payee").serialize();
        var jqxhr = $.post("/accountscont/do_save_new_payee?"+formserial, function(data) {
            clear_form_elements("#frm_new_payee")
            $("#add_new_payee").hide();
        });
        return false;
    });
    $("#button_do_cancel_new_payee").click(function(){
        clear_form_elements("#frm_new_payee")
        $("#add_new_payee").hide();
        return false;
    });
    function activate_table_payee() {
        $("#get_payee_table").delegate('tr','mouseover mouseleave click',function(e) {
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
        $("#get_payee_table").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                var payeeid = $(this).parent().find("td").eq(0).html();
                var sitename = $(this).parent().find("td").eq(2).html();
                var siteidindex = $(this).parent().index();
                $("#activepayeeid").val(alltrim(payeeid));
                if ($(this).index() == 15){ 
                    //console.log("edit pressed");
                    $("#payee_history").load("/accountscont/get_payee_history?payeeid="+alltrim(payeeid),function(data){
                        $("#payreq_tabs").tabs('select', 2);
                    }); 
                    $("#get_new_paymentreq").load("/accountscont/get_new_payment_req?payeeid="+alltrim(payeeid),function(data){
                        $("#pay_req_payee").css('width','450px')
                        $("#pay_req_description").css('width','450px')
                        $( "#pay_req_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#pay_req_promised_pay_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#pay_req_must_pay_date" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $( "#pay_req_date_paid" ).datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $("#pay_req_total_excl").css('text-align','right');
                        $("#pay_req_total_vat").css('text-align','right');
                        $("#pay_req_total_incl").css('text-align','right');
                        $("#pay_req_qty").css('text-align','right');
                        $("#pay_req_rate").css('text-align','right');
                        $("#pay_req_qty").change(function(){
                            $pay_req_qty = $("#pay_req_qty");
                            $pay_req_rate = $("#pay_req_rate");
                            $pay_req_total_excl = $("#pay_req_total_excl");
                            var thistotal = parseFloat($pay_req_qty.val())*parseFloat($pay_req_rate.val());
                            $pay_req_total_excl.val(thistotal.toFixed(2));
                            var thisvat = parseFloat($pay_req_total_excl.val())*parseFloat(VATRATE);
                            var thisincl = parseFloat($pay_req_total_excl.val())+parseFloat(thisvat);
                            $("#pay_req_total_vat").val(thisvat.toFixed(2));
                            $("#pay_req_total_incl").val(thisincl.toFixed(2));
                        });
                        $("#pay_req_rate").change(function(){
                            $pay_req_qty = $("#pay_req_qty");
                            $pay_req_rate = $("#pay_req_rate");
                            $pay_req_total_excl = $("#pay_req_total_excl");
                            var thistotal = parseFloat($pay_req_qty.val())*parseFloat($pay_req_rate.val());
                            $pay_req_total_excl.val(thistotal.toFixed(2));
                            var thisvat = parseFloat($pay_req_total_excl.val())*parseFloat(VATRATE);
                            var thisincl = parseFloat($pay_req_total_excl.val())+parseFloat(thisvat);
                            $("#pay_req_total_vat").val(thisvat.toFixed(2));
                            $("#pay_req_total_incl").val(thisincl.toFixed(2));
                        });
                        $("#pay_req_total_excl").change(function(){
                            $pay_req_qty = $("#pay_req_qty");
                            $pay_req_rate = $("#pay_req_rate");
                            $pay_req_total_excl = $("#pay_req_total_excl");
                            //var thistotal = parseFloat($pay_req_qty.val())*parseFloat(VATRATE);
                            //$("#pay_req_total_vat").val(thistotal.toFixed(2));
                        });
                        $("#btn_pay_req_new").click(function(){
                            var formserial = $("#pay_req_new_form").serialize();
                            var payeeid = alltrim($("#activepayeeid").val());
                            var jqxhr = $.post("/accountscont/do_save_new_payment_req?payeeid="+payeeid+"&"+formserial, function(data) {
                                $("#get_new_paymentreq").empty();
                                //myuser = $("#activemyuser").val();
                                //$("#ui-tabs-MyPOReqs").load("/logisticscont/purchase_reqs_items_per_user/"+myuser)
                                $("#payreq_tabs").tabs("select",4)
                                return false;
                            });
                            return false;
                        });
                    }); 
                };
                if ($(this).index() == 14){ 
                    $("#payee_list_edit").load("/accountscont/get_edit_payee?payee_id="+alltrim(payeeid),function(data){
                        $("#payee_editname").css('width','450px');
                        $("#address1_edit").css('width','350px');
                        $("#address2_edit").css('width','350px');
                        $("#address3_edit").css('width','350px');
                        $("#payee_list_edit").show();
                        $("#button_do_add_payee_edit").click(function(){
                            var formserial = $("#frm_new_payee_edit").serialize();
                            var jqxhr = $.post("/accountscont/save_edit_payee?"+formserial, function(data) {
                                clear_form_elements("#frm_new_payee_edit");
                                $("#payee_list_edit").hide();
                                $("#button_view_all_payees").trigger('click');
                            });
                            return false;
                        });
                        $("#button_do_cancel_new_payee_edit").click(function(){
                            clear_form_elements("#frm_new_payee_edit");
                            $("#payee_list_edit").hide();
                            return false;
                        });

                    });
                };
            };
        });
    };
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

    };
    function align_form_left_elements(ele) {
        $(ele).find(':input').each(function() {
            switch(this.type) {
                case 'password':
                case 'select-multiple':
                case 'select-one':
                case 'text':
                    $(this).css('position','relative');
                case 'textarea':
                    //$(this).val('');
                    break;
                case 'checkbox':
                case 'radio':
                    //this.checked = false;
            }
        });
    };
    function rotate_and_flip(ele,x){
         $(ele).css('transform', 'rotate('+ x +'deg) scaleX(-1)');
    };
    $("#payreq_tabs").css('height','600px').tabs('refresh');
    //$( "#pay_req_payee" ).combobox_req_payee().css("width","100px");
    $("#payreq_tabs").tabs('select', 1);
    $("#button_view_all_payees").button();
    $("#button_search_payee").button();
    $("#button_add_new_payee").button();
    //align_form_left_elements($("#pay_req_new_form"));
});


