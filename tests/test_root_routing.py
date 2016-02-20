# -*- coding: utf-8 -*-
from routes import Mapper
from tg import expose
from webtest import TestApp
from tgext.routes import RoutedController
from .utils import make_appcfg_for_controller


class RootController(RoutedController):
    mapper = Mapper()
    mapper.connect('/', controller='home', action='index')
    mapper.connect('/json', controller='home', action='jsonexposed')
    mapper.connect('/unex', controller='home', action='unexposed')
    mapper.connect('/nocontroller', action='index')
    mapper.redirect('/home', '/')

    @expose()
    def odispatch(self):
        return 'ObjectDispatch'

    def private(self):
        return 'PRIVATE'


class TestRootRouting(object):
    @classmethod
    def setup_class(cls):
        config = make_appcfg_for_controller(RootController())
        cls.wsgi_app = config.make_wsgi_app()

    def setup(self):
        self.app = TestApp(self.wsgi_app)

    def test_index(self):
        resp = self.app.get('/')
        assert 'INDEX' == resp.text, resp

    def test_objectdispatch(self):
        resp = self.app.get('/odispatch')
        assert 'ObjectDispatch' == resp.text, resp

    def test_redirect(self):
        resp = self.app.get('/home')
        resp = resp.follow()
        assert 'INDEX' == resp.text, resp

    def test_unexposed(self):
        # As a route explicitly points to the controller, even unexposed controllers should work
        resp = self.app.get('/unex')
        assert 'HI' == resp.text, resp

    def test_private(self):
        # but internal methods should not be exposed
        self.app.get('/private', status=404)

    def test_exposition_works(self):
        resp = self.app.get('/json')
        assert 'application/json' in resp.content_type, resp
        assert {"args": [], "kwargs": {}} == resp.json, resp

    def test_missing_controller(self):
        self.app.get('/nocontroller', status=404)

