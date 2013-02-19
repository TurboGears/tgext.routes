from routes.route import Route
from tg.decorators import Decoration

class route(object):
    def __init__(self, path, **kargs):
        self.routing_path = path
        self.routing_args = kargs

    def __call__(self, func):
        deco = Decoration.get_decoration(func)
        if not hasattr(deco, '_tgext_routes'):
            deco._tgext_routes = []
        deco._tgext_routes.append(Route(func.__name__, self.routing_path, action=func.__name__, **self.routing_args))
        return func