# -*- coding: utf-8 -*-
from routes import Mapper
from tg import expose, request
from webtest import TestApp
from tgext.routes import RoutedController
from .utils import make_appcfg_for_controller


class RootController(RoutedController):
    mapper = Mapper()
    mapper.connect('/', controller='home', action='index')
    mapper.connect('/json', controller='home', action='jsonexposed')
    mapper.connect('/unex', controller='home', action='unexposed')
    mapper.connect('/nocontroller', action='index')
    mapper.connect('/delete', controller='home', action='delete', conditions=dict(method=["DELETE"]))
    mapper.redirect('/home', '/')
    mapper.connect('/forsub{_dispatch:.*?}', controller='home',  action='_dispatch')
    mapper.connect('/altsub', controller='home', action='_dispatch')

    @expose()
    def odispatch(self):
        return 'ObjectDispatch'

    def private(self):
        return 'PRIVATE'

    @expose()
    def get_host(self):
        return request.routes_local.host


class BaseRoutesTest(object):
    root_controller = RootController

    @classmethod
    def setup_class(cls):
        config = make_appcfg_for_controller(cls.root_controller())
        cls.wsgi_app = config.make_wsgi_app()

    def setup(self):
        self.app = TestApp(self.wsgi_app)


class TestRootRouting(BaseRoutesTest):
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

    def test_delete_without_method(self):
        self.app.get('/delete', status=404)

    def test_delete_with_method_override_disabled(self):
        self.app.get('/delete?_method=DELETE', status=404)

    def test_without_http_host(self):
        resp = self.app.get("/get_host", extra_environ={"HTTP_HOST": ""})
        assert "localhost:80" == resp.text


class TestRootRoutingMethodOverride(BaseRoutesTest):
    class root_controller(RootController):
        method_override = True

    def test_delete_with_method_override_enabled(self):
        resp = self.app.get('/delete?_method=DELETE')
        assert 'DELETE' in resp.text, resp


class TestRootRoutingDispatchContinuation(BaseRoutesTest):
    def test_subdispatch(self):
        self.app.get('/forsub/missing', status=404)

    def test_subdispatch_index(self):
        resp = self.app.get('/forsub/')
        assert 'INDEX' in resp.text

    def test_subdispatch_subcontroller(self):
        resp = self.app.get('/forsub/sub')
        assert 'SUBINDEX' in resp.text

    def test_subdispatch_subcontroller_action(self):
        resp = self.app.get('/forsub/sub/hello')
        assert 'Hello World' in resp.text

    def test_subdispatch_subcontroller_action_args(self):
        resp = self.app.get('/forsub/sub/hello/User')
        assert 'Hello User' in resp.text

    def test_altsub(self):
        resp = self.app.get('/altsub')
        assert 'INDEX' in resp

    def test_altsub_more(self):
        self.app.get('/altsub/anything', status=404)