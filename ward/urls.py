from django.urls import path
from django.contrib.auth.decorators import login_required

from ward import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='ward login'),
    path('logout/',views.logout,name='ward logout'),
    path('applicants/',views.ApplicantListView.as_view(),name='ward applicant list'),
    path('applicants/<int:pk>/',views.ApplicantDetailView.as_view(),name='ward applicant detail'),
    path('applicants/review/<int:pk>/',views.ApplicantReview.as_view(),name="ward applicant review"),
    path('',views.HomePageView.as_view(),name='ward homepage'),
]