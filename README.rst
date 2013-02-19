About tgext.routes
-------------------------

tgext.routes provides a simple way to integrate routes based dispatch
into TurboGears2 applications through the @route decorator.

Installing
-------------------------------

tgext.routes can be installed both from pypi or from bitbucket::

    pip install tgext.routes

should just work for most of the users

Routing Actions
----------------------------

Routes matching is done through the `@route` decorator,
each exposed method can be bound to one or multiple routes.

The only requirement is that you inherit from the RoutedController instance.

The following example registers the `entry_by_date` method for urls like
`/date/2012-01` and `/date/2012-01-01`::

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

Keep in mind that tgext.routes doesn't prevent the method to be accessed
through ObjectDispatch routing, it just registers additional routes.

For more documentation about routes refer to `Routes Documentation <http://routes.readthedocs.org>`_
