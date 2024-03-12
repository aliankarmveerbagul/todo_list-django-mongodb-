from django.urls import path
from . import views

app_name = "todo_app"

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/<str:uid>', views.home, name='home'),
    path('add/<str:uid>', views.add_task, name='add'),
    path('del/<str:id>/<str:uid>', views.delete, name='del'),
    path('views_task/<str:id>/<str:uid>', views.views_task, name='views_task'),
    path('edit/<str:id>/<str:uid>', views.edit_task, name='edit'),
    path('view_add_status/<str:uid>', views.add_status, name='add_status'),
    path('view_status/<str:uid>', views.home_status, name='home_status'),
    path('view_status_edit/<str:id>/<str:uid>/<str:stat>', views.task_status_edit, name='task_status_edit'),
    path('view_status_del/<str:id>/<str:stat>/<str:uid>', views.task_status_del, name='task_status_del'),
    path('filter_values/<str:flt>/<str:uid>', views.filter_hours, name='filter'),
    path('filter_values_tasks/<str:flt>/<str:uid>', views.filter_task, name='filter_task'),

]
