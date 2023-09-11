from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.views import View

from applicant.forms import LoginForm,RegistrationForm,ProfileForm
from applicant.models import Application,Profile

# Create your views here.
 
class LoginView(View):
    form_class = LoginForm
    template_name = "base_applicant_login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and not user.is_ward_admin and not user.is_edu_admin and not user.is_accountant:
                login(request,user)
                messages.success(request,"Log In Successful")
                return redirect('applicant homepage')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('applicant login')

class HomePageView(LoginRequiredMixin,View):
    login_url = '/login/'
    template_name = "base_applicant_homepage.html"
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            application = Application.objects.filter(
                profile=profile,
                financial_year=FinancialYear.objects.get(is_active=True)
                )
            if application:
                return redirect('applicant status')
            form = ApplicationForm()
            return render(request,self.template,{'form':form})
        except:
            return redirect('applicant profile')

class ProfileView(LoginRequiredMixin,View):
    login_url = "/login/"
    template_name = 'base_applicant_profile.html'

    def get(self, request, *args, **kwargs):
        form = ProfileForm()

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            admission_number = form.cleaned_data['admission_number']
            parents_name = form.cleaned_data['parents_name']
            parents_phone = form.cleaned_data['parents_phone']
            parents_id = form.cleaned_data['parents_id']
            school_name = form.cleaned_data['school_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']
            first_name = form.cleaned_data['first_name']

def logout(request):
    return logout_then_login(request,login_url='/login/')