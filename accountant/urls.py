from django.urls import path
from accountant.views import (
    homepage,
    applications,
    list_filter,
    list_schools,
    list_students,
    email,
    download,
    print_file,
    LoginView,
    logout_then_login
)

urlpatterns = [
    path('applications/',view=applications,name='accounts applications'),
    path('filter/',view=list_filter,name='accounts filter'),
    path('schools/',view=list_schools,name='accounts schools'),
    path('students/<str:institution>/',view=list_students,name='accounts students'),
    path('email/<str:institution>/',view=email,name='accounts email'),
    path('print/<str:filter>/',view=print_file,name="accounts print"),
    path('download/<str:institution>/',view=download,name="accounts download"),
    path('login/',view=LoginView.as_view(),name="accounts login"),
    path('logout/',view=logout_then_login,name="accounts logout"),
    path('',view=homepage,name='accounts homepage'),
]