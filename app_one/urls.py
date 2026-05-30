from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view()),
    path("signin/", views.SignIn.as_view()),
    path("logout/", views.Logout.as_view()),
    path("update/", views.UpdateUser.as_view()),

]