# -*- coding: utf-8 -*-
from tg import TGController, expose


class SubController(TGController):
    @expose()
    def hello(self, name='World'):
        return 'Hello %s' % name

    @expose()
    def index(self):
        return 'SUBINDEX'


class HomeController(TGController):
    sub = SubController()
    
    @expose('json')
    def jsonexposed(self, *args, **kwargs):
        return dict(kwargs=kwargs, args=args)

    def unexposed(self):
        return 'HI'

    def private(self):
        return 'NONO!'

    @expose()
    def index(self, *args, **kwargs):
        return 'INDEX'

    def delete(self, *args, **kwargs):
        return 'DELETE'
