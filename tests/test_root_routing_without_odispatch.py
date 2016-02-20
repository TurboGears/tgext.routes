# -*- coding: utf-8 -*-
from routes import Mapper
from tg import expose
from webtest import TestApp
from tgext.routes import RoutedController
from .utils import make_appcfg_for_controller


class RootController(RoutedController):
    disable_objectdispatch = True

    mapper = Mapper()
    mapper.connect('/', controller='home', action='index')
    mapper.connect('/json', controller='home', action='jsonexposed')
    mapper.connect('/unex', controller='home', action='unexposed')
    mapper.connect('/nocontroller', action='index')
    mapper.redirect('/home', '/')

    @expose()
    def odispatch(self):
        return 'ObjectDispatch'


class TestRootRoutingWithoutObjectDispatch(object):
    @classmethod
    def setup_class(cls):
        config = make_appcfg_for_controller(RootController())
        cls.wsgi_app = config.make_wsgi_app()

    def setup(self):
        self.app = TestApp(self.wsgi_app)

    def test_index(self):
        resp = self.app.get('/')
        assert 'INDEX' == resp.text, resp

    def test_disabled_objectdispatch(self):
        self.app.get('/odispatch', status=404)

    def test_redirect(self):
        resp = self.app.get('/home')
        resp = resp.follow()
        assert 'INDEX' == resp.text, resp

    def test_unexposed(self):
        # As a route explicitly points to the controller, even unexposed controllers should work
        resp = self.app.get('/unex')
        assert 'HI' == resp.text, resp

    def test_exposition_works(self):
        resp = self.app.get('/json')
        assert 'application/json' in resp.content_type, resp
        assert {"args": [], "kwargs": {}} == resp.json, resp
