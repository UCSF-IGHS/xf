# XF CRUD™
© and ™ by UCSF, UC, Global Programs and MXL

XFCrud is a framework to quickly and fast develop basic CRUD applications, 
that is applications that support basic listing, creating, editing and
deleting objects. An object is defined as a model.

## Design philosophy

The framework is designed with the following philosophy in mind:
* Reuse of code as much as possible.
* No writing of specific HTML code for a specific class. HTML is 
written for either all classes, or none at all. This ensures
that all pages look the same.
* Form definitions in code as much as possible, the framework
generates the HTML
* Builds of XFViz to ensure a proper, common design


## AJAX First™

The framework is designed with the AJAX First™ philosophy, UCSF's 
patened idea that AJAX should always come first, but if AJAX isn't
available, it should still work. This means that:

* Every create, edit, view and delete opeation will show initially
in a Bootstrap modal dialog box
* If AJAX is not enabled, the same operation will continue in a
full screen operation, navigating away from the page.

### How AJAX First™ works

AJAX first is a smart idea. But before you can understand AJAX First,
you should first understand how basic URLs work.

## URL Schemes

XF Crud can automatically generate URLs for your models. In the example,
we have three basic models: Author, Book and Category. The basic URL scheme is a follows:

http://server/myapp/model/operation

For example, in this case, the app is library, and the model is Book. 
Therefore, the following URLs will be available:

/library/Book
/library/Book/all
/library/Book/<id>edit
/library/Book/<id>delete

These URLs can be generated automatically, by using the crudurl helper
function, which is defined in `xf_crus_helpers`:
`urlpatterns += crudurl("library", "Book", Book, None)`

This statement can be included in either the urls.py of your site
or of your app. You should repeat it for all the models for which
you would like to use automatic CRUD operations.

## AJAX First™ and URLs

AJAX First generates several commands that generate model dialog
boxes, with a form view. The content of that form view is the
exact same content as the model's edit URL, minus the outside template. In
other words, when a user clicks Create new or Edit, the popup dialog
calls the /library/Book/2/edit URL, but with a special parameter in
the URL, ajax, so it becomes: `/library/Book/2/edit?ajax`. By doing
that, the framework knows that the page will be embedded within a
dialog box, and call a special base template, ajax_form.html. This
form will not contain any HTML tag other than the exact form. In
contrast, the URL without the AJAX parameter will default to the
normal template. The code responsible for this is the `XFAjaxViewMixin`
mixin, which will force any page that has ?ajax in the querystring
to be laoded using the `ajax_form.html` base template.

You can use the mixin yourself as well on views. In XF Crud, 
`XFListView`, `XFDetailView`, `XFUpdateView`, `XFCreateView` and `XFDeleteView`
all inherit from `XFAjaxViewMixin`.


