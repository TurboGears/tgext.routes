About tgext.routes
------------------

.. image:: https://travis-ci.org/TurboGears/tgext.routes.png
    :target: https://travis-ci.org/TurboGears/tgext.routes

.. image:: https://coveralls.io/repos/TurboGears/tgext.routes/badge.png
    :target: https://coveralls.io/r/TurboGears/tgext.routes

.. image:: https://img.shields.io/:license-mit-blue.svg?style=flat-square
    :target: https://pypi.python.org/pypi/tgext.routes

tgext.routes provides a simple way to integrate routes based dispatch
into TurboGears2 applications.

Installing
----------

tgext.routes can be installed both from pypi or from bitbucket::

    pip install tgext.routes

should just work for most of the users

Routing Single Actions
----------------------

Routes matching is done through the ``@route`` decorator,
each exposed method can be bound to one or multiple routes.

The only requirement is that you inherit from the ``RoutedController`` instance.

All routes registered through the ``@route`` decorator are registered starting
from the controller mount point.

The following example registers the ``entry_by_date`` method for urls like
**/date/2012-01** and **/date/2012-01-01**::

    from tgext.routes import RoutedController, route

    class DateController(RoutedController):
        @expose()
        @route('{year}-{month}', day=33)
        @route('{year}-{month}-{day}')
        def entry_by_date(self, year, month, day):
            return '%s ++ %s ++ %s' % (year, month, day)

    class RootController(BaseController):
        date = DateController()

        @expose()
        def index(self):
            return 'Hello!'

Keep in mind that as ``@expose`` wraps it, the method is still
accessible through *ObjectDispatch* routing, ``@route`` can just
register additional routes.

If there is a route pointing to it, also actions that do not provide
an ``@expose`` decoration are resolved, keep in mind that in that case
you will have to render template manually.

In case you want to disable *ObjectDispatch* you can set ``disable_objectdispatch=True``
inside the controller. Keep in mind that it will disable *ObjectDispatch* for the
whole controller and so you won't be able to dispatch actions that do not provide
a route from that controller on.

Routing Whole application
-------------------------

``RoutedController`` can also be mounted as the application *RootController*.
In that case instead of using the ``@route`` decorator you can even provide
a ``routes.Mapper`` object as controller ``mapper`` attribute and register
all the routes of your application::

    class RootController(RoutedController):
        mapper = Mapper()
        mapper.connect('/', controller='home', action='index')
        mapper.connect('/json', controller='home', action='jsonexposed')
        mapper.connect('/unex', controller='home', action='unexposed')

In this case the ``controller`` argument is required and controller will be looked
up inside the path specified by ``tg.config['paths']['controllers']``. In the previous
example a ``HomeController`` class will be looked for into the ``home.py`` module to
serve the */*, */json* and */unex* paths through its ``index``, ``jsonexposed`` and
``unexposed`` methods.

In case both a ``mapper`` attribute and ``@route`` decorator are used inside the same
``RoutedController``, the ``@route`` decorator is applied after the mapper routes.

For more documentation about routes refer to `Routes Documentation <http://routes.readthedocs.org>`_
