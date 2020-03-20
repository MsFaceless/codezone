$(document).ready(function() {
    $( "#eskom_5yr_fencing_tabs" ).tabs({ 
        heightStyle: "fill", 
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
 //           console.log("beforeActivate pressed old tab is:" +ui.oldPanel.label) 
            }
  //          console.log("beforeActivate pressed new tab is:" +ui.panel) 
       }
    });
    $("#button_view_all_sites").button();
    $("#button_search_site_description").button();
    $("#button_search_site_name").button();
    $("#button_add_new_est_site").button();
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
    $("#button_view_all_sites").click(function(){
        $("#div_est_sites").load("/est5yreskomfencingcont/get_estimate_sites?switch=All",function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_search_site_name").click(function(){
        var searchphrase = $("#search_sitename").val()
        $("#div_est_sites").load("/est5yreskomfencingcont/get_estimate_sites?switch=SearchName&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_search_site_description").click(function(){
        var searchphrase = $("#search_sitedescription").val()
        $("#div_est_sites").load("/est5yreskomfencingcont/get_estimate_sites?switch=SearchDescription&searchphrase="+alltrim(searchphrase),function(responseTxt,statusTxt,xhr){
            activate_table_sites();
        });
    });
    $("#button_add_new_est_site").click(function(){
        $("#estimate_newsite").show();
    });
    $("#button_do_add_new_site").click(function(){
        var formserial = $("#frm_est_new_site").serialize();
        var jqxhr = $.post("/est5yreskomfencingcont/save_new_estimate_sites?"+formserial, function(data) {
            clear_form_elements($("#frm_est_new_site"));
            $("#estimate_newsite").hide();
            $("#button_view_all_sites").trigger("click");
            return false;
        });
            return false;
    });
    $("#button_do_cancel_new_site").click(function(){
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
                    $("#estimate_editsite").load("/est5yreskomfencingcont/get_edit_estimate_sites?siteid="+alltrim(siteid),function(data){
                        $("#estimate_editsite").show();
                        $("#button_do_cancel_edit_site").click(function(){
                            clear_form_elements($("#frm_est_new_site"));
                            $("#estimate_editsite").hide();
                            return false;
                        });
                        $("#button_do_edit_new_site").click(function(){
                            var formserial = $("#frm_edit_est_new_site").serialize();
                            var jqxhr = $.post("/est5yreskomfencingcont/save_edit_estimate_sites?"+formserial, function(data) {
                                clear_form_elements($("#frm_edit_est_new_site"));
                                $("#estimate_editsite").hide();
                                $("#button_view_all_sites").trigger("click");
                                return false;
                            });
                                return false;
                        });
                    }); 
                };
                if ($(this).index() == 10){ 
                    $("#estimate_quote_list").load("/est5yreskomfencingcont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
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
                            $("#estimate_quote_items").load("/est5yreskomfencingcont/get_estimate_quote_items?quoteid="+alltrim(thisquoteid),function(data){
                                 $("#estimate_quote_items").css("margin-left","16%");   //activate_table_sites();
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
                                            $("#estimate_quote_items_edit").load("/est5yreskomfencingcont/get_estimate_quote_items_edit?itemid="+alltrim(thisitemid),function(data){
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
                                                    var jqxhr = $.post("/est5yreskomfencingcont/save_edit_estimate_item?itemid="+alltrim(thisitemid)+"&"+formserial, function(data) {
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
                                            var jqxhr = $.post("/est5yreskomfencingcont/ajaxdeletequoteitem?itemid="+alltrim(thisitemid),function(responseTxt,statusTxt,xhr){
                                                            $("#quote_list").find("tr").eq(thisquoteindex).find("td").trigger("click");
                                            });
                                        };
                                    };

                                });
                            });

                        });
                    });
                    $("#eskom_5yr_fencing_tabs").tabs('select', 2);
                    $("#eskom_pics").load("/est5yreskomfencingcont/get_photos_by_site?siteid="+alltrim(siteid),function(data){
                        $('.thumb_clicked').click(function() {
                            //console.log($(this));
                            var picpath = $(this).attr('value');
                            window.open('/est5yreskomfencingcont/estimating_pic_viewer?fname='+picpath, '_blank');
                            return false;
                        });
                    });
                };
                if ($(this).index() == 19){ 
                };
            };
        });
    };
    function populate_quotes_from_sites(quoteno) {
    };
    $("#eskom_5yr_fencing_tabs").tabs('select', 1);
    $("#button_do_add_new_quote_eskom").click(function(){
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
        var jqxhr = $.post("/est5yreskomfencingcont/ajaxaddnewquotefull/"+alltrim(siteid),function(responseTxt,statusTxt,xhr){
            $("#estimate_quote_list").load("/est5yreskomfencingcont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    activate_table_sites;
                });
            });
    });
    $("#button_do_add_new_quote_empty_eskom").click(function(){
        var siteid = $("#activesiteid").val();
        var siteidindex = $("#activesiteidindex").val();
        var jqxhr = $.post("/est5yreskomfencingcont/ajaxaddnewquoteempty/"+alltrim(siteid),function(responseTxt,statusTxt,xhr){
            $("#estimate_quote_list").load("/est5yreskomfencingcont/get_estimate_quote_list?siteid="+alltrim(siteid),function(data){
                $("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                    activate_table_sites;
                });
            });
    });
    $("#boqlist_eskom").delegate('tr','mouseover mouseleave click',function(e) {
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
    $("#boqlist_eskom").delegate('td','click',function(e){
        if ($(this).parent().index() != 0){ 
            if ($(this).index() == 5){ 
                if ($("#activequoteid").val()){
                    var quoteidindex = $("#activequoteidindex").val();
                    var quoteid = $("#activequoteid").val();
                    var siteid = $("#activesiteid").val();
                    var siteidindex = $("#activesiteidindex").val();
                    var bqitemid = $(this).parent().find("td").eq(0).html();
                    console.log(quoteidindex);
                    var jqxhr = $.post("/est5yreskomfencingcont/ajaxaddnewquote_oneitem/"+alltrim(quoteid)+"/"+alltrim(bqitemid),function(responseTxt,statusTxt,xhr){
                            //$("#estimate_sites_table").find("tr").eq(siteidindex).find("td").eq(10).trigger("click");
                            $("#eskom_5yr_fencing_tabs").tabs('select', 2);
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
    var jqueryuploader_eskom = $('#jquery-fine-uploader_eskom').fineUploader({
        request: {
                     endpoint: '/est5yreskomfencingcont/estuploadfile'
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
        $("#eskom_pics") .load("/est5yreskomfencingcont/get_photos_by_site?siteid="+alltrim(activesiteid),function(data){
        });
        //console.log(response); 
    });
    $('#triggerUpload').click(function() {
        jqueryuploader_eskom.fineUploader('uploadStoredFiles');
        var formserial = $("#upload_data_form").serialize();
        return false;
    });
    $('#triggerClose').click(function() {
        close();
        return false;
    });
    $('#triggerReset').click(function() {
        jqueryuploader_eskom.fineUploader('reset');
        clear_form_elements($("#upload_data_form"));
        return false;
    });
    $('#pic_description').change(function(){
        $('#jquery-fine-uploader_eskom').show();
        $('#triggerUpload').show();
        $('#triggerReset').show();
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

    };
});
