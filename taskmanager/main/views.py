from django.views import generic as views
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

import main.forms as taskman_forms
import main.models as taskman_models

from main.decorators import LoginRequired

@LoginRequired
class CreateProjectView (views.CreateView):
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs
    
    form_class = taskman_forms.ProjectForm
    template_name = 'uni_form/model_form_page.html'

@LoginRequired
class UpdateProjectView (views.UpdateView):
    form_class = taskman_forms.ProjectForm
    template_name = 'uni_form/model_form_page.html'

@LoginRequired
class ProjectDetailView (views.DetailView):
    model = taskman_models.Project
    template_name = 'taskman/project_detail_page.html'

@LoginRequired
class ProjectListView (views.ListView):
    model = taskman_models.Project
    template_name = 'model_filters/model_list_page.html'

class ProjectSubmodelMixin (object):
    project_model = taskman_models.Project
    
    def get_project(self):
        queryset = self.project_model.objects
        
        # Try looking up by primary key.
        pk = self.kwargs.get('project_pk', None)
        slug = self.kwargs.get('project_slug', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        
        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Project sub-view %s must be called with "
                                 u"either a project pk or slug."
                                 % self.__class__.__name__)

        try:
            project = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No project found matching the query"))
        return project
    
@LoginRequired
class CreateTaskView (views.CreateView, ProjectSubmodelMixin):
    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        project = self.get_project()
        return form_class(project, **self.get_form_kwargs())
    
    def get_success_url(self):
        """
        Returns the url that the user will be redirected to if the form is valid
        and saves successfully.
        """
        project = self.get_project()
        return project.get_absolute_url()
    
    form_class = taskman_forms.TaskForm
    template_name = 'uni_form/model_form_page.html'


