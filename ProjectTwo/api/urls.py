from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('user', views.get_user_data, name='get_user_data'),
    path('tasks/createdby', views.get_all_tasks_created_by, name='get_all_tasks_created_by'),
    path('tasks/assignedto', views.get_all_tasks_assigned_to, name='get_all_tasks_assigned_to'),
    path('tasks/add', views.add_task, name='add_task'),
    path('tasks/edit/<str:task_id>', views.edit_task, name='edit_task'),
    path('tasks/delete/<str:task_id>', views.delete_task, name='delete_task'),
    path('', views.index, name='index'),
    path('tasks', views.index, name='index'),
]