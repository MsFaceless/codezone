$(document).ready(function() {
    $( "#fileupload_tabs" ).tabs({ 
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
       select: function(event,ui){
            //console.log("select pressed old tab is:" +ui.oldPanel); 
            //console.log("select pressed new tab is:" +ui.panel.id); 
            if (ui.panel.id=='ui-tabs-MyUploads'){
                var timestart = $("#pic_date_start").val();
                var timeend = $("#pic_date_end").val();
                $("#my_upload_list").load("/productioncont/myuploads?startdate="+timestart+"&enddate="+timeend,function(responseTxt,statusTxt,xhr){
                    $('.thumb_clicked').click(function() {
                        //console.log($(this));
                        var picpath = $(this).attr('value');
                        window.open('/productioncont/production_pic_viewer?fname='+picpath, '_blank');
                        return false;
                    });
                });
            };
            if (ui.panel.id=='ui-tabs-MySharedUploads'){
                var timeframe = $("#pic_view_timeframe").val();
                $("#my_upload_list_shared").load("/productioncont/uploads_shared_view",function(responseTxt,statusTxt,xhr){
                    $('.thumb_clicked').click(function() {
                        //console.log($(this));
                        var picpath = $(this).attr('value');
                        window.open('/productioncont/production_pic_viewer?fname='+picpath, '_blank');
                        return false;
                    });
                    $("#staff_faces_available_carousel_shared").carouFredSel({
                        items               : 10,
                        visible             : {
                            min             :5,
                        max             :10
                        },
                        direction           : "down",
                        mousewheel      : true,
                        scroll : {
                            items           : 5,
                        easing          : "linear",
                        duration        : 1000,                        
                        pauseOnHover    : true,
                        fx              : "directscroll",
                        },                  
                        swipe :  {
                                     onmouse    : true,
                        ontouch    : true,
                                 },
                    });
                    $("#staff_faces_available_carousel_shared").find("img").click(function() {
                        var currentpicid = $(this).attr("value");
                        //console.log(currentpicid);
                        $("#my_upload_list_pics_shared").load("/productioncont/uploads_shared_thumbs_per_user/"+alltrim(currentpicid),function(responseTxt,statusTxt,xhr){
                            $('.thumb_clicked').click(function() {
                                //console.log($(this));
                                var picpath = $(this).attr('value');
                                window.open('/productioncont/production_pic_viewer_shared?fname='+picpath, '_blank');
                                return false;
                            });
                        });

                    }).css("cursor","pointer");
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
    var jqueryuploader = $('#jquery-fine-uploader').fineUploader({
        request: {
                     endpoint: '/productioncont/uploadfile'
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
        $(this).fineUploader('setParams',{
           userid : $("#userid").val(),
        });
    }).on('complete',function(event,id,name,response){
        //console.log(response); 
    });
    $('#triggerUpload').click(function() {
        jqueryuploader.fineUploader('uploadStoredFiles');
        var formserial = $("#upload_data_form").serialize();
        return false;
    });
    $('#triggerClose').click(function() {
        close();
        return false;
    });
    $('#triggerReset').click(function() {
        jqueryuploader.fineUploader('reset');
        //$("#fileupload_tabs").tabs( "refresh" );
        clear_form_elements($("#upload_data_form"));
        return false;
    });
    $('#btn_unshare_from_pic').click(function() {
        var picid = $("#jist_viewer_current_pic_shared").attr('value');
        var jqxhr = $.post("/productioncont/deletepicturesharing_from_sharer?currentpicid="+picid, function(data) {
                return false;
        });
        return false;
    });
    $('#btn_get_my_thumbs').click(function() {
        var timestart = $("#pic_date_start").val();
        var timeend = $("#pic_date_end").val();
        $("#my_upload_list").load("/productioncont/myuploads?startdate="+timestart+"&enddate="+timeend,function(responseTxt,statusTxt,xhr){
            $('.thumb_clicked').click(function() {
                //console.log($(this));
                var picpath = $(this).attr('value');
                window.open('/productioncont/production_pic_viewer?fname='+picpath, '_blank');
                return false;
            });
        });
    });
    function alltrim(str) {
                return str.replace(/^\s+|\s+$/g, '');
    };
    $("#staff_faces_available_carousel").carouFredSel({
        items               : 10,
        visible             : {
            min             :5,
        max             :10
        },
        direction           : "up",
        mousewheel      : true,
        scroll : {
            items           : 5,
        easing          : "linear",
        duration        : 1000,                        
        pauseOnHover    : true,
        fx              : "directscroll",
        },                  
        swipe :  {
                     onmouse    : true,
        ontouch    : true,
                 },
    });
    $("#staff_faces_shared_carousel").carouFredSel({
        items               : 10,
        visible             : {
            min             :5,
        max             :10
        },
        direction           : "down",
        mousewheel      : true,
        scroll : {
            items           : 5,
        easing          : "linear",
        duration        : 1000,                        
        pauseOnHover    : true,
        fx              : "directscroll",
        },                  
        swipe :  {
                     onmouse    : true,
        ontouch    : true,
                 },
    });
    $("#staff_faces_shared_carousel_sharing").carouFredSel({
        items               : 10,
        visible             : {
            min             :5,
        max             :10
        },
        direction           : "down",
        mousewheel      : true,
        scroll : {
            items           : 5,
        easing          : "linear",
        duration        : 1000,                        
        pauseOnHover    : true,
        fx              : "directscroll",
        },                  
        swipe :  {
                     onmouse    : true,
        ontouch    : true,
                 },
    });
    //$("#staff_faces_carousel").css({"width":960,"height":800})
    $("#staff_faces_available_carousel").find("img").click(function() {
        $(this).animate({
            opacity     : 100
        }, 100).animate({
            width       : 80,
            margin      : 0,
            borderWidth : 0
        }, 100, function() {
            var htmldiv  = $(this).parent();
            $("#staff_faces_available_carousel").trigger("removeItem", $(this).parent());
            $("#staff_faces_available_carousel").trigger('updateSizes');
            $("#staff_faces_available_carousel").css("overflow","hidden");

            $("#staff_faces_shared_carousel").trigger("insertItem",[htmldiv,0,"null",0]);
            $("#staff_faces_shared_carousel").trigger('updateSizes');
            $("#staff_faces_shared_carousel").css("overflow","hidden");
            //var arr = getOptions(true);
            //$("#staff_faces_shared_carousel").trigger("insertItem", arr);
            //e.preventDefault();
            var userid = $(this).attr('value');
            var currentpicid = $("#jist_viewer_current_pic").attr("value");
            //console.log(val);
            var jrkqxhr = $.post("/productioncont/addpicturesharing?userid="+userid+"&currentpicid="+currentpicid, function(data1,status1,xhr1) {

                    return false;
            });
        });
    }).css("cursor","pointer");
    $("#staff_faces_shared_carousel").find("img").click(function() {
        $(this).animate({
            opacity     : 0
        }, 500).animate({
            width       : 0,
            margin      : 0,
            borderWidth : 0
        }, 500, function() {
            $("#staff_faces_shared_carousel").trigger("removeItem", $(this).parent());
            $("#staff_faces_shared_carousel").trigger('updateSizes');
            $("#staff_faces_shared_carousel").css("overflow","hidden");
            var picid = $("#jist_viewer_current_pic").attr('value');
            var userid = $(this).attr('value');
            //console.log(userid);
            var jqxhr = $.post("/productioncont/deletepicturesharing_from_owner?currentpicid="+picid+"&userid="+userid, function(data) {
                    return false;
            });
        });
    }).css("cursor","pointer");
    $('#pic_description').change(function(){
        $('#jquery-fine-uploader').show();
        $('#triggerUpload').show();
        $('#triggerReset').show();
        return false;
    });
    $('.rotate_pic').click(function(){
        var picid = $(this).attr('value');
        var jqxhr = $.post("/productioncont/rotate_pic?currentpicid="+picid, function(data) {
            window.location.reload();
        });
    });
    $('.rotate_pic_fencing_ests').click(function(){
        var picid = $(this).attr('value');
        var appname = $(this).attr('appname');
        var jqxhr = $.post("/est3yresspalisadecont/rotate_pic?currentpicid="+picid+"&appname="+appname, function(data) {
            window.location.reload();
        });
    });
    $('.set_default_pic').click(function(){
        var picid = $(this).attr('picid');
        var appname = $(this).attr('appname');
        var jqxhr = $.post("/est3yresspalisadecont/setdefault_pic?currentpicid="+picid+"&appname="+appname, function(data) {
            window.location.reload();
        });
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
    $("#fileupload_tabs").tabs('select', 1);
    $("#pic_date_taken").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#pic_date_start").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#pic_date_end").datepicker().datepicker( "option", "dateFormat", "yy-mm-dd" );
    $("#pic_subject" ).css("width","500px");
    $("#triggerClose").button();
    $("#btn_unshare_from_pic").button();
    $("#btn_get_my_thumbs").button();
    //$(document).tooltip({
    //    track: true
    //});
});
