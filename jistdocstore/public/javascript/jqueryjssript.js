//Handels the estimate pages
$(document).ready(function(){
        $( "#dialog-message" ).dialog({
            modal: true,
            buttons: {
                Ok: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });

$(function() {
        $( "#dialog-confirm" ).dialog({
            resizable: false,
            height:140,
            modal: true,
            buttons: {
                "Delete all items": function() {
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
$(function() {
        var sitename = $( "#sitename" ),
            description = $( "#description" ),
            area = $( "#area" ),
            wonumber = $( "#wonumber" ),
            supervisor= $( "#supervisor" ),
            allsiteFields = $( [] ).add( sitename ).add( description ).add( area ).add( wonumber).add(supervisor),
            tips = $( ".validateSiteTips" );
            scopename = $( "#scopename" ),
            scopeunit = $( "#scopeunit" ),
            editscopename = $( "#editscopename" ),
            editscopeunit = $( "#editscopeunit" ),
            editscopeqty = $( "#editscopeqty" ),
            editsitedate = $("#editsitedate").datepicker();
            $( "#editsitedate" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
            editsitename = $("#editsitename");
            editsitewonumber = $("#editsitewonumber");
            editsitearea = $("#editsitearea");
            editsitesupervisor = $("#editsitesupervisor");
            editsitedescription = $("#editsitedescription");
            editsiteid = $("#editsiteid");
            scopeqty = $( "#scopeqty" ),
            allscopeFields = $( [] ).add( scopename ).add( scopeunit ).add( scopeqty ),
            alleditscopeFields = $( [] ).add( editscopename ).add( editscopeunit ),
            alleditsiteFields = $( [] ).add( editsitename ).add( editsiteid ).add( editsitedate ).add( editsitesupervisor ).add( editsitedescription ).add( editsitewonumber ).add( editsitearea ),
            tips = $( ".validateScopeTips" );
            bqitemqty = $( "#bqitemqty" ),
            bqitemprice = $( "#bqitemprice" ),
            allbqitemFields = $( [] ).add( bqitemqty ),
            tips = $( ".validateBQItemTips" );
 
        function updateTips( t ) {
            tips
                .text( t )
                .addClass( "ui-state-highlight" );
            setTimeout(function() {
                tips.removeClass( "ui-state-highlight", 1500 );
            }, 500 );
        }
 
        function checkLength( o, n, min, max ) {
            if ( o.val().length > max || o.val().length < min ) {
                o.addClass( "ui-state-error" );
                updateTips( "Length of " + n + " must be between " +
                    min + " and " + max + "." );
                return false;
            } else {
                return true;
            }
        }
 
        function checkRegexp( o, regexp, n ) {
            if ( !( regexp.test( o.val() ) ) ) {
                o.addClass( "ui-state-error" );
                updateTips( n );
                return false;
            } else {
                return true;
            }
        }
 
        $( "#dialog-newsite" ).dialog({
            autoOpen: false,
            height: 450,
            width: 450,
            modal: true,
            buttons: {
                "Create New Site": function() {
                    var bValid = true;
                    allsiteFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( sitename, "site name", 3, 120 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadNewSiteData(sitename.val(),description.val(),area.val(),wonumber.val(),supervisor.val())
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
                allsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#dialog-newscope" ).dialog({
            autoOpen: false,
            height: 350,
            width: 250,
            modal: true,
            buttons: {
                "Create New Scope": function() {
                    var bValid = true;
                    allscopeFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( scopename, "site name", 3, 80 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadNewScopeData(scopename.val(),scopeunit.val(),scopeqty.val())
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
                allscopeFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#dialog-editscope" ).dialog({
            autoOpen: false,
            height: 250,
            width: 450,
            modal: true,
            buttons: {
                "Edit Scope": function() {
                    var bValid = true;
                    //allscopeFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( editscopename, "site name", 3, 80 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                    if ( bValid ) {
                        LoadEditScopeData(editscopename.val(),editscopeunit.val(),editscopeqty.val())
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
                alleditscopeFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#dialog-editsite" ).dialog({
            autoOpen: false,
            height: 450,
            width: 450,
            modal: true,
            buttons: {
                "Edit Site": function() {
                    var bValid = true;
                    //allscopeFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( editsitename, "site name", 3, 80 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                    if ( bValid ) {
                        LoadEditSiteData(editsiteid.val(),editsitedate.val(),editsitename.val(),editsitedescription.val(),
                                          editsitewonumber.val(),editsitesupervisor.val(),editsitearea.val())
                        $( this ).dialog( "close" );
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                alleditsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#dialog-newbqqty" ).dialog({
            autoOpen: false,
            height: 350,
            width: 250,
            modal: true,
            buttons: {
                "Add Quantity": function() {
                    var bValid = true;
                    allbqitemFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( bqitemqty, "Qty", 3, 80 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
                    var decimal=  /^[0-9]+(\.[0-9]+)+$/;  
                    //bValid = bValid && checkRegexp( bqitemqty, /^[0-9]+(\.[0-9]+)+$/i, "Qty may consist of  0-9 only." );
                    //bValid = bValid && checkLength( bqitemqty, "bqitemqty", 3, 80 );
 
                    if ( bValid ) {
                        LoadXMLEditBQQty(bqitemqty.val(),bqitemprice.val())
                        $( this ).dialog( "close" );
                        return false;
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                allbqitemFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
        $( "#dialog-QuoteContract" ).dialog({
            autoOpen: false,
            height: 250,
            width: 850,
            modal: true,
            buttons: {
                "Add Quote to JCNo": function() {
                    var bValid = true;
                    //allsiteFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( sitename, "site name", 3, 120 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        //LoadNewSiteData(sitename.val(),description.val(),area.val(),wonumber.val(),supervisor.val())
                        var cont = $("#quote_contract_add").val();
                        var quote = $("#activequoteno").val();
                        var uniqid = Math.random()
                        var jqxhr = $.post("/estimatingcont/ajax3yrquoteScopeAttachContract/"+uniqid+"/"+cont+"/"+quote, function(data) {
                            })
                        $( this ).dialog( "close" );
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                //allsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#create-user" )
            .button()
            .click(function() {
                $( "#dialog-newsite" ).dialog( "open" );
            });

        $( "#create-newscope" )
            .button()
            .click(function() {
                $( "#dialog-newscope" ).dialog( "open" );
            });

        $( "#create-newquote" )
            .button()
            .click(function() {
                $( "#dialog-newquote" ).dialog( "open" );
            });

        $( "#dialog-newpurchasereqitem" ).dialog({
            autoOpen: false,
            height: 350,
            width: 250,
            modal: true,
            buttons: {
                "Add New Item To Purchase Req": function() {
                    var bValid = true;
                    allscopeFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( scopename, "site name", 3, 80 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadNewScopeData(scopename.val(),scopeunit.val(),scopeqty.val())
                        $( this ).dialog( "close" );
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                allscopeFields.val( "" ).removeClass( "ui-state-error" );
            }
        });

        $( "#dialog-new-userform" ).dialog({
            autoOpen: false,
            height: 350,
            width: 250,
            modal: true,
            buttons: {
                "Create New Site": function() {
                    var bValid = true;
                    allsiteFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( sitename, "username", 3, 16 );
                    bValid = bValid && checkLength( email, "email", 6, 80 );
                    bValid = bValid && checkLength( password, "password", 5, 16 );
 
                    bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                    // From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
                    bValid = bValid && checkRegexp( email, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i, "eg. ui@jquery.com" );
                    bValid = bValid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );
 
                    if ( bValid ) {
                        $( "#users tbody" ).append( "<tr>" +
                            "<td>" + sitename.val() + "</td>" + 
                            "<td>" + email.val() + "</td>" + 
                            "<td>" + password.val() + "</td>" +
                        "</tr>" ); 
                        LoadNewSiteData(sitename.val(),email.val(),password.val())
                        $( this ).dialog( "close" );
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                allsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
    });

(function( $ ) {
    $.widget( "ui.combobox", {
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
                        loadXMLSingleContract(ui.item.option.value)
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
})( jQuery );

$(function() {
    $( "#combobox" ).combobox();
    $( "#toggle" ).click(function() {
        $( "#combobox" ).toggle();
    });
});
$(function() {
        var sitename = $( "#sitename" ),
            description = $( "#description" ),
            orderno = $( "#orderno" ),
            clientname = $( "#clientname" ),
            orderdate= $( "#orderdate" ).datepicker();
            $( "#orderdate" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
            contact= $( "#contact" ),

            allsiteFields = $( [] ).add( sitename ).add( description ).add( orderno ).add( clientname).add(orderdate).add(contact);
            tips = $( ".validateSiteTips" );
            activesiteid = $("#activesiteid"),

            editsitename = $("#editsitename");
            editsiteclientname = $("#editsiteclientname");
            editsiteorderno = $("#editsiteorderno");
            editsiteorderdate = $("#editsiteorderdate").datepicker();
            $("#editsiteorderdate" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
            editsitecontact= $( "#editsitecontact" ),
            editsitecompleted= $( "#editsitecompleted" ),
            editsitedescription = $("#editsitedescription");
            editsitejcno = $("#editsitejcno");

            editscopename = $( "#editscopename" ),
            editscopeunit = $( "#editscopeunit" ),
            editscopeqty = $( "#editscopeqty" ),

            scopeqty = $( "#scopeqty" ),
            scopename = $( "#scopename" ),
            scopeunit = $( "#scopeunit" ),
            
            poitems = $("#item"),
            podescription = $("#item_description"),
            pounit = $("#unit"),
            poqty = $("#qty"),
            poprice = $("#price"),
            pototal = $("#total"),

            editpoid = $("#edit_id"),
            editpoitems = $("#edit_item"),
            editpodescription = $("#edit_item_description"),
            editpounit = $("#edit_unit"),
            editpoqty = $("#edit_qty"),
            editpoprice = $("#edit_price"),
            editpototal = $("#edit_total"),

            allorderitemsFields = $( [] ).add( poitems ).add( podescription ).add(pounit  ).add(poqty  ).add(poprice ).add(pototal  ),
            alledititemFields = $( [] ).add(editpoid ).add(editpoitems ).add( editpodescription ).add(editpounit  ).add(editpoqty  ).add(editpoprice  ).add(editpototal  ),
            alleditsiteFields = $( [] ).add( editsitename ).add( editsitejcno ).add( editsitedate ).add( editsiteorderdate ).add( editsitedescription ).add( editsiteclientname ).add( editsiteorderno ),
            tips = $( ".validateScopeTips" );
            bqitemqty = $( "#bqitemqty" ),
            allbqitemFields = $( [] ).add( bqitemqty ),
            tips = $( ".validateBQItemTips" );
            productionstaff = $("#productionstaff");
            $( "#sitename" ).css("width","300px");
            $( "#sitename" ).css("width","300px");
            $( "#description" ).css("width","300px");
            $( "#clientname" ).css("width","300px");
            $("#edit_item_description").css("width","300px");
            $("#item_description").css("width","300px");

            contact= $( "#contact" )
 
        function updateTips( t ) {
            tips
                .text( t )
                .addClass( "ui-state-highlight" );
            setTimeout(function() {
                tips.removeClass( "ui-state-highlight", 1500 );
            }, 500 );
        }
 
        function checkLength( o, n, min, max ) {
            if ( o.val().length > max || o.val().length < min ) {
                o.addClass( "ui-state-error" );
                updateTips( "Length of " + n + " must be between " +
                    min + " and " + max + "." );
                return false;
            } else {
                return true;
            }
        }
 
        function checkRegexp( o, regexp, n ) {
            if ( !( regexp.test( o.val() ) ) ) {
                o.addClass( "ui-state-error" );
                updateTips( n );
                return false;
            } else {
                return true;
            }
        }
        $( "#create-newcontract" )
            .button()
            .click(function() {
                $( "#dialog-newcontract" ).dialog( "open" );
            });
        $( "#create-neworderitem" )
            .button()
            .click(function() {
                $( "#dialog-addorderitem" ).dialog( "open" );
            });
        $( "#dialog-newcontract" ).dialog({
            autoOpen: false,
            height: 590,
            width: 450,
            modal: true,
            buttons: {
                "Create New Contract": function() {
                    var bValid = true;
                    allsiteFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( sitename, "site name", 3, 16 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadNewContractData(sitename.val(),description.val(),orderno.val(),clientname.val(),orderdate.val(),contact.val())
                        $( this ).dialog( "close" );
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                allsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
        $( "#dialog-editcontract" ).dialog({
            autoOpen: false,
            height: 790,
            width: 500,
            modal: true,
            buttons: {
                "Edit Contract": function() {
                    var bValid = true;
                    alleditsiteFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( sitename, "site name", 3, 16 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadEditContractData(editsitejcno.val(),editsitename.val(),editsitedescription.val(),editsiteorderno.val(),
                            editsiteclientname.val(),editsiteorderdate.val(),editsitecontact.val(),editsitecompleted.val())
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
                alleditsiteFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
        $( "#dialog-addorderitem" ).dialog({
            autoOpen: false,
            height: 590,
            width: 430,
            modal: true,
            buttons: {
                "Add Order Items": function() {
                    var bValid = true;
                    allorderitemsFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( podescription, "Description", 3, 16 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
 
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
 
                    if ( bValid ) {
                        LoadNewOrderItem(activesiteid.val(),poitems.val(),podescription.val(),pounit.val(),alltrim(poqty.val()),alltrim(poprice.val()),alltrim(pototal.val()));
                        $( this ).find('input').val('');
                        $( this ).dialog( "close" );
                        return false;
                    }
                },
                Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                allorderitemsFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
        $( "#dialog-editorderitem" ).dialog({
            autoOpen: false,
            height: 650,
            width: 430,
            modal: true,
            buttons: {
                "Edit Order Items": function() {
                    var bValid = true;
                    alledititemFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( podescription, "Description", 3, 16 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                    var uniq = Math.random()
                    if ( bValid ) {
                        LoadEditOrderItem(uniq,editpoid.val(),activesiteid.val(),editpoitems.val(),editpodescription.val(),editpounit.val(),alltrim(editpoqty.val()),alltrim(editpoprice.val()),alltrim(editpototal.val()));
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
                alledititemFields.val( "" ).removeClass( "ui-state-error" );
            }
        });
        $( "#combotruefalse" ).click(function() {
            $( "#editsitecompleted" ).val( this.value);
            return false;
        });
        $( "#combocidbrating" ).click(function() {
            $( "#editsitecidbrating" ).val( this.value);
            return false;
        });
        $( "#combocidbcategory" ).click(function() {
            $( "#editsitecidbcategory" ).val( this.value);
            return false;
        });
        $( "#combositeworkcategory" ).click(function() {
            $( "#editsiteworkcategory" ).val( this.value);
            return false;
        });
        $( "#effectbutton" ).click(function() {
            $( "#effect" ).addClass( "newClass", 1000, callbackbutton );
            return false;
        });
        function callbackbutton() {
            setTimeout(function() {
                $( "#effect" ).removeClass( "newClass" );
            }, 1500 );
        }
        $( "#dialog-staffphotos" ).dialog({
            autoOpen: false,
            height: 650,
            width: 730,
            modal: true,
            buttons: {
                "Get Selected People": function() {
                    var bValid = true;
                    alledititemFields.removeClass( "ui-state-error" );
                    //bValid = bValid && checkLength( podescription, "Description", 3, 16 );
                    //bValid = bValid && checkLength( email, "email", 6, 80 );
                    //bValid = bValid && checkRegexp( sitename, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                    if ( bValid ) {
                        $( this ).find('input').val('');
                        $( this ).dialog( "close" );
                        return false;
                    }
                },
                Cancel: function() {
                    $( this ).find('input').val('');
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
                $( this ).find('input').val('');
                alledititemFields.val( "" ).removeClass( "ui-state-error" );
            }


        });
        $( "#thisbutton" ).click(function() {
            //$( "#droppable" ).addClass( "newClass", 1000, callbackgallery );
            openstaffphotosdialog()
        });
            return false;

    $( "#productionstaff").click(function() {
        //$( "#droppable" ).addClass( "newClass", 1000, callbackgallery );
        var person = $(this);    
        personid = person.children('div').html(),
        alert(person);
        $("#outputcalendar").load("/mngntcont/ajaxgetmanagepoints/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
            //alert("External content loaded successfully!");
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
        return false;

});

//Gallery and trash example    
$(function() {
    // there's the gallery and the trash
    var $gallery = $( "#gallery" ),
        $gallery_invoices = $( "#gallery_invoices" ),
        $trash = $( "#trash" );

    // let the gallery items be draggable
    $( "li", $gallery ).draggable({
        cancel: "a.ui-icon", // clicking an icon won't initiate dragging
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        containment: "document",
        //helper: "clone",
        cursor: "move"
    });
    // let the gallery items be draggable
    $( "li", $gallery_invoices ).draggable({
        cancel: "a.ui-icon", // clicking an icon won't initiate dragging
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        containment: "document",
        //helper: "clone",
        cursor: "move"
    });

    // let the trash be droppable, accepting the gallery items
    $trash.droppable({
        accept: "#gallery > li",
        activeClass: "ui-state-highlight",
        drop: function( event, ui ) {
            //deleteImage( ui.draggable );
        }
    });

    // let the gallery be droppable as well, accepting items from the trash
    $gallery.droppable({
        accept: "#trash li",
        activeClass: "custom-state-active",
        drop: function( event, ui ) {
            //recycleImage( ui.draggable );
        }
    });
    $gallery_invoices.droppable({
        accept: "#trash li",
        activeClass: "custom-state-active",
        drop: function( event, ui ) {
            //recycleImage( ui.draggable );
        }
    });
    $( "li", $gallery ).click(function(event) {
        //$( "#droppable" ).addClass( "newClass", 1000, callbackgallery );
        var target = $( event.target );
        var person = $(this);    
        personid = person.children('div').html(),
        $("#outputcalendar").load("/mngntcont/ajaxgetmanagepoints/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
    $( "li", $gallery_invoices ).click(function(event) {
        var target = $( event.target );
        var person = $(this);    
        personid = person.children('div').html(),
        $("#outputcalendar").load("/mngntcont/ajax_invoices_per_point/"+personid,function(responseTxt,statusTxt,xhr){
          if(statusTxt=="success")
            //alert("External content loaded successfully!");
          if(statusTxt=="error")
            alert("Error: "+xhr.status+": "+xhr.statusText);
        });
            return false;
    });
        return false;


    function callbackgallery() {
        setTimeout(function() {
            $( "#droppable" ).removeClass( "newClass" );
        }, 1500 );
    }

    // image deletion function
    var recycle_icon = "<a href='link/to/recycle/script/when/we/have/js/off' title='Recycle this image' class='ui-icon ui-icon-refresh'>Recycle image</a>";
    function deleteImage( $item ) {
        $item.fadeOut(function() {
            var $list = $( "ul", $trash ).length ?
                $( "ul", $trash ) :
                $( "<ul class='gallery ui-helper-reset'/>" ).appendTo( $trash );

            $item.find( "a.ui-icon-trash" ).remove();
            $item.append( recycle_icon ).appendTo( $list ).fadeIn(function() {
                $item
                    .animate({ width: "48px" })
                    .find( "img" )
                        .animate({ height: "36px" });
            });
        });
    }

    // image recycle function
    var trash_icon = "<a href='link/to/trash/script/when/we/have/js/off' title='Delete this image' class='ui-icon ui-icon-trash'>Delete image</a>";
    function recycleImage( $item ) {
        $item.fadeOut(function() {
            $item
                .find( "a.ui-icon-refresh" )
                    .remove()
                .end()
                .css( "width", "96px")
                .append( trash_icon )
                .find( "img" )
                    .css( "height", "72px" )
                .end()
                .appendTo( $gallery )
                .fadeIn();
        });
    }

    // image preview function, demonstrating the ui.dialog used as a modal window
    function viewLargerImage( $link ) {
        var src = $link.attr( "href" ),
            title = $link.siblings( "img" ).attr( "alt" ),
            $modal = $( "img[src$='" + src + "']" );

        if ( $modal.length ) {
            $modal.dialog( "open" );
        } else {
            var img = $( "<img alt='" + title + "' width='384' height='288' style='display: none; padding: 8px;' />" )
                .attr( "src", src ).appendTo( "body" );
            setTimeout(function() {
                img.dialog({
                    title: title,
                    width: 400,
                    modal: true
                });
            }, 1 );
        }
    }

    // resolve the icons behavior with event delegation
    $( "ul.gallery > li" ).click(function( event ) {
        var $item = $( this ),
            $target = $( event.target );

        if ( $target.is( "a.ui-icon-trash" ) ) {
            deleteImage( $item );
        } else if ( $target.is( "a.ui-icon-zoomin" ) ) {
            viewLargerImage( $target );
        } else if ( $target.is( "a.ui-icon-refresh" ) ) {
            recycleImage( $item );
        }

        return false;
    });
});
//draggable example
$(function() {
        $( "#draggable" ).draggable();
        $( "#droppable" ).droppable({
            drop: function( event, ui ) {
                $( this )
                    .addClass( "ui-state-highlight" )
                    .find( "p" )
                        .html( "Dropped!" );
            }
        });
    });

$(document).ready(function(){
    $("#dvClickme").bind('click', function(){
        alert('You clicked me..');
    });

    $("#btnClone").bind('click', function(){
       $('#dvClickme').clone(true).appendTo('body');
    });

    $('#copy-correct')
              .append($('#orig .elem')
              .clone()
              .children('a')
              .prepend('bar - ')
              .end()); 
    function log( message ) {
        $( "<div>" ).text( message ).prependTo( "#log" );
        $( "#log" ).scrollTop( 0 );
        };

    var cache = {};
    $( "#req_description" ).autocomplete({
            source: "/logisticscont/search_supplier_items/"+'2',
            minLength: 3,
            autocomplete: true,
            //matchContains: true,
            select: function( event, ui ) {
                log( ui.item ?
                    "Selected: " + ui.item.value + " aka " + ui.item.id :
                    "Nothing selected, input was " + this.value );
            },
            response: function( event, ui ) {
                //alert(response)
                log( ui.item ?
                    "Selected: " + ui.item.value + " aka " + ui.item.id :
                    "Nothing selected, input was " + this.value );
            }
    });
});    
//Code Ends           ​
