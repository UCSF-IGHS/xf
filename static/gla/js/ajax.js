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
    $(".mxlget").submit(function() {
        event.preventDefault();
        getform(event.target);
    });

    // This binds all the AJAX links
    $(".mxlajax").click(function() {
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
    $("a[data-toggle=modal]").click(function (e) {

        var htmltarget = $(this).attr('html-target')
        var formtarget = $(this).attr('data-target')
        var url = $(this).attr('href') + "?ajax";

        // This is a hack. The href is used to both pop a modal window, and to find the POST URL for a modal window.
        // For a popup in a popup this doesn't work... so a new attribute hrefpost has been introduced to resolve
        // this.
        if ($(this).attr('hrefpost') != null)
            url = $(this).attr('hrefpost') + "?ajax";

        // Ensure that the new form is bound to the submit event and load the FORM based on the
        // URL parameter
        $(htmltarget).load(url, function() {
            ajaxFormLoaded(htmltarget, formtarget, url);
            //bindAjax();
        });

    })

    // Set up the search field to clear after clicking the Clear button
    $("#lnkClear").click(function(){ $("#txtSearchString").val(""); });

}



function ajaxFormLoaded(htmltarget, formtarget, posttarget) {
    // This function fires when a HTML AJAX FORM is loaded. It binds the form to the submit event,
    // to enable routing to the AJAX processor

    // If a validator is available through a form asset, attach to it
    if (typeof attach_validator == 'function') {
        attach_validator($(".mxlform"), htmltarget, formtarget, posttarget);
    }

    // Otherwise, we will handle it ourselves
    else {

        hideMessages();
        $(".mxlform").submit(function () {
            // Executed when the form is being submitted
            //alert(posttarget);
            event.preventDefault();
            postform(event, htmltarget, formtarget, posttarget)
        });

        // Disable the submit button once clicked
        //alert($("#btnDlgSumbit").text());
        $("#btnDlgSubmit").click(function () {
            $("#btnDlgSubmit").val("Please wait");
        });
    }

    /* TODO: THe date picker doesn't work
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd'
    });
    */
}

function postform(e, htmltarget, formtarget, posttarget) {
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

            if (!data.success) {
                $(htmltarget).html(data.html);
                ajaxFormLoaded(htmltarget, formtarget, posttarget);
            }
            else {
                $(htmltarget).html("Loading");
                $(formtarget).modal('hide') // dismiss dialog
                $('#msg_info').html(data.message);
                $('#msg_info').show();
                if(typeof window.mxlSuccess == 'function') {
                    // function exists, so we can now call it
                    mxlSuccess();
                }
            }
        },
        error:function(data) {
            //var errors = jQuery.parseJSON(data);
            //alert(JSON.stringify(data));
            alert("Could not connect to the server. Your request could not be proccessed.")
            $("#btnDlgSubmit").val("Try again");
        }
    });
}

function getform(e) {


    var form = $("#" + e.id);
    var htmlTarget = form.attr('html-target');
    $.ajax({
        type: "GET",
        url: window.location.href + "?ajax",
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
    var url = source.attr('href');
    // Add ?ajax/&ajax depending on link in the href
    if (url.indexOf("?") == -1)
        url = url + "?ajax";
    else
        url = url + "&ajax";
    $("#" + htmlTarget).load(url, function() {
        // Always rebind after loading HTML
        bindAjax();
    });
}


function LoadHTMLIntoDiv(url, divTarget) {

    // Add ?ajax/&ajax depending on link in the href
    if (url.indexOf("?") == -1)
        url = url + "?ajax";
    else
        url = url + "&ajax";
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
    $SIDEBAR_MENU.find('a[href="' + url + '"]').closest("ul").closest("li").find("> a").trigger("click");
    $SIDEBAR_MENU.find('a[href="' + url + '"]').closest("li").addClass("current-page");
}



/* Friendly, new functions */

function RefreshObjectList(url) {

    LoadHTMLIntoDiv(url, $('#ctxObjectList'));

}