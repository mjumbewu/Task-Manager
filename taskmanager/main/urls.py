from django.conf.urls.defaults import patterns, include, url

import main.views as taskman_views

urlpatterns = patterns('taskmanager',
    # Examples:
    # url(r'^$', 'taskmanager.views.home', name='home'),
    # url(r'^taskmanager/', include('taskmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 
        taskman_views.ProjectListView.as_view(),
        name='taskman_project_list'),
    url(r'^create$', 
        taskman_views.CreateProjectView.as_view(),
        name='taskman_create_project'),
    url(r'^(?P<pk>\w+)/edit$', 
        taskman_views.UpdateProjectView.as_view(),
        name='taskman_edit_project'),
    url(r'^(?P<pk>\w+)/$', 
        taskman_views.ProjectDetailView.as_view(),
        name='taskman_project_details'),
    
    url(r'(?P<project_pk>\w+)/tasks/create$',
        taskman_views.CreateTaskView.as_view(),
        name='taskman_create_task'),
)
