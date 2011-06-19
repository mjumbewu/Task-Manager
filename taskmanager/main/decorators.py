from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def LoginRequired(ViewClass):
    """Decorator for classes that derive from generic class-based views."""
    
    ViewClass.dispatch = method_decorator(login_required)(ViewClass.dispatch)
    return ViewClass
