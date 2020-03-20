//Handels javascript for the contracts pages
function toggle_sites_wip() {
    var ele = document.getElementById("sites_main_window");
    var text = document.getElementById("siteswip");
    var combobox = document.getElementById("searchwidget")
        if(ele.style.display == "block") {
            ele.style.display = "none";
            //text.innerHTML = "Show Bill of Quantities";
            text.checked = false
                combobox.style.display == "none";
        }
        else {
            ele.style.display = "block";
            combobox.style.display == "none";
            loadXMLSite('wip');
            //text.innerHTML = "Hide Bill of Quantities";
        }
} 
function toggle_sites_completed() {
    var ele = document.getElementById("sites_main_window");
    var text = document.getElementById("sitescompleted");
    var combobox = document.getElementById("searchwidget")
        if(ele.style.display == "block") {
            ele.style.display = "none";
            //text.innerHTML = "Show Bill of Quantities";
            text.checked = false
                combobox.style.display == "none";
        }
        else {
            ele.style.display = "block";
            combobox.style.display == "none";
            loadXMLSite('completed');
            //text.innerHTML = "Hide Bill of Quantities";
        }
} 
function loadXMLSite(mode)
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
    if (mode=='wip'){
        xmlhttp.open("GET","/contractscont/ajaxsiteswip/",true);
    }
    else{
        xmlhttp.open("GET","/contractscont/ajaxsitescompleted/",true);

    }
    xmlhttp.send();
    //clearoutputsow()
    //clearoutputsitescopeitems()
    //toggle_view_off_site_status_changer()
    //toggle_view_off_site_show()
}
function loadXMLSingleContract(jcno)
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
            var ajaxDisplay = document.getElementById('outputcontractorderitems');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
            //var editbuttondiv = document.getElementById('editcontractbutton');
            //editbuttondiv.style.display = "block";
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxsitescontractorderitems/"+jcno,true);
    xmlhttp.send();
    var ele2 = document.getElementById("activesiteid");
    ele2.value = jcno;
    loadXMLContractData(jcno)
}

function loadXMLContractData(jcno)
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
            var ajaxDisplay = document.getElementById('outputcontractdata');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxsitescontractdata/"+jcno,true);
    xmlhttp.send();
    loadXMLContractOrderItems(jcno)
        loadXMLContractScopeOfWork(jcno)
}

