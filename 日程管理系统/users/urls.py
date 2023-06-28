from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("", views.dashboard, name='dashboard'),   
    path("about/", views.about, name="about"),
    path("changepass/", views.changepass, name="change"),
    path("subscription/", views.subscription, name="subscription"),
    path("login/", views.LoginPage, name="login"),
    path("signup/", views.SignupPage, name="signup"),
    path("signup_admin/", views.SignupAdmin, name="signupadmin"),
    path('profile/', views.profile, name='profile'),
    path("logout/", views.LogoutPage, name="logout"),
]