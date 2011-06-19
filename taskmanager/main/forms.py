from django import forms

import main.models as taskman_models

class ProjectForm (forms.ModelForm):
    class Meta:
        model = taskman_models.Project
    
