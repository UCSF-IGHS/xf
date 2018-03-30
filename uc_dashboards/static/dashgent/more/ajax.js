/**
 * Created by fitti on 12/07/16.

 */


function bindAjax() {


    // This binds all the POST forms
    $(".ucsfform").submit(function() {
        event.preventDefault();
        //alert ("ucsfFORM SUBMIT");
        //postform(event.target)   // COMMENTED TO AVOID SOME ERROR BUT NOT RESOLVED
    });

    // This binds all the GET forms
    $(".ucsfget").submit(function() {
        event.preventDefault();
        getform(event.target);
    });

    // This binds all the AJAX links
    $(".ucsfajax").click(function() {
        event.preventDefault();
        gethtml($(this));
    });

    $(".ucsf-autocomplete").blur(function() {
        event.preventDefault();
        autocomplete_leave($(this));
    });

    $(".ucsf-get-query").blur(function() {
        event.preventDefault();
        get_query($(this));
    });


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

    /* End Legacy Code */

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
            bindAjax();
        });

    })
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
        alert($("#" + htmlTarget));

        //bindAjax();
    });
}