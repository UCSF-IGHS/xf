/**
 * Created by fitti on 21/07/16.
 */

// this function binds all ajax-autoload controls and loads their widget content
function bindAjax() {

    $('.uh-ajax-autoload').each(function() {
        $(this).load($(this).attr('widget-url')+ "");

    });

    setTimeout(function(){
      $('.loading-indicator').html("We're sorry, but this component failed to load. Please try again later.");
        //alert($('.loading-indicator'))
    }, 5000);


   /* The following is legacy code that needs to be merged with the above. It is currently used by XF_CRUD
     */

    $(".mxlform").submit(function() {
        event.preventDefault();
        //alert ("MXLFORM SUBMIT");
        //postform(event.target)   // COMMENTED TO AVOID SOME ERROR BUT NOT RESOLVED
    });

    // This binds all the GET forms
    $(".mxlget").unbind('submit.mxlget').bind('submit.mxlget', function() {
        event.preventDefault();
        getform(event.target);
    });

    // This binds all the AJAX links
    $(".mxlajax").unbind('click.mxlajax').bind('click.mxlajax', function() {
        event.preventDefault();
        gethtml($(this));
    });

    $(".mxl-autocomplete").blur(function() {
        event.preventDefault();
        autocomplete_leave($(this));
    });

    $(".mxl-get-query").blur(function() {
        event.preventDefault();
        get_query($(this));
    });

    $('#frmDlg').on('hidden.bs.modal', function () {
        $('#frmDlgHtml').html("Loading...");
        $('#frmDlgHtml').removeAttr('style');
    })

   // This snippet is executed during the popup of a modal window.
    // It will automatically load a piece of HTML (url href attribute) into the specified target (html-target
    // attribute)
    $("a[data-toggle=modal]").unbind("click"); // removes previous click to prevent multiple loading
    $("a[data-toggle=modal]").click(function (e) {

        var htmltarget = $(this).attr('html-target')
        var formtarget = $(this).attr('data-target')
        var url = CreateAJAXURL($(this).attr('href')); // ensures that Django loads the AJAX version of this page

        // This is a hack. The href is used to both pop a modal window, and to find the POST URL for a modal window.
        // For a popup in a popup this doesn't work... so a new attribute hrefpost has been introduced to resolve
        // this.
        if ($(this).attr('hrefpost') != null)
            url = CreateAJAXURL($(this).attr('hrefpost'));

        // Ensure that the new form is bound to the submit event and load the FORM based on the
        // URL parameter
        $(htmltarget).load(url, function() {
            ajaxFormLoaded(htmltarget, formtarget, url, e);
            bindAjax();
        });

    })

    // Set up the search field to clear after clicking the Clear button
    $("#lnkClear").unbind('click.lnkclear').bind('click.lnkclear', function(){ $("#txtSearchString").val(""); });

    /* Clickable table rows and cells */
    /* Cells work better when using drop down buttons in the row */
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
    $(".clickable-cell").click(function() {
        window.location = $(this).data("href");
    });


    /* MissingTextInput Widget –bind to the checkboxes */
    $(".xf-unknown-checkbox").change( function(){
        UnknownCheckBoxChange($(this));
    });

}



function ajaxFormLoaded(htmltarget, formtarget, posttarget, sourceElement) {
    // This function fires when a HTML AJAX FORM is loaded. It binds the form to the submit event,
    // to enable routing to the AJAX processor

    // If a validator is available through a form asset, attach to it
    if (typeof attach_validator == 'function') {
        attach_validator($(".mxlform"), htmltarget, formtarget, posttarget);
    }

    // Otherwise, we will handle it ourselves
    else {

        hideMessages();
        $(".mxlform").submit(function (event) {
            // Executed when the form is being submitted
            event.preventDefault();

            postform(event, htmltarget, formtarget, posttarget, sourceElement);

            $("#btnDlgSubmit", this)
                  .val("Please wait")
                  .attr('disabled', 'disabled');
            return true;
        });

        // Disable the submit button once clicked
        $("#btnDlgSubmit").click(function () {
            var form = document.getElementById("frmAjax");
            if (!form.checkValidity()){
                $("#btnDlgSubmit").val("Try again");
                $("#btnDlgSubmit").removeAttr("disabled");
                var panels = $("#frmAjax").find(".panel-collapse");
                panels.each(function (indeX, nodE) {
                    var has_errors = 0;
                    $("#" + nodE.id).find(":invalid").each(function (index, node) {
                        has_errors ++;
                    });
                    if(has_errors > 0){
                        panels.each(function (index, node) {
                            var expanded = $("#" + node.id).is(":visible");
                            if (indeX === index){
                                if (expanded === false){
                                    $("#" + node.id).collapse("toggle");
                                }
                            }else{
                                if (expanded === true){
                                    $("#" + node.id).collapse("toggle");
                                }
                            }
                        });
                        return false;
                    }
                });
            }
        });
    }

    /* TODO: THe date picker doesn't work
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd'
    });
    */
}

