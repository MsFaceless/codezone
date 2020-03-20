$(document).ready(function() {
    $( "#ess_3yr_palisade_fencing_tabs" ).tabs({ 
        //heightStyle: "fill", 
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
       }
    });
    $( "#ess_3yr_palisade_fencing_production_tabs" ).tabs({ 
        //heightStyle: "fill", 
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
       }
    });
    $( "#ess_3yr_palisade_fencing_jjmc_tabs" ).tabs({ 
        //heightStyle: "fill", 
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
       }
    });
    /// Start of the estimating Section
    ///
    $( "#dialog_newsitescope" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "New Site Scope": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    var activejcno = $("#activesiteid").val();
                    var formserial = $("#new_sites_scope_form").serialize();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxAddSiteScope/"+alltrim(activejcno)+"?"+formserial, function(data) {
                        var activejcno = $("#activesiteid").val();
                        //$("#ui-tabs-SOW").load("/contractscont/ajaxsitescontractscopeofwork/"+activejcno,callback_after_main_sow);
                        var siteidindex = $("#activesiteidindex").val();
                        $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                        activate_table_sites();
                        //$("#div_site_scope").empty();
                        //$("#div_site_scope") .load("/est3yresspalisadecont/get_site_scope?siteid="+alltrim(activejcno),function(data){
                        // });
                        //$("#div_site_picture").empty();
                        //$("#div_site_picture") .load("/est3yresspalisadecont/get_default_pic?siteid="+alltrim(activejcno),function(data){
                        //});
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
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_editsitescope" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "Edit Site Scope": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                var activescopeno = $("#activescopeid").val();
                var formserial = $("#edit_sites_scope_form").serialize();
                var activejcno = $("#activesiteid").val();
                //$("#palisade_pics") .load("/est3yresspalisadecont/get_photos_by_site?siteid="+alltrim(activesiteid),function(data){
                //});
                var jqxhr = $.post("/est3yresspalisadecont/ajaxEditSiteScope/"+alltrim(activescopeno)+"?"+formserial, function(data) {
                    var activejcno = $("#activesiteid").val();
                    //$("#div_site_scope").empty();
                    var siteidindex = $("#activesiteidindex").val();
                    $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    activate_table_sites();
                    //$("#div_site_scope") .load("/est3yresspalisadecont/get_site_scope?siteid="+alltrim(activejcno),function(data){
                     //});

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
                    $( this ).find('input').val('');
               }
    });
    $("#button_view_all_sites_palisade").button();
    $("#button_search_site_description_palisade").button();
    $("#button_search_site_name_palisade").button();
    $("#button_add_new_est_site_palisade").button();
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
    $("#button_view_all_sites_palisade").click(function(){
        $("#div_est_sites").load("/est3yresspalisadecont/get_estimate_sites?switch=All",function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_search_site_name_palisade").click(function(){
        var searchphrase = $("#search_sitename_palisade").val()
        $("#div_est_sites").load("/est3yresspalisadecont/get_estimate_sites?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_search_site_description_palisade").click(function(){
        var searchphrase = $("#search_sitedescription_palisade").val()
        $("#div_est_sites").load("/est3yresspalisadecont/get_estimate_sites?switch=SearchArea&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_add_new_est_site_palisade").click(function(){
        $("#estimate_newsite").show();
    });
    $("#button_do_add_new_site_palisade").click(function(){
        var formserial = $("#frm_est_new_site").serialize();
        var jqxhr = $.post("/est3yresspalisadecont/save_new_estimate_sites?"+formserial, function(data) {
            clear_form_elements($("#frm_est_new_site"));
            $("#estimate_newsite").hide();
            $("#button_view_all_sites_palisade").trigger("click");
            return false;
        });
            return false;
    });
    $("#button_do_cancel_new_site_palisade").click(function(){
        clear_form_elements($("#frm_est_new_site"));
        $("#estimate_newsite").hide();
        return false;
    });
    function activate_table_sites() {
        $("#estimate_sites_table").delegate('tr','mouseover mouseleave click',function(e) {
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
        $("#estimate_sites_table").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                var siteid = $(this).parent().find("td").eq(0).html();
                var sitename = $(this).parent().find("td").eq(2).html();
                var siteidindex = $(this).parent().index();
                $("#activesiteid").val(siteid);
                $("#activesiteidindex").val(siteidindex);
                $("#activesitename").val(sitename);
                if ($(this).index() == 9){ 
                    //console.log("edit pressed");
                    $("#estimate_editsite").load("/est3yresspalisadecont/get_edit_estimate_sites?siteid="+alltrim(siteid),function(data){
                        $("#estimate_editsite").show();
                        $("#button_do_cancel_edit_site_palisade").click(function(){
                            clear_form_elements($("#frm_est_new_site"));
                            $("#estimate_editsite").hide();
                            return false;
                        });
                        $("#button_do_edit_new_site_palisade").click(function(){
                            var formserial = $("#frm_edit_est_new_site").serialize();
                            var jqxhr = $.post("/est3yresspalisadecont/save_edit_estimate_sites?"+formserial, function(data) {
                                clear_form_elements($("#frm_edit_est_new_site"));
                                $("#estimate_editsite").hide();
                                $("#button_view_all_sites_palisade").trigger("click");
                                return false;
                            });
                                return false;
                        });
                    }); 
                };
                if ($(this).index() == 10){ 
                    $("#estimate_quote_list").load("/est3yresspalisadecont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                        $("#estimate_quote_items").empty();
                        $("#estimate_quote_items_edit").empty();
                        $("#activequoteid").val('');
                        $("#quote_list").delegate('tr','mouseover mouseleave click',function(e) {
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
                        $("#quote_list").delegate('td','click',function(e) {
                          //var index = $( "#quote_list td" ).index( this );
                          //result.append( " #" + ( index + 1 ) );
                          var thisquoteid = $(this).parent().find("td").eq(0).html();
                          var thisquoteindex = $(this).parent().index();
                          $("#activequoteid").val(thisquoteid);
                          $("#activequoteidindex").val(thisquoteindex);
                            $("#estimate_quote_items").load("/est3yresspalisadecont/get_estimate_quote_items?quoteid="+alltrim(thisquoteid),function(data){
                                //$("#estimate_quote_items").css("margin-left","16%");   //activate_table_sites();
                                $("#button_quote_create_scope").button();
                                $("#button_quote_create_scope").click(function(){
                                    $("#estimate_quote_scope").load("/est3yresspalisadecont/get_form_quote_scopes?siteid="+alltrim(siteid)+"&quoteid="+alltrim(thisquoteid),function(data){
                                        $("#save_quote_scope").button();
                                        $("#save_quote_scope").click(function(){
                                            //console.log("Got Here");
                                            var formserial = $("#frm_edit_quote_scope").serialize();
                                            var jqxhr = $.post("/est3yresspalisadecont/save_quote_scope?"+formserial, function(data) {
                                                    //clear_form_elements($("#frm_edit_quote_scope"));
                                                    $("#quote_scope_items").empty();
                                                    $("#quote_scope_items").hide();
                                                    $("#quote_list").find("tr").eq(thisquoteindex).find("td").trigger("click");
                                                    return false;
                                            });
                                             
                                            return false;
                                        });
                                        return false;
                                    });
                                });
                                $("#quote_items").delegate('tr','mouseover mouseleave click',function(e) {
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
                                $("#quote_items").delegate('td','click',function(e) {
                                    if ($(this).parent().index() != 0){ 
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        var thisitemindex = $(this).parent().index();
                                        if ($(this).index() == 6){ 
                                            $("#estimate_quote_items_edit").load("/est3yresspalisadecont/get_estimate_quote_items_edit?itemid="+alltrim(thisitemid),function(data){
                                                $("#edit_description").css("width","350px");
                                                $("#edit_quantity").focus();
                                                $( "#edit_quantity" ).change(function(e){
                                                    if ( $(this).val()){
                                                        var supp_price = $("#edit_price").val();
                                                        var supp_total = parseFloat(supp_price)*parseFloat($(this).val());
                                                        $( "#edit_total" ).val(supp_total.toFixed(2));
                                                    };
                                                });
                                                $( "#edit_price" ).change(function(e){
                                                    if ( $(this).val()){
                                                        var supp_qty = $("#edit_quantity").val();
                                                        var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
                                                        $( "#edit_total" ).val(supp_total.toFixed(2));
                                                    };
                                                });
                                                $( "#button_do_edit_quote_item" ).click(function(e){
                                                    var formserial = $("#frm_edit_est_quote_item").serialize();
                                                    var jqxhr = $.post("/est3yresspalisadecont/save_edit_estimate_item?itemid="+alltrim(thisitemid)+"&"+formserial, function(data) {
                                                            clear_form_elements($("#frm_edit_est_quote_item"));
                                                            $("#estimate_quote_items_edit").empty();
                                                            $("#quote_list").find("tr").eq(thisquoteindex).find("td").trigger("click");
                                                    });
                                                    return false;
                                                });
                                                $( "#button_do_cancel_edit_item" ).click(function(e){
                                                    $("#estimate_quote_items_edit").empty();
                                                    return false;
                                                });
                                            });
                                        };
                                        if ($(this).index() == 7){ 
                                            //console.log("Delete Pressed"+thisitemid);
                                            var jqxhr = $.post("/est3yresspalisadecont/ajaxdeletequoteitem?itemid="+alltrim(thisitemid),function(responseTxt,statusTxt,xhr){
                                                            $("#quote_list").find("tr").eq(thisquoteindex).find("td").trigger("click");
                                            });
                                        };
                                    };
                                });
                                $("#quote_scope_items").delegate('tr','mouseover mouseleave click',function(e) {
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
                                $("#quote_scope_items").delegate('td','click',function(e) {
                                    if ($(this).parent().index() != 0){ 
                                        var thisitemid = $(this).parent().find("td").eq(0).html();
                                        var thisitemindex = $(this).parent().index();
                                        var thisquoteindex = $("#activequoteidindex").val();
                                        if ($(this).index() == 4){ 
                                            var jqxhr = $.post("/est3yresspalisadecont/ajaxDeleteQuoteScope/"+alltrim(thisitemid), function(data) {
                                                $("#quote_list").find("tr").eq(thisquoteindex).find("td").trigger("click");

                                            });
                                        };
                                    };
                                });
                            });

                        });
                    });
                    $("#ess_3yr_palisade_fencing_tabs").tabs('select', 2);
                    $("#palisade_pics").load("/est3yresspalisadecont/get_photos_by_site?siteid="+alltrim(siteid),function(data){
                        $('.thumb_clicked').click(function() {
                            //console.log($(this));
                            var picpath = $(this).attr('value');
                            window.open('/est3yresspalisadecont/estimating_pic_viewer?fname='+picpath, '_blank');
                            return false;
                        });
                    });
                    $("#palisade_pics_default").empty();
                    $("#palisade_pics_default") .load("/est3yresspalisadecont/get_default_pic?siteid="+alltrim(siteid),function(data){
                    });
                    $("#div_site_scope").empty();
                    $("#div_site_scope") .load("/est3yresspalisadecont/get_site_scope?siteid="+alltrim(siteid),function(data){
                        $("#button_add_new_site_scope").button();
                        $("#button_add_new_site_scope").click(function(){
                            $("#dialog_newsitescope").dialog("open");
                        });
                        $("#site_scope_items").delegate('tr','mouseover mouseleave click',function(e) {
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
                        $("#site_scope_items").delegate('td','click',function(e){
                            var itemid = $(this).parent().find("td").eq(0).html();
                            var itemdescr = $(this).parent().find("td").eq(1).html();
                            var itemunit = $(this).parent().find("td").eq(2).html();
                            var itemqty = $(this).parent().find("td").eq(3).html();
                            if ($(this).parent().index() != 0){ 
                                if ($(this).index() == 4){ 
                                    $("#editsitescopeid").val(alltrim(itemid));
                                    $("#editsitescopedescription").val(alltrim(itemdescr));
                                    $("#editsitescopedescription").css('width','350px');
                                    $("#editsitescopeunit").val(alltrim(itemunit));
                                    $("#editsitescopeqty").val(alltrim(itemqty));
                                    $("#activescopeid").val(alltrim(itemid));
                                    $("#dialog_editsitescope").dialog("open");
                                };
                                if ($(this).index() == 5){ 
                                    $("#activesiteidindex").val(siteidindex);
                                    var jqxhr = $.post("/est3yresspalisadecont/ajaxDeleteSiteScope/"+alltrim(itemid), function(data) {
                                        $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                                        activate_table_sites;
                                    });
                                };
                            };
                        });
                    });
                    $("#div_site_picture").empty();
                    $("#div_site_picture") .load("/est3yresspalisadecont/get_default_pic?siteid="+alltrim(siteid),function(data){
                    });
                };
                if ($(this).index() == 19){ 
                };
            };
        });
    };
    $("#ess_3yr_palisade_fencing_tabs").tabs('select', 1);
    $("#button_do_add_new_quote_palisade").click(function(){
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
        var jqxhr = $.post("/est3yresspalisadecont/ajaxaddnewquotefull/"+alltrim(siteid),function(responseTxt,statusTxt,xhr){
            $("#estimate_quote_list").load("/est3yresspalisadecont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    activate_table_sites;
                });
            });
    });
    $("#button_do_add_new_quote_palisade_empty").click(function(){
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
        var jqxhr = $.post("/est3yresspalisadecont/ajaxaddnewquoteempty/"+alltrim(siteid),function(responseTxt,statusTxt,xhr){
            $("#estimate_quote_list").load("/est3yresspalisadecont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    activate_table_sites;
                });
            });
    });
    $("#button_show_all_quotes").click(function(){
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
            $("#estimate_quote_list_all").load("/est3yresspalisadecont/get_estimate_quote_list_all",function(data){
                $("#estimate_quote_list").hide();
                $("#estimate_quote_items_edit").hide();
                $("#estimate_quote_items").hide();
                $("#estimate_quote_list_all").show();
                $("#estimate_quote_list_all").css('overflow-y','scroll');
                $("#estimate_quote_list_all").css('height','600px');
                //$("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    //activate_table_sites;
            });
    });
    $("#boqlist_palisade").delegate('tr','mouseover mouseleave click',function(e) {
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
    $("#boqlist_palisade").delegate('td','click',function(e){
        if ($(this).parent().index() != 0){ 
            if ($(this).index() == 5){ 
                if ($("#activequoteid").val()){
                    var quoteidindex = $("#activequoteidindex").val();
                    var quoteid = $("#activequoteid").val();
                    var siteid = $("#activesiteid").val();
                    var siteidindex = $("#activesiteidindex").val();
                    var bqitemid = $(this).parent().find("td").eq(0).html();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxaddnewquote_oneitem/"+alltrim(quoteid)+"/"+alltrim(bqitemid),function(responseTxt,statusTxt,xhr){
                            //$("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                            $("#ess_3yr_palisade_fencing_tabs").tabs('select', 2);
                            $("#quote_list").find("tr").eq(quoteidindex).find("td").trigger("click");
                        //$("#estimate_quote_list").load("/est5yreskomfencingcont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                         //       activate_table_sites;
                          //  });
                    });

                }else{
                    $("#warningdiv").html("Choose an Existing Quote Or Create a New One!!!!");
                    $("#warningdiv").fadeIn(2000,function(){
                        $("#warningdiv").fadeOut('slow');    
                    });
                    return false;
                };
            };
        };
    });
    var jqueryuploader_palisade = $('#jquery-fine-uploader_palisade').fineUploader({
        request: {
                     endpoint: '/est3yresspalisadecont/estuploadfile'
                 },
        autoUpload: false,
        validation: {
            allowedExtensions: ['jpeg', 'jpg', 'gif', 'png'],
        sizeLimit: 5242880, // 5M = 5 * 1024 * 1024 bytes
        //sizeLimit: 51200, // 50 kB = 50 * 1024 bytes
        itemLimit: 5,
        },
        text: {
                  uploadButton: 'Add Pics To Upload List - Max 5'
              },
        editFilename:  true,
    }).on('submit',function(event,id,name){
        if ($("#activesiteid").val()){
            $(this).fineUploader('setParams',{
               picjcno : $("#activesiteid").val(),
               pictakenby: $("#pic_taken_by_user").val(), 
               picdate: alltrim($("#pic_date_taken").val()), 
               picdescription: alltrim($("#pic_description").val()), 
               picsubject: alltrim($("#pic_subject").val()) 
            });
        }else{
            $("#warningdiv").html("Choose an Existing Site Or Create a New One!!!!");
            $("#warningdiv").fadeIn(2000,function(){
                $("#warningdiv").fadeOut('slow');    
            });
            return false;
        };
    }).on('complete',function(event,id,name,response){
        var activesiteid = $("#activesiteid").val();
        $("#palisade_pics") .load("/est3yresspalisadecont/get_photos_by_site?siteid="+alltrim(activesiteid),function(data){
        });
        //console.log(response); 
    });
    $('#triggerUpload').click(function() {
        jqueryuploader_palisade.fineUploader('uploadStoredFiles');
        var formserial = $("#upload_data_form").serialize();
        return false;
    });
    $('#triggerClose').click(function() {
        close();
        return false;
    });
    $('#triggerReset').click(function() {
        jqueryuploader_palisade.fineUploader('reset');
        clear_form_elements($("#upload_data_form"));
        return false;
    });
    $('#pic_description').change(function(){
        $('#jquery-fine-uploader_palisade').show();
        $('#triggerUpload').show();
        $('#triggerReset').show();
        return false;
    });
    $("#button_do_add_new_quote_palisade").button();
    $("#button_do_add_new_quote_palisade_empty").button();
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
    /// End of the estimating Section
    /// Start of the production Section
    
    $("#button_view_all_contracts_palisade").button();
    $("#button_search_contract_description_palisade").button();
    $("#button_search_contract_area_palisade").button();
    $("#button_search_contract_name_palisade").button();
    $("#button_add_new_est_contract_palisade").button();
    $("#ess_3yr_palisade_fencing_production_tabs").tabs('select', 1);
    $( "#dialog_newstandarditems" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "New Contract Standard Item": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    //var activejcno = $("#activecontractid").val();
                    var formserial = $("#new_standard_list_form").serialize();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxAddStandardItem?"+formserial, function(data) {
                        window.location.reload();
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
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_editstandarditems" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "Edit Contract Standard Item": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    //var activejcno = $("#activecontractid").val();
                    var formserial = $("#edit_standard_list_form").serialize();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxEditStandardItem?"+formserial, function(data) {
                        window.location.reload();
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
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_new_site_requirements" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "New Contract  Item": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    //var activejcno = $("#activecontractid").val();
                    var formserial = $("#new_site_requirements_form").serialize();
                    var linkedid = $("#activelinkid").val();
                    var siteidindex = $("#activesiteidindex").val();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxAddSiteRequirement?"+formserial+"&linkid="+alltrim(linkedid), function(data) {
                        //window.location.reload();
                        //$("#estimate_contracts_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                        $("#estimate_item_list").load("/est3yresspalisadecont/get_site_requirements?linkid="+alltrim(linkedid),function(data){
                            $("#newlist_date_req").datepicker();
                            $("#newlist_date_req").datepicker( "option", "dateFormat", "yy-mm-dd" );
                        });
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
                    $( this ).find('input').val('');
               }
    });
    $( "#dialog_edit_site_requirements" ).dialog({
        autoOpen: false,
        height: 550,
        width: 450,
        modal: true,
        buttons: {
            "New Contract  Item": function() {
                var bValid = true;
                if ( bValid ) {
                    var uniqid = Math.random()
                    //var activejcno = $("#activecontractid").val();
                    var formserial = $("#new_site_requirements_form").serialize();
                    var linkedid = $("#activelinkid").val();
                    var siteidindex = $("#activesiteidindex").val();
                    var jqxhr = $.post("/est3yresspalisadecont/ajaxAddSiteRequirement?"+formserial+"&linkid="+alltrim(linkedid), function(data) {
                        //window.location.reload();
                        //$("#estimate_contracts_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                        $("#estimate_item_list").load("/est3yresspalisadecont/get_site_requirements?linkid="+alltrim(linkedid),function(data){
                            $("#newlist_date_req").datepicker();
                            $("#newlist_date_req").datepicker( "option", "dateFormat", "yy-mm-dd" );
                        });
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
                    $( this ).find('input').val('');
               }
    });
    $("#button_view_all_contracts_palisade").click(function(){
        $("#div_est_contracts").load("/est3yresspalisadecont/get_estimate_contracts_linked?switch=All",function(responseTxt,statusTxt,xhr){
            activate_table_contracts();
        });
    });
    $("#button_search_contract_name_palisade").click(function(){
        var searchphrase = $("#search_contractname_palisade").val()
        $("#div_est_contracts").load("/est3yresspalisadecont/get_estimate_contracts_linked?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_contracts();
        });
    });
    $("#button_search_contract_description_palisade").click(function(){
        var searchphrase = $("#search_contractdescription_palisade").val()
        $("#div_est_contracts").load("/est3yresspalisadecont/get_estimate_contracts_linked?switch=SearchArea&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_contracts();
        });
    });
    $("#button_search_contract_area_palisade").click(function(){
        var searchphrase = $("#search_contract_area_palisade").val()
        $("#div_est_contracts").load("/est3yresspalisadecont/get_estimate_contracts_linked?switch=SearchArea&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_contracts();
        });
    });
    $("#button_add_new_est_contract_palisade").click(function(){
        //$("#estimate_newcontract").show();
        $("#div_est_contracts").load("/est3yresspalisadecont/get_new_estimate_contract_link",function(responseTxt,statusTxt,xhr){
            $(".button_do_link").button();
            $("#id_jcno_dropdown").change(function(){
                var jcno = $(this).val();
                $("#booleancontractlinked").load("/est3yresspalisadecont/get_link_contract?id_jcno="+$(this).val(),function(responseTxt,statusTxt,xhr){;
                    $("#div_contract_data").load("/contractscont/ajaxsitescontractorderitems/"+jcno,function(responseTxt,statusTxt,xhr){;
                        $("#div_contract_scope_data").load("/contractscont/ajaxsitescontractscopeofwork/"+jcno,function(responseTxt,statusTxt,xhr){;

                        });

                    });
                });
            });
            $("#id_estsite_dropdown").change(function(){
                var siteid = $(this).val();
                var jcno = $("#id_jcno_dropdown").val();
                $("#booleanestsitelinked").load("/est3yresspalisadecont/get_link_estsite?id_estsite="+$(this).val(),function(responseTxt,statusTxt,xhr){;
                    $("#div_quote_data").load("/est3yresspalisadecont/get_site_quotelist_andquotes?siteid="+siteid,function(responseTxt,statusTxt,xhr){;
                            $(".button_contract_create_scope").button();
                            $(".button_contract_create_scope").click(function(){
                                varquoteid = $(this).attr('value')
                                var jqxhr = $.post("/est3yresspalisadecont/save_new_scope_to_jcno?quoteid="+varquoteid+"&siteid="+siteid+"&jcno="+jcno, function(data) {
                                    //clear_form_elements($("#frm_est_new_contract_link"));
                                    $("#estimate_newcontract").hide();
                                    $("#id_jcno_dropdown").trigger("change");
                                    return false;
                                });
                            });

                    });

                });
            });
            $("#button_do_add_new_site_link").click(function(){
                var formserial = $("#frm_est_new_contract_link").serialize();
                var jqxhr = $.post("/est3yresspalisadecont/save_new_estimate_contract_link?"+formserial, function(data) {
                    clear_form_elements($("#frm_est_new_contract_link"));
                    $("#estimate_newcontract").hide();
                    $("#button_cancel_new_site_link").trigger("click");
                    $("#button_view_all_contracts_palisade").trigger("click");
                    return false;
                });
                    return false;
            });
            $("#button_cancel_new_site_link").click(function(){
                $("#div_est_contracts").empty()
                $("#div_contract_data").empty()
                $("#div_quote_data").empty()
                $("#div_contract_scope_data").empty()
                return false;
            });
            activate_table_contracts();
        });
    });
    $("#button_do_cancel_new_contract_palisade").click(function(){
        clear_form_elements($("#frm_est_new_contract"));
        $("#estimate_newcontract").hide();
        return false;
    });
    $("#button_new_standarditem").click(function(){
        $("#dialog_newstandarditems").dialog("open");
    });
    $("#standardlist_palisade").delegate('tr','mouseover mouseleave click',function(e) {
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
    $("#standardlist_palisade").delegate('td','click',function(e){
        if ($(this).parent().index() != 0){ 
            if ($(this).index() == 6){ 
                var itemid = $(this).parent().find("td").eq(0).html();
                var descrip = $(this).parent().find("td").eq(1).html();
                var size = $(this).parent().find("td").eq(2).html();
                var length = $(this).parent().find("td").eq(3).html();
                var height = $(this).parent().find("td").eq(4).html();
                var weight = $(this).parent().find("td").eq(5).html();
                $("#editlistid").val(alltrim(itemid));
                $("#editlistdescription").val(alltrim(descrip));
                $("#editlistsize").val(alltrim(size));
                $("#editlistlength").val(alltrim(length));
                $("#editlistheight").val(alltrim(height));
                $("#editlistweight").val(alltrim(weight));
                $("#dialog_editstandarditems").dialog("open");
            };
        };
    });

    function activate_table_contracts() {
        $("#estimate_contracts_table").delegate('tr','mouseover mouseleave click',function(e) {
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
        $("#estimate_contracts_table").delegate('td','click',function(e){
            if ($(this).parent().index() != 0){ 
                var consoleid = $(this).parent().find("td").eq(0).html();
                var siteid = $(this).parent().find("td").eq(1).html();
                var sitejno = $(this).parent().find("td").eq(2).html();
                var siteidindex = $(this).parent().index();
                //console.log(siteidindex);
                $("#activesiteid").val(siteid);
                $("#activesiteidindex").val(siteidindex);
                $("#activejcno").val(sitejno);
                $("#activelinkid").val(consoleid);
                //$("#activesitename").val(sitename);
                if ($(this).index() == 9){ 
                    //console.log("edit pressed");
                    $("#estimate_editcontract").load("/est3yresspalisadecont/get_edit_estimate_contracts_link?siteid="+alltrim(siteid)+"&contractid="+alltrim(sitejno),function(data){
                        $("#estimate_editcontract").show();
                        $("#button_do_cancel_edit_contract_palisade").click(function(){
                            clear_form_elements($("#frm_est_new_contract"));
                            $("#estimate_editcontract").hide();
                            return false;
                        });
                        $("#button_do_edit_new_contract_palisade").click(function(){
                            var formserial = $("#frm_edit_est_new_contract").serialize();
                            var jqxhr = $.post("/est3yresspalisadecont/save_edit_estimate_contracts?"+formserial, function(data) {
                                clear_form_elements($("#frm_edit_est_new_contract"));
                                $("#estimate_editcontract").hide();
                                $("#button_view_all_contracts_palisade").trigger("click");
                                return false;
                            });
                                return false;
                        });
                    }); 
                };
                if ($(this).index() == 10){ 
                    $("#").show();
                    $("#palisade_pics_default").empty();
                    $("#div_site_scope").empty();
                    $("#div_site_picture").empty();
                    $("#div_jcno_scope").empty();
                    $("#div_jcno_despatch").empty();
                    $("#estimate_item_list").load("/est3yresspalisadecont/get_site_requirements?linkid="+alltrim(consoleid),function(data){
                        //$("#newlist_date_req").datepicker();
                        //$("#newlist_date_req").datepicker( "option", "dateFormat", "yy-mm-dd" );
                        $("#site_requirement_items").delegate('tr','mouseover mouseleave click',function(e) {
                            e.preventDefault();
                            if (e.type == 'mouseover') {
                                $(this).addClass("hover");
                                //$(this).find("td").eq(4).hide();
                                //$(this).find("td").eq(5).hide();
                            } else if ( e.type == 'click' ) {
                                var values = '';
                                var tds = $(this).find('td');
                            }else   {
                                $(this).removeClass("hover");
                            }
                        });
                        $("#site_requirement_items").delegate('td','click',function(e){
                            var itemid = $(this).parent().find("td").eq(0).html();
                            var itemdescr = $(this).parent().find("td").eq(1).html();
                            var itemunit = $(this).parent().find("td").eq(2).html();
                            var itemqty = $(this).parent().find("td").eq(3).html();
                            if ($(this).parent().index() != 0){ 
                                if ($(this).index() == 9){ 
                                    $("#editsitescopeid").val(alltrim(itemid));
                                    $("#editsitescopedescription").val(alltrim(itemdescr));
                                    $("#editsitescopedescription").css('width','350px');
                                    $("#editsitescopeunit").val(alltrim(itemunit));
                                    $("#editsitescopeqty").val(alltrim(itemqty));
                                    $("#activescopeid").val(alltrim(itemid));
                                    $("#estimate_item_items_edit").load("/est3yresspalisadecont/get_edit_site_requirements?requireid="+alltrim(itemid),function(data){
                                        //$("#dialog_edit_site_requirements").dialog("open");
                                        $("#editlist_date_req").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
                                        var thisdate = $("#editlist_date_req").attr('date');
                                        $("#editlist_date_req").datepicker('setDate',thisdate);
                                        $("#editlistdescription").css('width',250);
                                        $("#editlist_instruction").css('width',250);
                                        $("#button_do_edit_site_requirements").button();
                                        $("#button_cancel_edit_site_requirements").button();
                                        $("#button_do_edit_site_requirements").click(function(){
                                            var formserial = $("#edit_site_requirements_form").serialize();
                                            var jqxhr = $.post("/est3yresspalisadecont/ajaxEditSiteRequirements?"+alltrim(formserial), function(data) {
                                                //$("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                                                //activate_table_sites;
                                                $("#estimate_item_items_edit").empty();           
                                                $("#estimate_contracts_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                                                $("#ess_3yr_palisade_fencing_production_tabs").tabs('select', 3);
                                                //$("#estimate_item_list").load("/est3yresspalisadecont/get_site_requirements?linkid="+alltrim(consoleid),function(data){
                                                    //$("#newlist_date_req").datepicker();
                                                    //$("#newlist_date_req").datepicker( "option", "dateFormat", "yy-mm-dd" );
                                                //});
                                                return false;
                                            });
                                                return false;
                                        });
                                        $("#button_cancel_edit_site_requirements").click(function(){
                                                $("#estimate_item_items_edit").empty();           
                                                return false;
                                        });
                                    });
                                };
                            };
                        });
                    });
                    $("#ess_3yr_palisade_fencing_production_tabs").tabs('select', 2);
                    $("#palisade_pics").load("/est3yresspalisadecont/get_photos_by_site?siteid="+alltrim(siteid),function(data){
                        $('.thumb_clicked').click(function() {
                            //console.log($(this));
                            var picpath = $(this).attr('value');
                            window.open('/est3yresspalisadecont/estimating_pic_viewer?fname='+picpath, '_blank');
                            return false;
                        });
                    return false;
                    });
                    $('#palisade_pics_jcno').load("/productioncont/uploads_thumbs_per_jcno/"+alltrim(sitejno),function(){
                        $('.thumb_clicked').click(function() {
                            //console.log($(this));
                            var picpath = $(this).attr('value');
                            window.open('/productioncont/production_pic_viewer_jcno?fname='+picpath, '_blank');
                            return false;
                        });
                    return false;
                    });

                    $("#palisade_pics_default").load("/est3yresspalisadecont/get_default_pic?siteid="+alltrim(siteid),function(data){
                    });
                    $("#div_site_scope") .load("/est3yresspalisadecont/get_site_scope?siteid="+alltrim(siteid),function(data){
                        $("#button_add_new_site_scope").hide();
                        //$("#site_scope_items","tr").find("th").eq(4).hide();
                        //$("#site_scope_items","tr").find("td").eq(5).hide();
                        //$("#site_scope_items","tr").find("th").eq(5).hide();
                        $("#site_scope_items").delegate('tr','mouseover mouseleave click',function(e) {
                            e.preventDefault();
                            if (e.type == 'mouseover') {
                                $(this).addClass("hover");
                                $(this).find("td").eq(4).hide();
                                $(this).find("td").eq(5).hide();
                            } else if ( e.type == 'click' ) {
                                var values = '';
                                var tds = $(this).find('td');
                            }else   {
                                $(this).removeClass("hover");
                            }
                        });
                        $("#site_scope_items").delegate('td','click',function(e){
                            var itemid = $(this).parent().find("td").eq(0).html();
                            var itemdescr = $(this).parent().find("td").eq(1).html();
                            var itemunit = $(this).parent().find("td").eq(2).html();
                            var itemqty = $(this).parent().find("td").eq(3).html();
                            if ($(this).parent().index() != 0){ 
                                if ($(this).index() == 4){ 
                                    $("#editsitescopeid").val(alltrim(itemid));
                                    $("#editsitescopedescription").val(alltrim(itemdescr));
                                    $("#editsitescopedescription").css('width','350px');
                                    $("#editsitescopeunit").val(alltrim(itemunit));
                                    $("#editsitescopeqty").val(alltrim(itemqty));
                                    $("#activescopeid").val(alltrim(itemid));
                                    $("#dialog_editsitescope").dialog("open");
                                };
                                if ($(this).index() == 5){ 
                                    $("#activesiteidindex").val(siteidindex);
                                    var jqxhr = $.post("/est3yresspalisadecont/ajaxDeleteSiteScope/"+alltrim(itemid), function(data) {
                                        $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                                        activate_table_sites;
                                    });
                                };
                            };
                        });
                    });
                    $("#div_site_picture") .load("/est3yresspalisadecont/get_default_pic?siteid="+alltrim(siteid),function(data){
                    });
                    $("#div_jcno_scope") .load("/contractscont/ajaxsitescontractscopeofwork_production/"+alltrim(sitejno),function(data){
                        //console.log("JCNo Scope Loaded");
                    });
                    $("#div_jcno_despatch") .load("/est3yresspalisadecont/get_despatch_by_jcno?sitejcno="+alltrim(sitejno),function(data){
                        //console.log("JCNo Scope Loaded");
                    });
                };
                if ($(this).index() == 19){ 
                };
            };
        });
    };
    $("#button_do_add_new_item_palisade").button();
    $("#button_show_all_quotes").button();
    $("#button_do_add_new_item_palisade").click(function(){
        //console.log("Its here");
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
        $("#newlistdescription").css('width',250);
        $("#newlist_instruction").css('width',250);
        $("#newlist_date_req").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
        //$("#newlist_date_req" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
        $("#dialog_new_site_requirements").dialog("open");
    });
    $("#div_nonstandard_list").load("/est3yresspalisadecont/get_non_standard_list",function(data){
        //console.log("JCNo Scope Loaded");
    });
    $("#div_stores_stock").load("/est3yresspalisadecont/get_stores_stock_html",function(data){
        $("#button_get_stores_receive").button();
        $("#button_get_stores_despatch").button();
        $("#button_get_stores_return").button();
        $("#button_get_stores_stock_level").button();
        $("#div_stores_stock").show();
        $("#div_stores_stock_level").hide();
        $("#div_stores_stock_data").hide();
        $("#div_stores_receive").hide();
        $("#div_stores_receive_dropbox").hide();
        $("#div_stores_receive_data").hide();
        $("#div_stores_despatch").hide();
        $("#div_stores_despatch_dropbox").hide();
        $("#div_stores_despatch_data").hide();
        $("#div_stores_return").hide();
        $("#div_stores_return_data").hide();
        $("#div_stores_return_dropbox").hide();
        $("#button_get_stores_stock_level").click(function(){
            $("#div_stores_stock").show();
            $("#div_stores_stock_level").show();
            $("#div_stores_stock_data").show();
            $("#div_stores_receive").hide();
            $("#div_stores_receive_dropbox").hide();
            $("#div_stores_receive_data").hide();
            $("#div_stores_despatch").hide();
            $("#div_stores_despatch_dropbox").hide();
            $("#div_stores_despatch_data").hide();
            $("#div_stores_return").hide();
            $("#div_stores_return_data").hide();
            $("#div_stores_return_dropbox").hide();
            $("#div_stores_stock_level").load("/est3yresspalisadecont/get_stores_stock_level_html",function(data){
                $("#select_mat_dropdown").change(function(){
                    var thislistid = $(this).val();
                    $("#div_stores_stock_data").load("/est3yresspalisadecont/get_stores_stock_data?listid="+thislistid,function(data){
                    });
                });
            });
        });
        $("#button_get_stores_receive").click(function(){
            $("#div_stores_stock").show();
            $("#div_stores_stock_level").hide();
            $("#div_stores_stock_data").hide();
            $("#div_stores_receive").show();
            $("#div_stores_receive_data").show();
            $("#div_stores_receive_dropbox").show();
            $("#div_stores_despatch").hide();
            $("#div_stores_despatch_dropbox").hide();
            $("#div_stores_despatch_data").hide();
            $("#div_stores_return").hide();
            $("#div_stores_return_dropbox").hide();
            $("#div_stores_return_data").hide();
            $("#div_stores_receive").load("/est3yresspalisadecont/get_stores_receive_selectbox",function(data){
                $("#div_stores_receive_data").load("/est3yresspalisadecont/get_stores_receive_form",function(data){
                    $("#stores_receive_comment").css('width','400px');
                    $("#button_new_mat_receive").button();
                    $("#button_cancel_mat_receive").button();
                    $("#stores_receive_date").datepicker();
                    $("#stores_receive_date").datepicker( "option", "dateFormat", "yy-mm-dd" );
                    $("#button_cancel_mat_receive").click(function(){
                        //$("#div_stores_receive_dropbox").hide();
                        $("#div_stores_receive").hide();
                        $("#div_stores_receive_data").hide();
                        return false;
                    });
                    $("#button_new_mat_receive").click(function(){
                        var formserial = $("#stores_receive_form").serialize();
                        var jqxhr = $.post("/est3yresspalisadecont/ajaxAddNewStoresReceive?"+formserial, function(data) {
                            $("#div_stores_receive").empty();
                            $("#div_stores_receive").hide();
                            $("#div_stores_receive_data").hide();
                            return false;

                        });
                        return false;
                    });

                });
                $("#select_mat_dropdown_receive").change(function(){
                    var thislistid = $(this).val();
                    $("#div_stores_receive_data").load("/est3yresspalisadecont/get_stores_receive_data?listid="+thislistid,function(data){
                    });
                });
            });
        });
        $("#button_get_stores_despatch").click(function(){
            $("#div_stores_stock").show();
            $("#div_stores_stock_level").hide();
            $("#div_stores_stock_data").hide();
            $("#div_stores_receive").hide();
            $("#div_stores_receive_data").hide();
            $("#div_stores_receive_dropbox").hide();
            $("#div_stores_despatch").show();
            $("#div_stores_despatch_dropbox").show();
            $("#div_stores_despatch_data").show();
            $("#div_stores_return").hide();
            $("#div_stores_return_dropbox").hide();
            $("#div_stores_return_data").hide();
            $("#div_stores_despatch_dropbox").load("/est3yresspalisadecont/get_stores_stock_despatch_html",function(data){
                $("#div_stores_despatch_data").load("/est3yresspalisadecont/get_stores_despatch_form",function(data){
                    $("#stores_despatch_comment").css('width','400px');
                    $("#button_new_mat_despatch").button();
                    $("#button_cancel_mat_despatch").button();
                    $("#stores_despatch_date").datepicker();
                    $("#stores_despatch_date").datepicker( "option", "dateFormat", "yy-mm-dd" );
                    $("#button_cancel_mat_despatch").click(function(){
                        //$("#div_stores_despatch_dropbox").hide();
                        $("#div_stores_despatch").hide();
                        $("#div_stores_despatch_data").hide();
                        $("#div_stores_despatch_dropbox").hide();
                        return false;
                    });
                    $("#button_new_mat_despatch").click(function(){
                        var formserial = $("#stores_despatch_form").serialize();
                        var jqxhr = $.post("/est3yresspalisadecont/ajaxAddNewStoresDespatch?"+formserial, function(data) {
                            $("#div_stores_despatch").empty();
                            $("#div_stores_despatch").hide();
                            $("#div_stores_despatch_data").hide();
                            $("#div_stores_despatch_dropbox").hide();
                            return false;

                        });
                        return false;
                    });

                });
                $("#select_mat_dropdown_despatch").change(function(){
                    var thislistid = $(this).val();
                    $("#div_stores_despatch_data").load("/est3yresspalisadecont/get_stores_despatch_data?listid="+thislistid,function(data){
                    });
                });
            });
        });
        $("#button_get_stores_return").click(function(){
            $("#div_stores_stock").show();
            $("#div_stores_stock_level").hide();
            $("#div_stores_stock_data").hide();
            $("#div_stores_receive").hide();
            $("#div_stores_receive_data").hide();
            $("#div_stores_receive_dropbox").hide();
            $("#div_stores_despatch").hide();
            $("#div_stores_despatch_dropbox").hide();
            $("#div_stores_despatch_data").hide();
            $("#div_stores_return").show();
            $("#div_stores_return_dropbox").show();
            $("#div_stores_return_data").show();
            $("#div_stores_return_dropbox").load("/est3yresspalisadecont/get_stores_stock_return_html",function(data){
                $("#div_stores_return_data").load("/est3yresspalisadecont/get_stores_return_form",function(data){
                    $("#stores_return_comment").css('width','400px');
                    $("#button_new_mat_return").button();
                    $("#button_cancel_mat_return").button();
                    $("#stores_return_date").datepicker();
                    $("#stores_return_date").datepicker( "option", "dateFormat", "yy-mm-dd" );
                    $("#button_cancel_mat_return").click(function(){
                        //$("#div_stores_return_dropbox").hide();
                        $("#div_stores_return").hide();
                        $("#div_stores_return_data").hide();
                        $("#div_stores_return_dropbox").hide();
                        return false;
                    });
                    $("#button_new_mat_return").click(function(){
                        var formserial = $("#stores_return_form").serialize();
                        var jqxhr = $.post("/est3yresspalisadecont/ajaxAddNewStoresReturn?"+formserial, function(data) {
                            $("#div_stores_return").empty();
                            $("#div_stores_return").hide();
                            $("#div_stores_return_data").hide();
                            $("#div_stores_return_dropbox").hide();
                            return false;

                        });
                        return false;
                    });

                });
                $("#select_mat_dropdown_return").change(function(){
                    var thislistid = $(this).val();
                    $("#div_stores_return_data").load("/est3yresspalisadecont/get_stores_return_data?listid="+thislistid,function(data){
                    });
                });
            });
        });
        $("#button_get_stores_nonstandard").click(function(){

        });
            //console.log("JCNo Scope Loaded");
    });

    /// End of the production Section
});
