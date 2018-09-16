from django.urls import path
from . import views
from django.db.models import F
urlpatterns = [
    path('', views.TestView.as_view()),
    path('auth', views.AuthTestView.as_view()),
    path('cookies', views.CookieChecker.as_view()),
    path('logout', views.LogOut.as_view()),

    #Views visible for pets.
 #   path('entity', views.EntityPETView.as_view()),
#    path('tasks', views.TaskPETView.as_view()),

    #Other views.
    #path('adm/entities', views.EntityLCView.as_view()),                     #GET, POST
   # path('adm/entities/<int:pk>', views.EntityRUDView.as_view()), #GET, PUT, PATCH, DELETE

    
  #  path('adm/entities/<int:pk>/authorizations', views.AuthorizationEScopeLCView.as_view()),         #GET, POST
    
 #   path('adm/authorizations', views.AuthorizationLView.as_view()),             #GET
#    path('adm/authorizations/<int:pk>', views.AuthorizationRUDView.as_view()), #GET, PATCH, PUT, DELETE 


    #path('adm/entities/<int:pk>/tasks', views.TasksEScopeLCView.as_view()),                          #GET, POST 
    
    #path('adm/tasks', views.TaskLView.as_view()),            #GET, 
   # path('adm/tasks/<int:pk>', views.TaskRUDView.as_view()),        #GET,PATCH,PUT,DELETE
  #  path('adm/tasks/<int:pk>/complete', views.TaskCompleteView.as_view()),        #POST
  #  path('adm/tasks/<int:pk>/jobs', views.JobTScopeLCView.as_view()),        #GET, POST

   # path('adm/jobs', views.JobLView.as_view()),
   # path('adm/jobs/<int:pk>', views.JobRUDView.as_view()),
   # path('adm/jobs/<int:pk>/start', views.JobStartView.as_view()),        #POST
   # path('adm/jobs/<int:pk>/finish', views.JobFinishView.as_view()),        #POST

    #path('adm/test', views.TaskSerialization.as_view()),
    path('tasks', views.TaskListCreate.as_view()),
    
    path('task/<int:pk>/files', views.ListTaskFiles.as_view(), kwargs={'type':None}),
    path('task/<int:pk>/input_files', views.ListTaskFiles.as_view(), kwargs={'type':'input'}),
    path('task/<int:pk>/output_files', views.ListTaskFiles.as_view(), kwargs={'type':'output'}),

    path('task/<int:pk>/status', views.TaskStatusView.as_view()),
    path('task/<int:pk>/log', views.TaskLogView.as_view()),
    path('task/<int:pk>/kill', views.TaskKillView.as_view()),

    path('entity', views.EntityView.as_view()),

    path('authorizations', views.AuthorizationView.as_view()),
    path('authorizations/active', views.AuthorizationActiveView.as_view()),
    path('test', views.TestView.as_view()),
    #refactoring

]