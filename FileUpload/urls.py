from django.urls import path
from FileUpload import views

urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("userhome/", views.userhome, name="userhome"),
]
