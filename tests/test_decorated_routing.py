# -*- coding: utf-8 -*-
from tg import expose
from webtest import TestApp
from tgext.routes import RoutedController, route
from .utils import make_appcfg_for_controller


class SubController(RoutedController):
    @expose('json')
    @route('{name}-{surname}')
    def name(self, name, surname):
        return dict(name=name, surname=surname)


class RootController(RoutedController):
    person = SubController()

    @route('{year}-{month}', day=33)
    @route('{year}-{month}-{day}')
    def today(self, year, month, day):
        return '%s,%s,%s' % (year, month, day)

    @expose()
    def index(self):
        return 'INDEX'


class TestRouteDecorator(object):
    @classmethod
    def setup_class(cls):
        config = make_appcfg_for_controller(RootController())
        cls.wsgi_app = config.make_wsgi_app()

    def setup(self):
        self.app = TestApp(self.wsgi_app)

    def test_index(self):
        resp = self.app.get('/')
        assert 'INDEX' == resp.text, resp

    def test_deco_on_root_controller(self):
        resp = self.app.get('/2015-01-01')
        assert '2015,01,01' == resp.text, resp

    def test_deco_on_subcontroller(self):
        resp = self.app.get('/person/John-Doe')
        assert 'application/json' in resp.content_type, resp
        assert resp.json['name'] == 'John', resp
        assert resp.json['surname'] == 'Doe', resp