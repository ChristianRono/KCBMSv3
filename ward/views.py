from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from applicant.models import Application,Profile
from education.models import KCBMSUser,FinancialYear,Ward
from ward.forms import LoginForm

# Create your views here.

class LoginView(View):
    form_class = LoginForm
    template_name = "base_ward_login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and user.is_ward_admin and not user.is_edu_admin and not user.is_accountant:
                login(request,user)
                messages.success(request,"Log In Successful")
                return redirect('ward homepage')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('ward login')

class HomePageView(LoginRequiredMixin,View):
    login_url = "/ward/login/"
    pass

class ApplicantListView(LoginRequiredMixin,ListView):
    login_url = "/ward/login/"
    template_name = "base_ward_applications_list.html"
    context_object_name = "applications"

    def get_queryset(self):
        self.ward = get_object_or_404(Ward,name='Ainamoi')

        return Application.objects.filter(profile__ward=self.ward,is_active=True)

class ApplicantDetailView(LoginRequiredMixin,DetailView):
    login_url = "/ward/login/"
    template_name = "base_ward_applications_detail.html"
    context_object_name = "application"
    model = Application


def logout(request):
    return logout_then_login(request,login_url='/ward/login/')