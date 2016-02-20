# -*- coding: utf-8 -*-
from tg import expose
from webtest import TestApp
from tgext.routes import RoutedController
from .utils import make_appcfg_for_controller


class RootController(RoutedController):
    VARIABLE = 'should be ignored'

    @expose()
    def index(self):
        return 'HELLO'

    def unexposed(self):
        return 'NO!'


class TestNormalDispatch(object):
    @classmethod
    def setup_class(cls):
        config = make_appcfg_for_controller(RootController())
        cls.wsgi_app = config.make_wsgi_app()

    def setup(self):
        self.app = TestApp(self.wsgi_app)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' == resp.text, resp

    def test_404(self):
        self.app.get('/missing', status=404)

    def test_variable(self):
        self.app.get('/VARIABLE', status=404)

    def test_unexposed(self):
        self.app.get('/unexposed', status=404)
