from django.views import generic as views

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
    template_name = 'model_form.html'

@LoginRequired
class UpdateProjectView (views.UpdateView):
    form_class = taskman_forms.ProjectForm
    template_name = 'model_form.html'

@LoginRequired
class ProjectDetailView (views.DetailView):
    model = taskman_models.Project
    template_name = 'model_detail.html'

@LoginRequired
class ProjectListView (views.ListView):
    model = taskman_models.Project
    template_name = 'model_list.html'