function postform(e, htmltarget, formtarget, posttarget, sourceElement) {
    var serializedData = $('#frmAjax').serialize();

    $.ajax({
        url: posttarget,
        type: "post",
        data: serializedData,
        cache: 'false',
        dataType: "json",
        async: 'true',

        success: function(data) {
            //var errors = jQuery.parseJSON(data);
            //var errors = data;

            // Not successful – reload the window and display any problems
            if (!data.success) {
                $(htmltarget).html(data.html);
                ajaxFormLoaded(htmltarget, formtarget, posttarget, sourceElement);
                bindAjax();
            }
            else {
                $(htmltarget).html("Loading");
                $(formtarget).modal('hide') // dismiss dialog
                // alert(data.pk);

                //$('#msg_info').html(data.message);
                //$('#msg_info').show();

                new PNotify({
                      title: 'Done',
                      text: data.message,
                      type: 'success',
                      styling: 'bootstrap3'
                  });

                if(typeof window.mxlSuccess == 'function') {
                    // function exists, so we can now call it
                    mxlSuccess();

                    // Refresh the object list for the link that triggered this action
                    object_list = $(sourceElement.target).attr('object_list');
                    if (object_list)
                        if ($(object_list).length > 0)
                            RefreshObjectListForDiv($(object_list));

                }

                // If the XFAction has a next_url, we should find it, add the recently modified or created
                // object ID, and load that page.
                // The 0 is used for scenarios where pk is not known in advance, so the 0 will be replaced by the pk
                var nextUrl = $(sourceElement.target).attr('data-next-url');
                if (nextUrl)
                    window.location = nextUrl.replace("/0/", "/" + data.pk + "/");

            }
        },
        error:function(jqXHR, exception) {
            $("#btnDlgSubmit").val("Try again");
            $("#btnDlgSubmit").removeAttr("disabled");

            var msg = '';
            if (jqXHR.status === 0) {
                msg = 'We are sorry, we could not connect to the server. Please check your internet connection.';
            } else if (jqXHR.status == 404) {
                msg = 'We are sorry, your request could not be completed.';
            } else if (jqXHR.status == 500) {
                msg = 'We are sorry, something went wrong on the server, and we could not connect to it.';
            } else if (exception === 'parsererror') {
                msg = 'We are sorry, the server sent something that we could not understand.';
            } else if (exception === 'timeout') {
                msg = 'We are sorry, your request has timed out, try again.';
            } else if (exception === 'abort') {
                msg = 'We are sorry, your request has been aborted, try again.';
            } else {
                msg = 'We are sorry, an unknown error has occurred.';
            }
            alert(msg);
        },
        complete: function() {
            $("#btnDlgSubmit").val("Try again");
            $("#btnDlgSubmit").removeAttr("disabled");
        }
    });
}

function getform(e) {
    var form = $("#" + e.id);
    var url = CreateAJAXURL(form.attr('action'));
    var htmlTarget = form.attr('html-target');
    $.ajax({
        type: "GET",
        url: url,
        data: $("#" + e.id).serialize(), // serializes the form's elements.
        success: function(data)
        {
            $("#" + htmlTarget).html(data);
            bindAjax();
        }
    });
}

function gethtml(source) {

    var htmlTarget = source.attr('html-target');
    var url = CreateAJAXURL(source.attr('href'));

    $("#" + htmlTarget).load(url, function() {
        // Always rebind after loading HTML
        bindAjax();
    });
}


function LoadHTMLIntoDiv(url, divTarget) {

    // Add ?ajax/&ajax depending on link in the href
    url = CreateAJAXURL(url);

    divTarget.load(url, function() {
        // Always rebind after loading HTML
        bindAjax();
    });
}

