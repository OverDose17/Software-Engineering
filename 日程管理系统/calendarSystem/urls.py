from django.urls import path, re_path, include, reverse_lazy

from django.contrib.auth import views as auth_views
from . import views

app_name = 'calendarSystem'
urlpatterns = [
    
    path('', views.calendar_view, name='calendar'),
    # path("", views.dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('statistic/<str:mydate>/', views.statistic, name='statistic'),
    
    path('event/new/<str:mydate>/', views.event, name='event_new'),

	re_path('event/edit/(?P<event_id>\d+)/', views.editevent, name='event_edit'),
    re_path("event/update/(?P<event_id>\d+)", views.updateevent, name = 'event_update'),
    
    re_path('event/delete/(?P<event_id>\d+)/', views.delete, name='event_delete'),
    path("user_info/", views.user_info),

]