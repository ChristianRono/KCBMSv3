from django.urls import path
from django.contrib.auth.decorators import login_required

from education import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='education login'),
    path('',views.HomePageView.as_view(),name='education homepage'),
]