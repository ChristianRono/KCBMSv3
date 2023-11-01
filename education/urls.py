from django.urls import path
from django.contrib.auth.decorators import login_required

from education import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='education login'),
    path('applications/',views.applications,name="education applications"),
    path('applications/filter/',views.list_filter,name="education applications filter"),
    path('applications/filter/print/<str:filter>/',views.print_file,name="education filter print"),
    path('allocations/',views.allocations,name='education allocations'),
    path('allocations/new/',views.allocations_new,name='education allocations form'),
    path('users/',views.users,name='education users'),
    path('users/edit/<int:id>/',views.edit_users,name="education users edit"),
    path('users/activate/<int:id>/',views.activate_user,name='education users activate'),
    path('users/deactivate/<int:id>/',views.deactivate_user,name='education users deactivate'),
    path('users/add/',views.add_users,name='education users add'),
    path('financial/',views.financial,name='education financial'),
    path('financial/new/',views.financial_new,name="education financial form"),
    path('financial/deactivate/<int:id>/',views.financial_deactivate,name='education financial deactivate'),
    path('financial/activate/<int:id>/',views.financial_activate,name='education financial activate'),
    path('check/',views.check_applications,name='check applications'),
    path('logout/',views.logout_then_login,name="education logout" ),
    path('',views.HomePageView.as_view(),name='education homepage'),
]