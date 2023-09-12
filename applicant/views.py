from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from applicant.forms import LoginForm,RegistrationForm,ProfileForm,ApplicationForm
from applicant.models import Application,Profile
from education.models import KCBMSUser,FinancialYear

# Create your views here.
 
class RegistrationView(View):
    form_class = RegistrationForm
    template_name = "base_applicant_registration.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(self.request, self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)

        if form.is_valid():
            print("valid")
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                print('passwords match')
                user = KCBMSUser.objects.create_user(
                    username = username,
                    email = email,
                    password = password1,
                )
                user.save()
                messages.success(self.request,'Registration is successful!')
                login(self.request,user)
                return redirect('applicant profile')
        messages.error(self.request,'Registration was unsuccessful!')
        return redirect('applicant register')

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
    form_class = ApplicationForm
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=self.request.user)
            application = Application.objects.filter(
                profile=profile,
                financial_year=FinancialYear.objects.get(is_active=True)
                )
            if application:
                return redirect('applicant status')
            form = self.form_class()
            return render(request,self.template_name,{'form':form})
        except ObjectDoesNotExist:
            messages.error(self.request,'You have to fill out your profile first!')
            return redirect('applicant profile')

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST,self.request.FILES)
        print(self.request.FILES)

        if form.is_valid():
            print('h')
            profile = Profile.objects.get(user__username = self.request.user)
            fee_balance = form.cleaned_data['fee_balance']
            fee_statement = form.cleaned_data['fee_statement']
            previous_term_report = form.cleaned_data['previous_term_report']
            financial_year = FinancialYear.objects.get(is_active=True)

            application = Application.objects.create(
                profile = profile,
                fee_balance = fee_balance,
                fee_statement = fee_statement,
                previous_term_report = previous_term_report,
                financial_year = financial_year,
            )
            application.save()
            messages.success(self.request,'Your application has been successfully submitted!')
            return redirect('applicant status')
        messages.error(self.request,'Your application has not been successfully submitted!')
        return redirect('applicant homepage')


class ProfileView(LoginRequiredMixin,View):
    login_url = "/login/"
    form_class = ProfileForm
    template_name = 'base_applicant_profile.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            form = self.form_class(instance=profile)
        except:
            form = self.form_class()

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST,self.request.FILES)

        if form.is_valid():
            print(self.request.user)
            profile = Profile.objects.create(
                user = KCBMSUser.objects.get(username=self.request.user),
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                admission_number = form.cleaned_data['admission_number'],
                parents_name = form.cleaned_data['parents_name'],
                parents_phone = form.cleaned_data['parents_phone'],
                parents_id = form.cleaned_data['parents_id'],
                school_name = form.cleaned_data['school_name'],
                bank_name = form.cleaned_data['bank_name'],
                bank_account = form.cleaned_data['bank_account'],
                bank_branch = form.cleaned_data['bank_branch'],
                course = form.cleaned_data['course'],
                year_of_study = form.cleaned_data['year_of_study'],
                year_of_completion = form.cleaned_data['year_of_completion'],
                disability_status = form.cleaned_data['disability_status'],
                family_status = form.cleaned_data['family_status'],
                death_certificate_father = form.cleaned_data['death_certificate_father'],
                death_certificate_mother = form.cleaned_data['death_certificate_mother'],
                family_income = form.cleaned_data['family_income'],
                applied_bursary_before = form.cleaned_data['applied_bursary_before'],
                annual_school_fees = form.cleaned_data['annual_school_fees'],
                ward = form.cleaned_data['ward'],
                )
            profile.save()
            return redirect('applicant homepage')
        else:
            return redirect('applicant homepage')

class StatusView(LoginRequiredMixin,View):
    template_name = 'base_applicant_status.html'

    def get(self, request, *args, **kwargs):
        try:
            application = Application.objects.get(
                profile = Profile.objects.get(user__username = request.user),
                financial_year = FinancialYear.objects.get(is_active=True)
            )
        except ObjectDoesNotExist:
            return redirect('applicant homepage')

        return render(self.request,self.template_name,{'application':application})

def logout(request):
    return logout_then_login(request,login_url='/login/')