function loadXMLContractOrderItems(jcno)
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
            var ajaxDisplay = document.getElementById('outputcontractorderitems');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxsitescontractorderitems/"+jcno,true);
    xmlhttp.send();
}
function loadXMLContractScopeOfWork(jcno)
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
            var ajaxDisplay = document.getElementById('outputcontractscopeofwork');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxsitescontractscopeofwork/"+jcno,true);
    xmlhttp.send();
}
function LoadNewContractData(sitename,description,orderno,client,orderdate,contact){
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
            var ajaxDisplay = document.getElementById('outputtempsitestorage');
            ajaxDisplay.innerHTML = xmlhttp.responseText;

            //document.getElementsByName("radiostatuscode")[0].checked = true
            //loadXMLRadioStatuscode()
            //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
            //radio_check_val.checked = true 
            //loadXMLRadioStatuscodeChange()
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxnewcontract/"+client+"/"+sitename+"/"+description+"/"+orderno+"/"+orderdate+"/"+contact,true);

    xmlhttp.send();
};
function LoadNewOrderItem(siteid,item,description,unit,qty,price,total)
{
    //alert (item)
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
            var ajaxDisplay = document.getElementById('outputtempsitestorage');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
            loadXMLContractOrderItems(siteid);
            //document.getElementsByName("radiostatuscode")[0].checked = true
            //loadXMLRadioStatuscode()
            //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
            //radio_check_val.checked = true 
            //loadXMLRadioStatuscodeChange()
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxaddorderitem/"+siteid+"/"+item+"/"+description+"/"+unit+"/"+qty+"/"+price+"/"+total,true);
    xmlhttp.send();
};
function LoadEditOrderItem(uniq,itemid,siteid,item,description,unit,qty,price,total)
{
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
            var ajaxDisplay = document.getElementById('outputtempsitestorage');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
            loadXMLContractOrderItems(siteid);
            //document.getElementsByName("radiostatuscode")[0].checked = true
            //loadXMLRadioStatuscode()
            //var radio_check_val = document.getElementsByName("radiostatuscodechange")[0].value;
            //radio_check_val.checked = true 
            //loadXMLRadioStatuscodeChange()
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxeditorderitem/"+uniq+"/"+itemid+"/"+siteid+"/"+item+"/"+description+"/"+unit+"/"+qty+"/"+price+"/"+total,true);
    xmlhttp.send();
};
function LoadEditContractData(siteid,sitename,description,orderno,client,orderdate,contact,completed){
    //alert (siteid)
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
            var ajaxDisplay = document.getElementById('outputtempsitestorage');
            ajaxDisplay.innerHTML = xmlhttp.responseText;
            loadXMLContractData(siteid)
                loadXMLContractOrderItems(siteid)
        }
    }
    xmlhttp.open("GET","/contractscont/ajaxeditcontract/"+siteid+"/"+client+"/"+sitename+"/"+description+"/"+orderno+"/"+orderdate+"/"+contact+"/"+completed,true);

    xmlhttp.send();
};
function opencontractedit(siteid,editsitename,
        editsiteclientname,
        editsiteorderno,
        editsiteorderdate,
        editsitecontact,
        editsitedescription,
        editsitecompleted
        )
{
    $( "#dialog-editcontract" ).dialog( "open" );
    //alert("made it here")
    $("#editsitejcno").val(siteid);
    $("#editsitejcno").prop('disabled','disabled');
    $("#editsitename").val(editsitename);
    $('#editsitename').css('width','400px');
    $("#editsiteclientname").val(editsiteclientname);
    $('#editsiteclientname').css('width','400px');
    $("#editsiteorderno").val(editsiteorderno);
    $("#editsiteorderdate").val(editsiteorderdate);
    $( "#editsitecontact" ).val(editsitecontact);
    $("#editsitedescription").val(editsitedescription);
    $("#editsitecompleted").val(editsitecompleted);
    $("#editsitecompleted").prop('disabled','disabled');
    $('#editsitedescription').css('width','400px');
};
function addorderitem()
{
    $( "#dialog-addorderitem" ).dialog( "open" );
    //console.log("Made It");
    $("#price").change(function(e){ //if ($(this).val()){
            var supp_qty = $("#qty").val();
            var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
            //console.log(supp_total);
            $("#total").val(supp_total.toFixed(2));
        //};
    });
    $("#qty").change(function(e){ //if ($(this).val()){
            var supp_qty = $("#price").val();
            var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
            //console.log(supp_total);
            $("#total").val(supp_total.toFixed(2));
        //};
    });
//alert("made it here")
};

