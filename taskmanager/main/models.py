from django.db import models
from userena.models import UserenaBaseProfile
from django.contrib.auth import models as auth_models

class AccountProfile (UserenaBaseProfile):
    pass

class Project (models.Model):
    name = models.CharField(max_length=1024)
    members = models.ManyToManyField(auth_models.User, 
                                     through='ProjectMemberRole',
                                     related_name='projects')
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('taskman_project_details', [self.pk])
        

class ProjectMemberRole (models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('contr', 'Contributor'),
        ('spect', 'Spectator'),
    ]
    
    project = models.ForeignKey(Project, related_name='member_roles')
    member = models.ForeignKey(auth_models.User, related_name='project_roles')
    role = models.TextField(max_length=5, choices=ROLE_CHOICES, default='owner')
    
    def __unicode__(self):
        return u'%s is a(n) %s on %s' % (self.member, self.role, self.project)

class Task (models.Model):
    project = models.ForeignKey(Project, related_name='tasks')
    label = models.CharField(max_length=256)
    points = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey('TaskStatus', null=True, blank=True)
    note = models.TextField(default='', blank=True)
    
    def __unicode__(self):
        return self.label

class TaskStatus (models.Model):
    label = models.CharField(max_length=128)
    specific_to = models.ForeignKey(Project, null=True,
                                    related_name="taskstatus_choices")
    
    def __unicode__(self):
        return self.label

