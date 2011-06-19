from django.db import models
from userena.models import UserenaBaseProfile

class AccountProfile (UserenaBaseProfile):
    pass

class Project (models.Model):
    name = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return name