function editcontractorderitem(itemid,item,description,unit,quantity,price,total)
{
    $( "#dialog-editorderitem" ).dialog( "open" );
    $("#edit_id").val(itemid);
    $("#edit_id").hide();
    $("#labeledit_id").hide();
    $("#edit_item").val(item);
    $("#edit_item_description").val(description);
    $("#edit_unit").val(unit);
    $("#edit_qty").val(quantity);
    $("#edit_price").val(price);
    $("#edit_total").val(total);
    //alert("made it here")
    $("#edit_price").change(function(e){ //if ($(this).val()){
            var supp_qty = $("#edit_qty").val();
            var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
            //console.log(supp_total);
            $("#edit_total").val(supp_total.toFixed(2));
        //};
    });
    $("#edit_qty").change(function(e){ //if ($(this).val()){
            var supp_qty = $("#edit_price").val();
            var supp_total = parseFloat(supp_qty)*parseFloat($(this).val());
            //console.log(supp_total);
            $("#edit_total").val(supp_total.toFixed(2));
        //};
    });

};
function openstaffphotosdialog()
{
    $( "#dialog-staffphotos" ).dialog( "open" );
};
function loadOverviewContractData(jcno)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
        xmlhttp2=new XMLHttpRequest();
        xmlhttp3=new XMLHttpRequest();
        xmlhttp4=new XMLHttpRequest();
        xmlhttp5=new XMLHttpRequest();
        xmlhttp6=new XMLHttpRequest();
        xmlhttp7=new XMLHttpRequest();
        var ajaxDisplay = document.getElementById('ui-tabs-Contractual');
        var ajaxDisplay2 = document.getElementById('ui-tabs-POItems');
        var ajaxDisplay3 = document.getElementById('ui-tabs-SOW');
        var ajaxDisplay4 = document.getElementById('ui-tabs-Budgets');
        var ajaxDisplay5 = document.getElementById('ui-tabs-Labour');
        var ajaxDisplay6 = document.getElementById('ui-tabs-Buying');
        var ajaxDisplay7 = document.getElementById('ui-tabs-Invoices');
    }
    else
    {// code for IE6, IE5
        //do nothing
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4){
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
        if(xmlhttp.readyState == 1){
            ajaxDisplay.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp2.onreadystatechange = function(){
        if(xmlhttp2.readyState == 4){
            ajaxDisplay2.innerHTML = xmlhttp2.responseText;
        }
        if(xmlhttp2.readyState == 1){
            ajaxDisplay2.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp3.onreadystatechange = function(){
        if(xmlhttp3.readyState == 4){
            ajaxDisplay3.innerHTML = xmlhttp3.responseText;
        }
        if(xmlhttp3.readyState == 1){
            ajaxDisplay3.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp4.onreadystatechange = function(){
        if(xmlhttp4.readyState == 4){
            ajaxDisplay4.innerHTML = xmlhttp4.responseText;
        }
        if(xmlhttp4.readyState == 1){
            ajaxDisplay4.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp5.onreadystatechange = function(){
        if(xmlhttp5.readyState == 4){
            ajaxDisplay5.innerHTML = xmlhttp5.responseText;
        }
        if(xmlhttp5.readyState == 1){
            ajaxDisplay5.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp6.onreadystatechange = function(){
        if(xmlhttp6.readyState == 4){
            ajaxDisplay6.innerHTML = xmlhttp6.responseText;
        }
        if(xmlhttp6.readyState == 1){
            ajaxDisplay6.innerHTML = 'Loading !!!!';
        }
    }
    xmlhttp7.onreadystatechange = function(){
        if(xmlhttp7.readyState == 4){
            ajaxDisplay7.innerHTML = xmlhttp7.responseText;
        }
        if(xmlhttp7.readyState == 1){
            ajaxDisplay7.innerHTML = 'Loading !!!!';
        }
    }
    //xmlhttp.open("GET","/contractscont/ajaxsitescontractstatusupdate/"+jcno,true);
    //xmlhttp2.open("GET","/contractscont/ajaxsitescontractorderitems/"+jcno,true);
    //xmlhttp3.open("GET","/contractscont/ajaxsitescontractscopeofwork/"+jcno,true);
    //xmlhttp4.open("GET","/mngntcont/ajaxgetcontractbudget/"+jcno,true);
    xmlhttp5.open("GET","/mngntcont/ajaxshowsubconalljcnosummary/"+jcno,true);
    xmlhttp6.open("GET","/logisticscont/getPurchase_orders_for_jcno/"+jcno,true);
    xmlhttp7.open("GET","/mngntcont/ajax_invoices_per_contract/"+jcno,true);
    //xmlhttp.send();
    //xmlhttp2.send();
    //xmlhttp3.send();
    //xmlhttp4.send();
    xmlhttp5.send();
    xmlhttp6.send();
    xmlhttp7.send();
    //loadXMLContractOrderItems(jcno)
    //loadXMLContractScopeOfWork(jcno)
};

function loadOverviewContractDataContractual(jcno)
{
    //alert (item)
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
        var ajaxDisplay = document.getElementById('ui-tabs-Contractual');
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4){
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
        if(xmlhttp.readyState == 1){
            ajaxDisplay.innerHTML = 'Loading !!!!';
        }

    }
    xmlhttp.open("GET","/contractscont/ajaxsitescontractdata/"+jcno,true);
    xmlhttp.send();
};
function loadContractProductionBudget(jcno,tabname)
{
    //alert (item)
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
        var tabnames = tabname
            var ajaxDisplay = document.getElementById(tabname);
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4){
            ajaxDisplay.innerHTML = xmlhttp.responseText;
        }
        if(xmlhttp.readyState == 1){
            ajaxDisplay.innerHTML = 'Loading !!!!';
        }

    }
    xmlhttp.open("GET","/mngntcont/ajaxgetproductioncontractbudget/"+jcno,true);
    xmlhttp.send();
};
function loadPurchaseOrderItemsPerJCNO(jcno,tabname)
{
    //alert (item)
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp_purchaseorder=new XMLHttpRequest();
        var ajaxDisplay_req = document.getElementById(tabname);
    }
    xmlhttp_purchaseorder.onreadystatechange = function(){
        if(xmlhttp_purchaseorder.readyState == 4){
            ajaxDisplay_req.innerHTML = xmlhttp_purchaseorder.responseText;
        }
        if(xmlhttp_purchaseorder.readyState == 1){
            ajaxDisplay_req.innerHTML = 'Loading !!!!';
        }

    }
    xmlhttp_purchaseorder.open("GET","/logisticscont/purchase_reqs_per_jcno/"+jcno,true);
    xmlhttp_purchaseorder.send();
};
function loadPurchaseOrderItemsAddForm(jcno,tabname)
{
    //alert (item)
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp_purchaseitemsadd=new XMLHttpRequest();
        var ajaxDisplay_reqitemsadd = document.getElementById(tabname);
    }
    xmlhttp_purchaseitemsadd.onreadystatechange = function(){
        if(xmlhttp_purchaseitemsadd.readyState == 4){
            ajaxDisplay_reqitemsadd.innerHTML = xmlhttp_purchaseitemsadd.responseText;
        }
        if(xmlhttp_purchaseitemsadd.readyState == 1){
            ajaxDisplay_reqitemsadd.innerHTML = 'Loading !!!!';
        }

    }
    xmlhttp_purchaseitemsadd.open("GET","/logisticscont/purchase_reqs_items_add_form/"+jcno,true);
    xmlhttp_purchaseitemsadd.send();
};
function loadNewReq(jcno,thisdate,pref_supp,tabname)
{
    //alert (item)
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp_purchaseitemsadd=new XMLHttpRequest();
        var ajaxDisplay_reqitemsadd = document.getElementById(tabname);
    }
    xmlhttp_purchaseitemsadd.onreadystatechange = function(){
        if(xmlhttp_purchaseitemsadd.readyState == 4){
            ajaxDisplay_reqitemsadd.innerHTML = xmlhttp_purchaseitemsadd.responseText;
        }
        if(xmlhttp_purchaseitemsadd.readyState == 3){
            ajaxDisplay_reqitemsadd.innerHTML = xmlhttp_purchaseitemsadd.responseText;
        }
        if(xmlhttp_purchaseitemsadd.readyState == 1){
            ajaxDisplay_reqitemsadd.innerHTML = 'Loading !!!!';
        }

    }
    xmlhttp_purchaseitemsadd.open("GET","/logisticscont/savenew_requisition/"+jcno+"/"+thisdate+"/"+pref_supp,false);
    xmlhttp_purchaseitemsadd.send();
};
function alltrim(str) {
    return str.replace(/^\s+|\s+$/g, '');
};

function map_init(){
    var box_extents = [
        [-10, 50, 5, 60],
    [-75, 41, -71, 44],
    [-122.6, 37.6, -122.3, 37.9],
    [10, 10, 20, 20]
        ];
    var map;
    map = new OpenLayers.Map('map');

    var ol_wms = new OpenLayers.Layer.WMS( "OpenLayers WMS",
            "http://vmap0.tiles.osgeo.org/wms/vmap0?", {layers: 'basic'} );

    var boxes  = new OpenLayers.Layer.Boxes( "Boxes" );
    for (var i = 0; i < box_extents.length; i++) {
        ext = box_extents[i];
        bounds = OpenLayers.Bounds.fromArray(ext);
        box = new OpenLayers.Marker.Box(bounds);
        box.events.register("click", box, function (e) {
            this.setBorder("yellow");
        });
        boxes.addMarker(box);
    }

    map.addLayers([ol_wms, boxes]);
    map.addControl(new OpenLayers.Control.LayerSwitcher());
    map.zoomToMaxExtent();
}
