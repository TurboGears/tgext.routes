import inspect
from routes import Mapper
from routes.util import URLGenerator
from tg import TGController, abort, TGApp
from tg.decorators import Decoration
from tg.exceptions import HTTPFound


class RoutedController(TGController):
    """Routes requests according to a routes mapper.

    Routing are resolved through a ``mapper`` attribute of
    the controller, usually you want to provide a ``mapper``
    class attribute inside your subclass and register the
    routes there.

    Additional routes can be registered also using @route
    decorator on top of controller methods.

    In case no mapper is provided or no route is resolved
    the dispatch proceed with standard TG object dispatch.
    """
    mapper = None

    def __init__(self, *args, **kw):
        super(RoutedController, self).__init__(*args, **kw)

        routes = []
        for name in dir(self):
            value = getattr(self.__class__, name, None)
            if value:
                if inspect.ismethod(value):
                    deco = Decoration.get_decoration(value.__func__)
                elif inspect.isfunction(value):
                    deco = Decoration.get_decoration(value)
                else:
                    continue
                
                if hasattr(deco, '_tgext_routes'):
                    routes.extend(deco._tgext_routes)

        if routes:
            instance_mapper = Mapper()
            if self.mapper is not None:
                instance_mapper.extend(self.mapper)
            instance_mapper.extend(routes)
            self.mapper = instance_mapper

    def _dispatch(self, state, remainder=None):
        if self.mapper is None:
            return super(RoutedController, self)._dispatch(state, remainder)

        environ = state.request.environ

        url = environ['PATH_INFO']
        if len(state.controller_path) > 1:
            # In case we are a subcontroller only dispatch over the remaining URL part.
            url = '/' + '/'.join(remainder)

        results = self.mapper.routematch(url, environ)
        if results:
            route_match, route = results[0], results[1]
        else:
            route_match, route = {}, None

        url = URLGenerator(self.mapper, environ)
        environ['routes.url'] = url
        environ['pylons.routes_dict'] = route_match
        environ['tg.routes_dict'] = route_match
        environ['wsgiorg.routing_args'] = (url, route_match)
        environ['routes.route'] = route

        if route and route.redirect:
            # So far we only emit redirect, it should actually emit according to
            # route.redirect_status.
            route_name = '_redirect_%s' % id(route)
            raise HTTPFound(location=url(route_name, **route_match))

        if not route_match:
            return super(RoutedController, self)._dispatch(state, remainder)

        route_match = route_match.copy()
        tg_context = environ['tg.locals']
        config = tg_context.config

        controller_name = route_match.pop('controller', None)
        if not controller_name:
            abort(404)

        if controller_name == '_tgext_routes_controller_placeholder':
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

