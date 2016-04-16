import inspect
from routes import Mapper
from routes.util import URLGenerator
from routes import request_config
from tg import TGController, abort, TGApp, redirect
from tg.decorators import Decoration
from tg.exceptions import HTTPFound
from tg.util import Bunch

from .decorators import route as route_decorator


class RoutedController(TGController):
    """Routes requests according to a routes mapper.

    Routing are resolved through a ``mapper`` attribute of
    the controller, usually you want to provide a ``mapper``
    class attribute inside your subclass and register the
    routes there.

    Additional routes can be registered also using @route
    decorator on top of controller methods.

    In case no mapper is provided or no route is resolved
    the dispatch proceed with standard TG object dispatch
    unless the ``disable_objectdispatch`` attribute of the
    controller is set to ``True``.

    RoutedController also provides a ``method_override``
    class attribute to turn on/off the possibility to override
    `REQUEST_METHOD` through `?_method=` url parameter
    to conveniently perform other type of requests in some
    conditions.
    """
    disable_objectdispatch = False
    mapper = None
    method_override = False

    def __init__(self, *args, **kw):
        super(RoutedController, self).__init__(*args, **kw)

        routes = []
        for name in dir(self):
            value = getattr(self.__class__, name, None)
            if value is None:
                continue

            deco = None
            if inspect.ismethod(value):  # pragma: no cover
                # PY2
                deco = Decoration.get_decoration(value.__func__)
            elif inspect.isfunction(value):  # pragma: no cover
                # PY3
                deco = Decoration.get_decoration(value)

            if deco is None:
                continue

            if hasattr(deco, '_tgext_routes'):
                routes.extend(deco._tgext_routes)

        if routes:
            instance_mapper = Mapper()
            if self.mapper is not None:
                instance_mapper.extend(self.mapper.matchlist)
            instance_mapper.extend(routes)
            self.mapper = instance_mapper

    def _dispatch(self, state, remainder=None):
        if self.mapper is None:
            return super(RoutedController, self)._dispatch(state, remainder)

        if state.controller is not self:
            # This happens when crank _dispatch_controller tries to use parent
            # controller _dispatch method for a subcontroller that
            # doesn't provide its own _dispatch function
            # (IE doesn't inherit from ObjectDispatcher).
            return super(RoutedController, self)._dispatch(state, remainder)

        environ = state.request.environ

        url = environ['PATH_INFO']
        if len(state.controller_path) > 1:
            # In case we are a subcontroller only dispatch over the remaining URL part.
            url = '/' + '/'.join(remainder)

        if self.method_override is True:
            # routes middleware overrides methods using _method param.
            if environ['REQUEST_METHOD'] == 'GET' and '_method' in state.request.GET:
                environ['REQUEST_METHOD'] = state.request.GET['_method'].upper()
            elif environ['REQUEST_METHOD'] == 'POST' and '_method' in state.request.POST:
                environ['REQUEST_METHOD'] = state.request.POST['_method'].upper()

        results = self.mapper.routematch(url, environ)
        if results:
            route_match, route = results[0], results[1]
        else:
            route_match, route = {}, None

        tg_context = environ['tg.locals']

        routes_config = request_config()
        if hasattr(routes_config, 'using_request_local'):
            routes_config.request_local = lambda: tg_context.request.routes_local

        if ('HTTPS' in environ or environ.get('wsgi.url_scheme') == 'https' or
            environ.get('HTTP_X_FORWARDED_PROTO') == 'https'):
            protocol = 'https'
        else:
            protocol = 'http'

        tg_context.request.routes_local = Bunch(
            mapper=self.mapper,
            host=environ['HTTP_HOST'],
            protocol=protocol,
            redirect=redirect
        )

        urlgen = URLGenerator(self.mapper, environ)
        environ['routes.url'] = urlgen
        environ['pylons.routes_dict'] = route_match
        environ['tg.routes_dict'] = route_match
        environ['wsgiorg.routing_args'] = (urlgen, route_match)
        environ['routes.route'] = route

        if route and route.redirect:
            # So far we only emit redirect, it should actually emit according to
            # route.redirect_status.
            route_name = '_redirect_%s' % id(route)
            raise HTTPFound(location=urlgen(route_name, **route_match))

        if not route_match:
            if not self.disable_objectdispatch:
                return super(RoutedController, self)._dispatch(state, remainder)
            else:
                abort(404)

        route_match = route_match.copy()
        config = tg_context.config

        controller_name = route_match.pop('controller', None)
        if not controller_name:
            abort(404)

        if controller_name == route_decorator.CURRENT_CONTROLLER:
            controller = self
        else:
            controller_class = TGApp.lookup_controller(config, controller_name)
            controller = controller_class()
            state.add_controller(controller_name, controller)

        action_name = route_match.pop('action', 'index')
        action = getattr(controller, action_name)

        state.set_action(action, [])
        state.set_params(route_match)
        return state

