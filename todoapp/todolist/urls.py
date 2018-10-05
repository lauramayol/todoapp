from django.urls import path

from . import views

app_name = 'todolist'

urlpatterns = [
    # ex: /polls/
    path('', views.OverviewView.as_view(), name='overview'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:todolist_id>/complete/', views.todo_complete, name='complete'),
    path('<int:pk>/notice', views.NoticeView.as_view(), name='notice'),
    path('clear_all/', views.clear_all, name='clear_all'),
]
