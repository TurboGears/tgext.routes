import inspect
from routes import Mapper
from tg import TGController
from tg.decorators import Decoration

class RoutedController(TGController):
    def __init__(self, *args, **kw):
        super(RoutedController, self).__init__(*args, **kw)
        routes = []

        for name, value in inspect.getmembers(self):
            if inspect.ismethod(value):
                deco = Decoration.get_decoration(value.__func__)
                if hasattr(deco, '_tgext_routes'):
                    routes.extend(deco._tgext_routes)

        self.map = Mapper()
        self.map.extend(routes)

    def _dispatch(self, state, remainder=None):
        if remainder is None:
            remainder = state.path

        if remainder:
            url_to_dispatch = '/'.join(remainder)
            match = self.map.match(url_to_dispatch)
            if match is not None:
                remainder = [match.pop('action', 'index')]
                state.params.update(match)

        return super(RoutedController, self)._dispatch(state, remainder)
