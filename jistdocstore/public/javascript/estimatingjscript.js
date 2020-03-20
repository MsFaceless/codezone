//Handels javascript for the 3yr building estimate pages
function loadXMLHeaders(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputheadings');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrheadings/"+jcno,true);
    xmlhttp.send();
    clearoutputitems()
    clearoutputsubheadings()
}
function loadXMLSubHeaders(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsubheadings');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrsubheadings/"+jcno,true);
    xmlhttp.send();
    clearoutputitems()
}
function loadXMLSite()
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsites');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrsites/"+1,true);
    xmlhttp.send();
    clearoutputsow()
    clearoutputquotesow()
    //clearoutputsow()
    //clearoutputsitescopeitems()
    //toggle_view_off_site_status_changer()
    //toggle_view_off_site_show()
}
function loadXMLSOW(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      xmlhttp2=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitesow');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp2.onreadystatechange = function(){
            if(xmlhttp2.readyState == 4){
                var ajaxDisplay2 = document.getElementById('output_newquotebox');
                ajaxDisplay2.innerHTML = xmlhttp2.responseText;
            }
      }
    xmlhttp.open("GET","/estimatingcont/ajax3yrsitesow/"+jcno,true);
    xmlhttp2.open("GET","/estimatingcont/ajax3yrnewquotescope/"+jcno,true);
    xmlhttp.send();
    xmlhttp2.send();
    toggle_site_status_edit_changer()
    toggle_view_on_scope_buttons()
    var elestat = document.getElementById("outputsitestatuschanger");
    elestat.style.display = "none";
    clearoutputsow()
    clearoutputquotesow()
    clearoutputsitescopeitems()
    clearoutputquotescope()
    clearoutputquotescopeitems()
    var ele = document.getElementById("outputsites");
    if(ele.style.display == " ") {
            ele.style.display = "block";
            }
    var ele2 = document.getElementById("activesiteid");
    ele2.value = jcno;
    LoadXMLAllQuotesForJNo(jcno)
    var ele3 = document.getElementById("radio_status_changer_jcno");
    ele3.value = jcno;
}
function loadXMLItems(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputitems');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    var ele2 = document.getElementById("activescopeid");
    var scopeid = ele2.value;
    xmlhttp.open("GET","/estimatingcont/ajax3yritems/"+jcno+"/"+scopeid,true);
    xmlhttp.send();
    toggle_view_off_site_status_changer()
    toggle_view_off_site_show()
}
function loadXMLBQItems(scopeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      var ele3 = document.getElementById("activesiteid");
      var jcno = ele3.value
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitescopeitems');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrscopeitems/"+scopeid+"/"+jcno,true);
    xmlhttp.send();
    toggle_view_off_site_status_changer()
    var ele2 = document.getElementById("activescopeid");
    ele2.value = scopeid;
    //clearoutputsites()
    toggle_view_off_site_show()
}
function loadXMLSiteBQItem(bqitemid,sitesowid)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      var ele3 = document.getElementById("activesiteid");
      var jcno = ele3.value
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    //var thisamount = $("#bqitemqty").val();
    //alert(thisamount)
    var ele2 = document.getElementById("activescopeid");
    var scopeid = ele2.value
    //alert(scopeid)
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                loadXMLBQItems(scopeid)
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yraddbqitem_tosite/"+jcno+"/"+bqitemid+"/"+scopeid,true);
    xmlhttp.send();
}
function openestsite(siteid,sitename,sitedate,sitedescription,sitewonumber,sitesupervisor,sitearea)
{
    $( "#dialog-editsite" ).dialog( "open" );
    //alert("made it here")
    $("#editsiteid").val(siteid)
    $("#editsitename").val(sitename)
    $('#editsitename').css('width','400px');
    $("#editsitedate").val(sitedate)
    $("#editsitedescription").val(sitedescription)
    $('#editsitedescription').css('width','400px');
    $("#editsitewonumber").val(sitewonumber)
    $("#editsitesupervisor").val(sitesupervisor)
    $("#editsitearea").val(sitearea)
}
function openbqqty(bqitemid,currentvalue,currentprice)
{
    $( "#dialog-newbqqty" ).dialog( "open" );
    var ele2 = document.getElementById("activebqitemid");
    ele2.value = bqitemid;
    $("#bqitemqty").val(currentvalue)
    $("#bqitemprice").val(currentprice)
}
function deleteitemscope(bqitemid)
{
    var uniqid = Math.random()
    var jqxhr = $.post("/estimatingcont/ajax3yrremoveitemscope/"+uniqid+"/"+bqitemid, function(data) {
        var ele2 = document.getElementById("activescopeid");
        var scopeid = ele2.value
        loadXMLBQItems(scopeid)
        //$("#grv_items").empty()
        //$("#grv_details").load("/logisticscont/grv_order_one_details/"+parseInt(activepo),callback_load_order_items_grv);
        })
}
function openeditscope(scopeid,currentscope,currentunit,currentqty,thisid)
{
    $( "#dialog-editscope" ).dialog( "open" );
    //var ele2 = document.getElementById("activebqitemid");
    //ele2.value = bqitemid;
    //alert(currentvalue)
    $('#editscopename').css('width','400px');
    $("#editscopename").val(currentscope)
    $("#editscopeunit").val(currentunit)
    $("#editscopeqty").val(currentqty)
    $("#editscopeid").val(thisid)
}
function loadXMLRadioStatuscode()
{
    var xmlhttp;
    var buttonpressed = getradiostatusbuttonpressed()
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsites');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                var ele2 = document.getElementById("activesiteid");
                ele2.value = '';
                var ele3 = document.getElementById("activescopeid");
                ele3.value = '';
                var ele4 = document.getElementById("activebqitemid");
                ele4.value = '';
                toggle_view_off_scope_buttons();
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrsites/"+buttonpressed,true);
    xmlhttp.send();
    clearoutputsow()
    clearoutputsitescopeitems()
    clearoutputquotescope()
    clearoutputquotescopeitems()
    toggle_view_off_site_status_changer()
    document.getElementById("output_newquotebox").innerHTML = "";
    document.getElementById("output_allquotebox").innerHTML = "";

    //clearoutputstatuSchanger()
}
function loadXMLRadioStatuscodeChange()
{
    var xmlhttp;
    var buttonpressed = getradiostatusbuttonchangepressed()
    var ele2 = document.getElementById("activesiteid");
    var jcno = ele2.value
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrstatuschange/"+buttonpressed+"/"+jcno,true);
    xmlhttp.send();
    loadXMLRadioStatuscode()

}
function LoadNewSiteData(name,description,area,wonumber,supervisor){
    //alert (name+email+password)
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitescopeitems');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                //loadXMLSite();
                document.getElementsByName("radiostatuscode")[0].checked = true
                loadXMLRadioStatuscode()
                //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
                //radio_check_val.checked = true 
                //loadXMLRadioStatuscodeChange()
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrnewsite/"+name+"/"+description+"/"+area+"/"+wonumber+"/"+supervisor,true);
    xmlhttp.send();
}
function LoadNewScopeData(name,unit,qty){
    //alert (name+email+password)
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
     var ele2 = document.getElementById("activesiteid");
     var jcno = ele2.value
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitescopeitems');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                loadXMLSOW(jcno);
                //var jno = ${session['session_site'][0].id}
                //alert(jno)
                //loadXMLSite();
                //document.getElementsByName("radiostatuscode")[0].checked = true
                //loadXMLRadioStatuscode()
                //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
                //radio_check_val.checked = true 
                //loadXMLRadioStatuscodeChange()
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrnewscope/"+name+"/"+jcno+"/"+unit+"/"+qty,true);
    xmlhttp.send();
}
function LoadEditScopeData(name,unit,qty){
    //alert (name+email+password)
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
     var ele2 = document.getElementById("activesiteid");
     var eleid = document.getElementById("editscopeid");
     var jcno = ele2.value
     var thisid = eleid.value
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                loadXMLSOW(jcno);
                loadXMLBQItems(thisid);
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yreditscope/"+name+"/"+jcno+"/"+unit+"/"+qty+"/"+thisid,true);
    xmlhttp.send();
}
function LoadEditSiteData(siteid,sitedate,sitename,sitedescription,sitewonumber,sitesupervisor,sitearea){
    alert (siteid+sitedate+sitename+sitedescription+sitewonumber+sitesupervisor+sitearea)
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
     var ele2 = document.getElementById("activesiteid");
     var eleid = document.getElementById("editscopeid");
     var jcno = ele2.value
     var thisid = eleid.value
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                //loadXMLSOW(jcno);
                loadXMLRadioStatuscode()
                //loadXMLBQItems(thisid);
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yreditsite/"+siteid+"/"+sitedate+"/"+sitename+"/"+sitedescription+"/"+sitewonumber+"/"+sitesupervisor+"/"+sitearea,true);
    xmlhttp.send();
}
function LoadNewQuoteData(scopearray){
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      var ele1 = document.getElementById("activesiteid");
      var siteid = ele1.value ;
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                //loadXMLSite();
                //document.getElementsByName("radiostatuscode")[0].checked = true
                //loadXMLRadioStatuscode()
                //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
                //radio_check_val.checked = true 
                //loadXMLRadioStatuscodeChange()
                LoadXMLAllQuotesForJNo(siteid)
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yraddnewquote/"+siteid+"/"+scopearray,true);
    xmlhttp.send();
}
function LoadXMLAllQuotesForJNo(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    var ele1 = document.getElementById("activesiteid");
    var siteid = ele1.value ;
    var ele2 = document.getElementById("activescopeid");
    var scopeid = ele2.value;
    var ele3 = document.getElementById("activebqitemid");
    var bqitemid = ele3.value;
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('output_allquotebox');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrquotespercontract/"+jcno,true);
    xmlhttp.send();
}
function LoadXMLQuoteScopesShow(quoteid)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    var ele1 = document.getElementById("activesiteid");
    var siteid = ele1.value ;
    var ele2 = document.getElementById("activescopeid");
    var scopeid = ele2.value;
    var ele3 = document.getElementById("activebqitemid");
    var bqitemid = ele3.value;
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('output_thisquotescope');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrquotescopeshow/"+quoteid,true);
    clearoutputquotescope()
    clearoutputquotescopeitems()
    xmlhttp.send();
}
function LoadXMLQuoteScopesItemsShow(quoteid,scopeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    var ele1 = document.getElementById("activesiteid");
    var siteid = ele1.value ;
    var ele2 = document.getElementById("activescopeid");
    var scopeid2 = ele2.value;
    var ele3 = document.getElementById("activebqitemid");
    var bqitemid = ele3.value;
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('output_thisquotescopeitems');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yrquotescopeitemsshow/"+quoteid+"/"+scopeid,true);
    xmlhttp.send();
}
function LoadXMLQuotePDF(quoteid)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    var ele1 = document.getElementById("activesiteid");
    var siteid = ele1.value ;
    var ele2 = document.getElementById("activescopeid");
    var scopeid2 = ele2.value;
    var ele3 = document.getElementById("activebqitemid");
    var bqitemid = ele3.value;
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){

        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent
                //var ajaxDisplay = document.getElementById('output_thisquotescopeitems');
                //ajaxDisplay.innerHTML = xmlhttp.responseText;
            }
        }
    xmlhttp.open("GET","/estimatingcont/export_3yr_quote_to_pdf/"+quoteid,false);
    xmlhttp.send();
}
function LoadXMLEditBQQty(bqqty,bqitemprice)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
          //do nothing
      }
    var ele1 = document.getElementById("activesiteid");
    var siteid = ele1.value ;
    var ele2 = document.getElementById("activescopeid");
    var scopeid = ele2.value;
    var ele3 = document.getElementById("activebqitemid");
    var bqitemid = ele3.value;
    //var thisamount = $("#bqitemqty").val();
    //alert(scopeid)
    xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4){
                var ajaxDisplay = document.getElementById('outputsitestatuschanger');
                ajaxDisplay.innerHTML = xmlhttp.responseText;
                loadXMLBQItems(scopeid)
            }
        }
    xmlhttp.open("GET","/estimatingcont/ajax3yredit_bqqty/"+bqqty+"/"+siteid+"/"+scopeid+"/"+bqitemid+"/"+bqitemprice,true);
    xmlhttp.send();
    //toggle_view_off_site_status_changer()
    //clearoutputsites()
    //toggle_view_off_site_show()
}
function clearoutputheadings(){
    document.getElementById("outputheadings").innerHTML = "";
}
function clearoutputsubheadings(){
    document.getElementById("outputsubheadings").innerHTML = "";
}
function clearoutputitems(){
    document.getElementById("outputitems").innerHTML = "";
}
function clearoutputsow(){
    //toggle_view_off_site_status_changer()
    document.getElementById("outputsitesow").innerHTML = "";
}
function clearoutputquotesow(){
    //toggle_view_off_site_status_changer()
    document.getElementById("output_newquotebox").innerHTML = "";
    document.getElementById("output_allquotebox").innerHTML = "";
}
function clearoutputsites(){
    document.getElementById("outputsites").innerHTML = "";
}
function clearoutputstatuschanger(){
    document.getElementById("radio_status_changer").innerHTML = "";
}
function clearoutputsitescopeitems(){
    document.getElementById("outputsitescopeitems").innerHTML = "";
}
function clearoutputquotescope(){
    document.getElementById("output_thisquotescope").innerHTML = "";
}
function clearoutputquotescopeitems(){
    document.getElementById("output_thisquotescopeitems").innerHTML = "";
}
function updatepage(str){
    document.getElementById("output").innerHTML = str;
}
function doIntervalUpdate()
{
    loadXMLDoc();
    setInterval ("loadXMLDoc()", 1000 );
}
function toggle_boq() {
    var ele = document.getElementById("toggleText_boq");
    var text = document.getElementById("displayText_boq");
    window.body.style.width = '100%'
    if(ele.style.display == "block") {
            ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
        text.checked = false
    }
    else {
        ele.style.display = "block";
        //text.innerHTML = "Hide Bill of Quantities";
    }
} 
function toggle_view_on_site_status_changer() {
    var ele = document.getElementById("toggleText_status_changer");
    if(ele.style.display == "block") {
            //ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
        //var buttpressed = getradiostatusbuttonpressed();
        //document.getElementsByName("radiostatuscodechange")[buttpressed-1].checked = "checked";
    }
    else {
        ele.style.display = "block";
        var buttpressed = getradiostatusbuttonpressed();
        //alert(buttpressed);
        document.getElementsByName("radiostatuscodechange")[buttpressed-1].checked = "checked";
            
    }
} 
function toggle_site_status_edit_changer() {
    var ele = document.getElementById("toggleText_status_changer");
    if(ele.style.display == "block") {
            //ele.style.display = "none";
        var buttpressed = getradiostatusbuttonpressed();
        document.getElementsByName("radiostatuscodechange")[buttpressed-1].checked = "checked";
    }
    else {
        ele.style.display = "block";
        var buttpressed = getradiostatusbuttonpressed();
        //alert(buttpressed);
        document.getElementsByName("radiostatuscodechange")[buttpressed-1].checked = "checked";
            
    }
} 
function toggle_scope_buttons() {
    var ele = document.getElementById("outputscopebuttons");
    if(ele.style.display == "block") {
            ele.style.display = "none";
    }
    else {
        ele.style.display = "block";
            
    }
} 
function toggle_view_off_site_status_changer() {
    var ele = document.getElementById("toggleText_status_changer");
    if(ele.style.display == "block") {
            ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else {
        //ele.style.display = "block";
    }
} 
function toggle_view_off_site_show() {
    var ele = document.getElementById("outputsites");
    //alert(ele.style.display)
    if(ele.style.display == "block") {
            ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele.style.display == "none") {
        //ele.style.display = "block";
    }
    else {
        ele.style.display = "none";
    }
    var ele2 = document.getElementById("radio_status_box");
    var ele3 = document.getElementById("outputsiteviewbutton");
    var text = document.getElementById("displayText_sites");
    ele3.style.display = "block"
    var ele4 = document.getElementById("radio_view_all_site_info");
    ele4.checked = false
    if(ele2.style.display == "block") {
            ele2.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele2.style.display == "none") {
        //ele.style.display = "block";
    }
    else {
        ele2.style.display = "none";
    }
} 
function toggle_view_on_site_show() {
    var ele = document.getElementById("outputsites");
    //alert(ele.style.display)
    if(ele.style.display == "block") {
            //ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele.style.display == "none") {
        ele.style.display = "block";
    }
    else {
        ele.style.display = "block";
    }
    var ele2 = document.getElementById("radio_status_box");
    var ele3 = document.getElementById("outputsiteviewbutton");
    var text = document.getElementById("displayText_sites");
    ele3.style.display = "none"
    if(ele2.style.display == "block") {
            //ele2.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele2.style.display == "none") {
        ele2.style.display = "block";
    }
    else {
        ele2.style.display = "block";
    }
} 
function toggle_view_off_scope_buttons() {
    var ele = document.getElementById("outputscopebuttons");
    //alert(ele.style.display)
    if(ele.style.display == "block") {
            ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele.style.display == "none") {
        //ele.style.display = "block";
    }
    else {
        ele.style.display = "none";
    }
} 
function toggle_view_on_scope_buttons() {
    var ele = document.getElementById("outputscopebuttons");
    //alert(ele.style.display)
    if(ele.style.display == "block") {
         //   ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele.style.display == "none") {
        ele.style.display = "block";
    }
    else {
        ele.style.display = "block";
    }
} 
function toggle_view_off_scope_show() {
    var ele = document.getElementById("outputscopebuttons");
    //alert(ele.style.display)
    if(ele.style.display == "block") {
            //ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
    }
    else if(ele.style.display == "none") {
        ele.style.display = "block";
    }
    else {
        ele.style.display = "block";
    }
} 
function toggle_sites() {
    var ele = document.getElementById("sites_main_window");
    var elebody = document.getElementById("body");
    var text = document.getElementById("displayText_sites");
    var container = document.getElementById("app_container");
    var body = document.getElementById("body");

    if(ele.style.display == "block") {
        ele.style.display = "none";
        //ele.style.width = "100%";
        //text.innerHTML = "Show Bill of Quantities";
        text.checked = false
    }
    else {
        ele.style.display = "block";
        var winwidth = window.innerWidth; 
        //setscreensize(winwidth);
        //console.log(body);
        //console.log(winwidth);
        //container.style.width = winwidth;
        //body.style.width = winwidth
        //$(window).onresize= setscreensize(winwidth);
        //loadXMLSite();
        //text.innerHTML = "Hide Bill of Quantities";
    }
} 
function toggle_newquote_box() {
    var ele = document.getElementById("newquotebox");
    var text = document.getElementById("idnew_quote_box");
    if(ele.style.display == "block") {
            ele.style.display = "none";
        //text.innerHTML = "Show Bill of Quantities";
        text.checked = false
    }
    else {
        ele.style.display = "block";
        //loadXMLSite();
        //text.innerHTML = "Hide Bill of Quantities";
    }
} 
function getradiostatusbuttonpressed() {
    var radio_check_val = "";
    var status = document.getElementsByName("radiostatuscode").length;
    //alert(status);
    var i ;
    for (i = 0; i < document.getElementsByName("radiostatuscode").length; i++) {
        if (document.getElementsByName("radiostatuscode")[i].checked) {
            //alert("this radio button was clicked: " + document.getElementsByName("radiostatuscode")[i].value);
            radio_check_val = document.getElementsByName("radiostatuscode")[i].value;
            document.getElementById("output_newquotebox").innerHTML = "";
            document.getElementById("output_allquotebox").innerHTML = "";
            return radio_check_val
        }
    }
    if (radio_check_val == "")
    {
        alert("please select radio button");
    }
}
function getradiostatusbuttonchangepressed() {
    var radio_check_val = "";
    var status = document.getElementsByName("radiostatuscodechange").length;
    //alert(status);
    var i ;
    for (i = 0; i < document.getElementsByName("radiostatuscodechange").length; i++) {
        if (document.getElementsByName("radiostatuscodechange")[i].checked) {
            //alert("this radio button was clicked: " + document.getElementsByName("radiostatuscode")[i].value);
            radio_check_val = document.getElementsByName("radiostatuscodechange")[i].value;
            return radio_check_val
        }
    }
    if (radio_check_val == "")
    {
        alert("please select radio button");
    }
}
function scopecheck() {
    var radio_check_val = "";
    var status = document.getElementsByName("chkboxscopequote").length;
    var checkvals = new Array()
    //alert(status);
    var i ;
    for (i = 0; i < document.getElementsByName("chkboxscopequote").length; i++) {
        if (document.getElementsByName("chkboxscopequote")[i].checked) {
            //alert("this radio button was clicked: " + document.getElementsByName("radiostatuscode")[i].value);
            radio_check_val = document.getElementsByName("chkboxscopequote")[i].value;
            checkvals[i] = radio_check_val 
        }
    }
    if (radio_check_val == "")
    {
        alert("please select check box");
    }
    LoadNewQuoteData(checkvals) 
    //return checkvals
}
function loadQuoteToScopeOfWorks(quoteno)
{
    //console.log("Made IT Here")
    //alert()
    //$("#output_thisquotescope").hide()
    $("#activequoteno").val(quoteno);
    $( "#dialog-QuoteContract" ).dialog( "open" );
    
}
function AddNewQuoteToContractScope(quoteno,jcno)
{
    //console.log("Made IT Here")
    //alert()
    //$("#output_thisquotescope").hide()
    $( "#dialog-QuoteContract" ).dialog( "open" );
    
}

