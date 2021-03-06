// Create generic hide / show event listener
function createClickHideShow(selector, elem_to_hide_show){
    $(selector).click(function(){
        var checked = $(this).prop("checked")
        if(checked == true){
            $(elem_to_hide_show).show("slow");

        } else if(checked == false){
            $(elem_to_hide_show).hide("slow");
        }
    });
};
//
function checkboxCheckOptions(selector, selector_id, url_save, url_delete){
    $(selector).click(function(){
        var kwargs = 'cover_and_exclusion_type_id='+$(this).attr(selector_id);
        var checked = $(this).prop("checked")
        if(checked == true){
            $.post(url_save, kwargs, function(data){
                return false;
            });
        } else{
            $.post(url_delete, kwargs, function(data){
                return false;
            });
        };

    });
};
// Custom options for Full Calendar plugin
function createDatepicker(selector, maxDate=undefined){
    var selected = $(selector).val();
    //console.log('createDatepicker: selected -> ', selected);
    $(selector).datetimepicker({
        format: 'DD-MM-YYYY',
        date: selected,
        maxDate: maxDate,
        icons: {
            time: "now-ui-icons tech_watch-time",
            date: "now-ui-icons ui-1_calendar-60",
            up: "fa fa-chevron-up",
            down: "fa fa-chevron-down",
            previous: 'now-ui-icons arrows-1_minimal-left',
            next: 'now-ui-icons arrows-1_minimal-right',
            today: 'fa fa-screenshot',
            clear: 'fa fa-trash',
            close: 'fa fa-remove'
        },
    });
};
// Focus on first input on the page and inside a bootstrap modal
function focusOnInput(){
    // Focus on page load
    $('input:not(:disabled):not(.search_sidebar):visible:first').focus();
    // Focus on modal open
    $(document).on('shown.bs.modal', function(e) {
        $('input:visible:enabled:first', e.target).focus();
    });
    // Focus on modal close
    $(document).on('hidden.bs.modal', function(e) {
        $('input:not(:disabled):not(.search_sidebar):visible:first').focus();
    });
};

// Get Object of form data for selector
function getFormData(selector){
    var inputdict = $(selector).serializeArray();
    var outputdict = new Object;
    $.map(inputdict, function(n, i){
        outputdict[n['name']] = n['value'];
    });
    return outputdict;
};

// Custom PDF download function
function exportFile(selector, href_with_formserial, focus=true){
    $(selector).click(function(){
        $.get(href_with_formserial, function(data){
            if(focus === true){
                var win = window.open(href_with_formserial, '_blank');
                win.focus();
            }else{
                window.location = href_with_formserial;
            };
            return false;
        });
    });
};

// Custom image-not-found error handler
function ImageNotFoundHandler(selector){
    $(selector).on('error', function(){
        $(this).attr('src', '/images/nothing.png');
    });
}

// Custom dynamic window resizer
function WindowResizer(selector){
    $(window).resize(function(){
        var width = $(window).width();
        var inner_width = width - 20;
        $("body").css('width', width+'px');
        $("body").css('height', '100%');
        $(selector).css('width', inner_width + 'px');
    })
    $(window).trigger("resize");
}

// Custom options for the jquery.validate.js plugin
function setFormValidation(id) {
    $(id).validate({
        highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
            $(element).closest('.form-check').removeClass('has-success').addClass('has-danger');
        },
        success: function(element) {
            $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
            $(element).closest('.form-check').removeClass('has-danger').addClass('has-success');
        },
        errorPlacement: function(error, element) {
            $(element).append(error);
        },
        invalidHandler: function(form, validator){
            var errors = validator.numberOfInvalids();
            if(errors){
                var focus = $('input:focus').length;
                if(focus == 0){
                    validator.errorList[0].element.focus();
                };
            };
        },
    });
}
function FormIsValid(form_selector){
    return $(form_selector).valid(); // Boolean
}


function showNotification(color = 'danger', message) {
    if (color == 'danger' || 'warning') {
        type_icon = 'exclamation-circle';
    } else if (color == 'info') {
        type_icon = 'info-circle';
    } else if (color == 'success') {
        type_icon = 'check-circle';
    } else {
        type_icon = 'exclamation-circle';
    }
    $.notify({
        icon: "fa fa-" + type_icon,
        message: message

    }, {
        type: color,
        timer: 4000,
        placement: {
            from: 'top',
            align: 'right'
        }
    });
}
