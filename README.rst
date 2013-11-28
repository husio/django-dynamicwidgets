======================
Django Dynamic Widgets
======================


Django dynamic widgets is a library that allow you to define HTML and expose
chunks, that will be load on page using XHR request.

There are few reasons why would you want to do this. The most obvious are:

* caching the whole page while still displaying *hello **username** * in the
  top right corner,
* load content only on certain actions - user clicked or hovered on certain
  element


Installation
------------

Make sure that `django.contrib.staticfiles` is set up properly and add
`dynamicwidgets` to your `INSTALLED_APPS` setting::

    INSTALLED_APPS = (
        # ...
        'django.contrib.staticfiles',
        # ...
        'dynamicwidgets',
    )


URL configuration
~~~~~~~~~~~~~~~~~

To autodiscover your widget routing, you have to import all your handlers.
This can be done using `dynamicwidgets.handlers.default.autodiscover()`. After
that, you have to place handler view somewhere in the urls tree. Good place
might be applications `urls.py` file::

    from dynamicwidgets import handlers

    handlers.default.autodiscover()

    urlpatterns = patterns('',
        # ...
        url(r'^dynamicwidgets/', include('dynamicwidgets.urls')),
    )

Javascript setup
~~~~~~~~~~~~~~~~

Dynamic widgets library is using javascript to dynamicly load HTML chunks and
depends on jQuery.

On page that you will use dynamic widges, include both jQuery and dynamic
widges libraries::


    {# include jQuery #}
    <script src="{% static "dynamicwidgets/js/dynamicwidgets.js" %}" type="text/javascript"></script>

In addition, **before** including above libraries, preferably in `<head>` tag,
specify path to widgets view::

    <script type="text/javascript">window.DYNAMIC_WIDGETS_URL = '{% url "dynamicwidgets.widgets" %}';</script>


Usage
-----

To use a widget, you have to define handler that will build and return a
content and a tag in the HTML document that content will be load into.

Widget handler
~~~~~~~~~~~~~~

Widget handler is a function that always takes two parameters - `request` and
a list of `widgets`. To define a handler, decorate it with
`dynamicwidgets.decorators.widget_handler`::


    from articles.models import Article
    from dynamicwidgets.decorators import widget_handler


    @widget_handler(r'^user-name$')
    def user_name(request, widgets):
        if request.user.is_anonymous():
            return {'user-name': {'html': 'anonymous'}}
        return {'user-name': {'html': request.user.username}}


Every handler should return a dictionary, where keys are widget names and
values are dictionaries. If value dictionary contains `html` key, it's value
will be rendered on page as widget content.


For performance reasons, all widget matches are aggregated and within single
request and every widget handler is called not more than once. Because of
that, you can save some queries to the database::

    @widget_handler(r'^article-details:(?P<art_id>\d+)$')
    def article_details(request, widgets):
        articles = Article.objects.filter(
            id__in=[w.params.art_id for w in widgets])
        article_by_id = {art.id: art for art in articles}

        response = {}
        for widget in widgets:
            article = article_by_id[int(widget.params.art_id)]
            html = '<h1>article {}: {}</h1>'.format(article.id, article.title)
            response[widget.wid] = {'html': html}
        return response


Every `widget` object contains two attributes:

* `wid` that holds the name of the widget, mached by regular expression which
  view was decorated with
* `params` holding zero or more parameters extracted from decorator's regular
  expression


HTML attributes
~~~~~~~~~~~~~~~

Whenever you want to use a widget, add `dw` attribute to an element. Those can
be:

* `dw-load` for widgets that should be loaded once the document is ready,
* `dw-click` for widgets that should be loaded on `click` event,
* `dw-hover` for widgets that should be loaded on `mouseover` event.

Using them can be as simple as::

    <div class="header">
        <span class="userinfo" dw-load="user-name"></span>
    </div>
    <div class="content">
        <span class="article" dw-click="article:1">click to show article<span>
        <span class="article" dw-hover="article:2">hover to show article<span>
    </div>

In addition, you can add `dw-once` attribute, to make sure widget content will
be fetched only once::

        <span class="article" dw-hover="article:2" dw-once>hover to show article<span>

But simple replacing of the content might not be enough. That's why full
format of the attribute value can be build using multiple chunks, separated by
comma character::

    dw-<action>="<widget name>,<insert method>,<destination selector>"

* `<widget name>` is used to match handler function. That's the only required
  part of the value string,
* `<insert method>` is any valid jQuery input method like `html`, `append`,
  `prepend`. Default value is `html`,
* `<destination selector>` is sizzle selector with one addition. Selector
  starting with `@` character is always narrowed to element that `dw`
  attribute was declarated. Default value is `@`.

Knowing all above, it's easy to make dropdown menu with dynamic content load::


    <style type="text/css">
        .dropdown-menu .menu-items       {display: none;}
        .dropdown-menu:hover .menu-items {display: block;}
    </style>

    <div class="dropdown-menu" dw-hover="article-attributes:3,html,@.menu-items" dw-once>
        Menu
        <span class="menu-items">
            Loading...
        </span>
    </div>
