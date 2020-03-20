//Handels the jquery cctv 
//Dec 2012-12-31
$(function(){
    $("#cctv_one_cam_view").click(function(){
        window.open('/cctvcont/view_single_cam_jist', '_blank');
    });
    $("#cctv_one_cam_view_old").click(function(){
        getonecamonly(imgsrc,iplist);
        var camscount = iplist.length;
        for (var i = 0; i < camscount; i++) {
            console.log(iplist[i]);
        };
        return false;
    });
    $(".cctv_img_small").click(function(){
            thisvalue = $(this).attr('value');   
            //var imgmain = $("#img_main_cctv")
            //console.log(thisvalue);
            //console.log(imgmain.attr('src')); 
            $("#div_cctv_main_image").empty();
            $("#div_cctv_main_image").addClass('loading').removeClass('notloading');
            $("#div_cctv_main_image").load("/cctvcont/view_single_cam_jist_ajax?src="+alltrim(thisvalue),function(responseTxt,statusTxt,xhr){
                if(statusTxt=="success"){
                
                    $("#div_cctv_main_image").removeClass('loading').addClass('notloading');
                    //$("#div_cctv_main_image").html('Notloading');
                };
                if(statusTxt=="error"){
                    alert("Error: "+xhr.status+": "+xhr.statusText);
                };
                return false;
            });

    });
    function getonecamonly(imgsrc,iplist){
        var winwidth = $(window).width();
        var winx = 0 
        var winy = winwidth - 420
        var winwidth = 640 + 20 
        var winheight = 480 + 20 
        var windowName = "JISTCameras";
        var windowparams = "left="+winy + ",top=0,width="+winwidth+",height="+winheight+",status=no,resizable=no,location=no,menubar=no,scrollbars=no,alwaysRaised=yes"
        var newwin = window.open('', windowName, windowparams);
        newwin.document.write(imgsrc)
        var newwintest = newwin.document.getElementById("camera640view");
        console.log(newwintest.src);
        var thiscam = 0;
        //var camscount = iplist.length;
        var camscount = 2;

        setInterval (function(){
            if (thiscam >= camscount){thiscam=0}; 
            var iptag = iplist[thiscam];
            var uniqid = Math.random();
            //uniqid = uniqid * 10
            var newwinimg = newwin.document.getElementById("camera640view");
            var httptag = "http://";
            //var iptag = "jisttrading.no-ip.org:10091"
            var cgitag = "/cgi-bin/faststream.jpg?'";
            var params = "stream=full&amp;fps=1.0&amp;error=picture&amp;dummy="+parseInt(uniqid);
            var imgsrc =  httptag + iptag + cgitag + params;
            console.log(imgsrc);
            //newwinimg.src = '' ;
            newwinimg.src = imgsrc;
            thiscam++;
        },
        30000 );
    };

    // This initialises carousels on the container elements specified, in this case, carousel1.
    $("#carousel_cctv").CloudCarousel(		
        {			
            xPos: 950,
    yPos: 10,
    buttonLeft: $("#left-but"),
    buttonRight: $("#right-but"),
    altBox: $("#alt-text"),
    titleBox: $("#title-text"),
    autoRotate: 'yes',
    autoRotateDelay: 2000,
    minScale: 0.04,
    xRadius: 804,
    yRadius: 233,
    reflHeight: 40,
    reflGap: 10,
    reflOpacity: 0.8,
    bringToFront: true,
    mouseWheel: true
        }
        );
    //Using default configuration
    $("#carousel_grid").carouFredSel({
        items               : 3,
        mousewheel      : true,
        scroll : {
            items           : 1,
        easing          : "swing",
        duration        : 1000,                        
        timeoutDuration : 2500,
        pauseOnHover    : "resume",
        fx              : "scroll",
        },                  
        swipe :  {
                     onMouse    : true,
        onTouch    : true,
                 },
    }).css("cursor","pointer");

    //Using custom configuration
    function getOptions(items) {
        var i = $("input[name=s_items]").val(),
            p = $("select[name=s_position]").val(),
            o = $("select[name=s_order]").val(),
            d = $("select[name=s_deviation]").val();

        if (o == "false")	o = false;
        if (o == "true")	o = true;
        
        if (items)	return [i, p, o, d];
        else		return [p, o, d];
    };

    $("#insert_btn").click(function(e) {
        var arr = getOptions(true);
        $("#foo2").trigger("insertItem", arr);
        e.preventDefault();
    });

    $("#foo2_fx").change(function() {
        $("#carousel_grid").trigger("configuration", [ "scroll.fx", $(this).val() ]);
    });
    $("#foo2_direction").change(function() {
        $("#carousel_grid").trigger("configuration", [ "direction", $(this).val() ]);
    });

    $("#carousel_grid").find("img").css({"width":633,"height":476});
    $("#carousel_grid").trigger("configuration", [ "scroll.fx", 1 ]);
});