function autocomplete_leave2(source2) {

    var availableTags = ["ActionScript", "AppleScript", "Asp", "BASIC", "C", "C++", "Clojure", "COBOL", "ColdFusion", "Erlang", "Fortran", "Groovy", "Haskell", "Java", "JavaScript", "Lisp", "Perl", "PHP", "Python", "Ruby", "Scala", "Scheme"];
    $("#" + source2.attr('id')).autocomplete({
        source: availableTags
    });
}

function autocomplete_leave(source) {

    var apicall = source.attr('mxl_api_call');
    var param = source.attr('mxl_param');
    //alert(apicall + param);
    var data = {};

    data[param] = source.val();
    $.get(apicall, data,
        function(data)
        {
            var id = "#" + source.attr('id');
            $(id + "_fb").html(data.Message)
            if (data.Success)
                $(id + "_ind").attr('class', 'icon-ok');
            else
                $(id + "_ind").attr('class', 'icon-ban-circle');
        }
    );
}

function get_query(source) {

    var apicall = source.attr('mxl_api_call');
    var param = source.attr('mxl_param');
    var mxl_return_value_target = source.attr('mxl_return_value_target');
    //alert(apicall + param);
    var data = {};

    //data[param] = source.val();
    data['visit_type'] = 1;
    data['visit_date'] = 2013;
    var form = source.closest("form");
    var serializedData = form.serialize();

    $.ajax({
        url: apicall,
        type: "get",
        data: serializedData,
        cache: 'false',
        dataType: "json",
        async: 'true',

        success: function(data) {
            //alert(data.return_value);
            target_value = $("[name='" + mxl_return_value_target + "']").val(data.return_value);
        },
        error:function(data) {
            var errors = jQuery.parseJSON(data);
            //alert(JSON.stringify(data));
            alert("Could not connect to the server. Your request could not be proccessed.")
        }
    });

    /*
    $.get(apicall, data,
        function(data)
        {
            //alert(data)
            //var id = "#" + source.attr('id');
            //$(id + "_fb").html(data.Message)
            if (data.Success)
                //$(id + "_ind").attr('class', 'icon-ok');
                alert(data.return_value);
            //else
                //$(id + "_ind").attr('class', 'icon-ban-circle');
        }
    );*/
}


function showInfo(message) {
    hideMessages();
    $('#msg_info').html(message);
}

function showError(message) {
    hideMessages();
    $('#msg_error').html(message);
}

function hideMessages() {
    $('#msg_error').hide();
    $('#msg_info').hide();
}




/* Setting a URL */
function selectURL(url) {
    var no_current_page = $SIDEBAR_MENU.find('.current-page');

    if (no_current_page.length == 0) {
        $SIDEBAR_MENU.find('a[href="' + url + '"]').closest("ul").closest("li").find("> a").trigger("click");
        $SIDEBAR_MENU.find('a[href="' + url + '"]').closest("li").addClass("current-page");
    }
}



/* Friendly, new functions */

function RefreshObjectList(url) {

    LoadHTMLIntoDiv(url, $('#ctxObjectList'));

}

function RefreshObjectListForDiv(div) {

    var url = div.attr('href');
    LoadHTMLIntoDiv(url, div);
}

function CreateAJAXURL(url){

    if (url.indexOf("?") == -1)
        url = url + "?ajax";
    else
        url = url + "&ajax";

    return url;
}

function CreateEmbedURL(url) {

    if (url.indexOf("?") == -1)
        url = url + "?embed";
    else
        url = url + "&embed";

    return url;

}


// Checks whether a validation blah
function UnknownCheckBoxChange(checkbox) {

    var inputField = $("#" + $(checkbox).attr('xf_blank_control'));
    var datePickerBtn = $("#" + $(checkbox).attr('xf_datepicker_button'));
    if( $(checkbox).is(':checked') ) {
        //alert(inputField);
        inputField.val("")
        //inputField.prop('required',false);
        inputField.prop('disabled',true);
        datePickerBtn.addClass('disabled');
    }
    else {
        inputField.val("")
        //inputField.prop('required',true);
        inputField.prop('disabled',false);
        datePickerBtn.removeClass('disabled');
    }
}

