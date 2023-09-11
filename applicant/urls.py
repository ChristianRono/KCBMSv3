from django.urls import path
from django.contrib.auth.decorators import login_required

from applicant import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='applicant login'),
    path('logout/',views.logout,name='applicant logout'),
    path('profile/',login_required(views.ProfileView.as_view()),name='applicant profile'),
    path('',login_required(views.HomePageView.as_view()),name='applicant homepage'),
]