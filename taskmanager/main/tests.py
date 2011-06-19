from django.test import TestCase
import mock

import main.decorators as taskman_decorators


class LoginRequiredTest(TestCase):
    """Test the LoginRequired class decorator"""
    
    def make_dummy_classes(self, _is_authenticated):
        from django.views.generic import View
        
        @taskman_decorators.LoginRequired
        class DummyView (View):
            dispatch_mock = mock.Mock()
            def dispatch(self, *args, **kwds):
                return self.dispatch_mock(*args, **kwds)

        class DummyUser (object):
            def is_authenticated(self):
                return _is_authenticated

        class DummyRequest (object):
            user = DummyUser()
            def build_absolute_uri(self):
                return 'absolute_uri'
            def get_full_path(self):
                return 'full_path'
        
        return DummyRequest, DummyView

    def test_UserRedirectedToLoginPageWhenNotLoggedIn(self):
        """
        Tests that the user is redirected to the login page when trying to 
        access a view that is decorated with LoginRequired if they are not
        logged in.
        """
        DummyRequest, DummyView = self.make_dummy_classes(False)
        
        request = DummyRequest()
        response = DummyView.as_view()(request)
        
        self.assertEqual(response.status_code, 302)
        self.assert_(response.has_header('Location'))
        self.assertEqual(response.get('location', None), '/accounts/signin/?next=full_path')
        self.assert_(not DummyView.dispatch_mock.called)

    def test_UserCanAccessPageWhenLoggedIn(self):
        """
        Tests that the user is given the requested page when trying to access
        a view that is decorated with LoginRequired if they are logged in.
        """
        DummyRequest, DummyView = self.make_dummy_classes(True)
        
        request = DummyRequest()
        response = DummyView.as_view()(request)
        
        self.assert_(DummyView.dispatch_mock.called)

