from django.urls import path
from django.contrib.auth.decorators import login_required

from applicant import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='applicant login'),
    path('registration/',views.RegistrationView.as_view(),name='applicant register'),
    path('logout/',views.logout,name='applicant logout'),
    path('profile/',views.ProfileView.as_view(),name='applicant profile'),
    path('status/',views.StatusView.as_view(),name='applicant status'),
    path('',views.HomePageView.as_view(),name='applicant homepage'),
]