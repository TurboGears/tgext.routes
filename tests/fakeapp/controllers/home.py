# -*- coding: utf-8 -*-
from tg import TGController, expose


class HomeController(TGController):
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