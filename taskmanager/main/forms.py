from django import forms

import main.models as taskman_models

class ProjectForm (forms.ModelForm):
    role_model = taskman_models.ProjectMemberRole
    
    def __init__(self, owner=None, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # When creating a project, a user must be provided.  This 
        self.owner = owner
    
    def save(self):
        project = super(ProjectForm, self).save()
        
        if project.members.count() == 0:
            member_role = self.role_model.objects.create(
                member=self.owner, project=project, role='owner')
            member_role.save()
        return project
    
    class Meta:
        model = taskman_models.Project
        exclude = ('members',)

class TaskForm (forms.ModelForm):
    class Meta:
        model = taskman_models.Task

