from django.test import TestCase
import mock

import main.decorators as taskman_decorators
import main.models as taskman_models
import main.views as taskman_views
import main.forms as taskman_forms

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


class ProjectModelTests (TestCase):
    def test_ProjectUrlIsCorrect(self):
        project = taskman_models.Project(name='My Project')
        project.save()
        
        pk = project.pk
        self.assertEqual(project.get_absolute_url(), '/projects/%s/' % pk)
    
    def test_ProjectUnicodeRepresentationIsCorrect(self):
        project = taskman_models.Project(name='My Project')
        project.save()
        
        pk = project.pk
        self.assertEqual(unicode(project), 'My Project')

class ProjectCreateViewTests (TestCase):
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
            method = 'POST'
            POST = {'name': 'My Unique Project'}
            FILES = []
            def build_absolute_uri(self):
                return 'absolute_uri'
            def get_full_path(self):
                return 'full_path'
        
        return DummyRequest, DummyView
    
    def test_FormKwargsAreCorrect(self):
        DummyRequest, DummyView = self.make_dummy_classes(True)
        
        view = taskman_views.CreateProjectView()
        view.request = DummyRequest()
        view.object = None
        
        kwargs = view.get_form_kwargs()
        self.assertEqual(sorted(kwargs.keys()), 
                         ['data', 'files', 'initial', 'instance', 'owner'])
        
    def test_ViewCallsSaveOnForm(self):
        DummyRequest, DummyView = self.make_dummy_classes(True)
        
        view = taskman_views.CreateProjectView()
        view.request = DummyRequest()
        
        save_mock = {'mock':None, 'form':None}
        
        import new
        def get_form_patch(self, *args, **kwargs):
            form = super(taskman_views.CreateProjectView, self).get_form(*args, **kwargs)
            form.save = mock.Mock()
            save_mock['form'] = form
            save_mock['mock'] = form.save
            return form
        view.get_form = new.instancemethod(get_form_patch, view, taskman_views.CreateProjectView)
        
        response = view.dispatch(view.request)
        self.assert_(save_mock['form'].is_bound)
        self.assert_(not save_mock['form'].errors, str(save_mock['form'].errors))
        self.assert_(save_mock['mock'].called)

class ProjectFormTests (TestCase):
    def make_dummy_classes(self, _is_authenticated):
        from django.views.generic import View
        
        class DummyUser (object):
            def is_authenticated(self):
                return _is_authenticated

        class DummyManager (object):
            def create(self, *args, **kwargs):
                pass
        
        class DummyMemberRole (object):
            objects = DummyManager()
            def save(self):
                pass
        
        DummyMemberRole.objects.create = mock.Mock(return_value=DummyMemberRole())
        
        return DummyUser, DummyMemberRole
    
    def test_OwnerIsSetToCurrentUser(self):
        DummyUser, DummyMemberRole = self.make_dummy_classes(True)
        
        user = DummyUser()
        form = taskman_forms.ProjectForm(owner=user,
            files=[], instance=None, initial={}, data={'name': 'My Special Project'})
        form.role_model = DummyMemberRole
        project = form.save()
        
        self.assert_(form.role_model.objects.create.called)
        self.assertEqual(form.role_model.objects.create.call_args[1]['role'],
                         'owner')
        self.assertEqual(form.role_model.objects.create.call_args[1]['member'],
                         user)

