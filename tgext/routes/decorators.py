from routes.route import Route
from tg.decorators import Decoration


class route(object):
    CURRENT_CONTROLLER = '_tgext_routes_controller_placeholder'

    def __init__(self, path, **kargs):
        if not path.startswith('/'):
            path = '/' + path
        self.routing_path = path
        self.routing_args = kargs

    def __call__(self, func):
        deco = Decoration.get_decoration(func)
        if not hasattr(deco, '_tgext_routes'):
            deco._tgext_routes = []
        deco._tgext_routes.append(Route(func.__name__,
                                        self.routing_path,
                                        controller=route.CURRENT_CONTROLLER,
                                        action=func.__name__,
                                        **self.routing_args))
        return func