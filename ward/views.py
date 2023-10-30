from typing import Any
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
from ward.forms import LoginForm,WardAdminForm

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
    template_name = "base_ward_homepage.html"

    def get(self,request,*args,**kwargs):
        total_all_applications = Application.objects.all().count()
        total_current_applications = Application.objects.filter(financial_year__is_active=True).count()
        all_wards = Application.objects.values_list('profile__ward__name',flat=True).distinct()
        current_wards = Application.objects.filter(financial_year__is_active=True).values_list('profile__ward__name',flat=True).distinct()

        if total_all_applications > 0:
            # Do the statistics for all applications
            all_males = Application.objects.filter(profile__gender='male').count()
            all_females = Application.objects.filter(profile__gender='female').count()
            try:
                all_males_percentage = all_males / ( all_males + all_females ) * 100
                all_females_percentage = all_females / ( all_males + all_females ) * 100
                all_males_percentage = round(all_males_percentage,2)
                all_females_percentage = round(all_females_percentage,2)
            except ZeroDivisionError:
                all_males_percentage = None
                all_females_percentage = None
        else:
            all_males = 0
            all_females = 0
            all_males_percentage = 0
            all_females_percentage = 0

        if total_current_applications > 0:
            # Do the statistics for current financial year applications
            current_males = Application.objects.filter(profile__gender='male',financial_year__is_active=True).count()
            current_females = Application.objects.filter(profile__gender='female',financial_year__is_active=True).count()
            try:
                current_males_percentage = current_males / ( current_males + current_females ) * 100
                current_females_percentage = current_females / ( current_males + current_females ) * 100
                current_males_percentage = round(current_males_percentage,2)
                current_females_percentage = round(current_females_percentage,2)
            except ZeroDivisionError:
                current_females_percentage = None
                current_males_percentage = None
        else:
            current_males = 0
            current_females = 0
            current_males_percentage = 0
            current_females_percentage = 0

        ward_all_data = {}
        if total_all_applications > 0:
            for ward in all_wards:
                ward_count = Application.objects.filter(profile__ward__name=ward).count()
                ward_percentage = ward_count / total_all_applications * 100
                ward_female_count = Application.objects.filter(profile__ward__name=ward,profile__gender='female').count()
                female_percentage = ward_female_count / ward_count * 100
                ward_male_count = Application.objects.filter(profile__ward__name=ward,profile__gender='male').count()
                male_percentage = ward_male_count / ward_count * 100
                ward_pwd_count = Application.objects.filter(profile__ward__name=ward,profile__disability_status=True).count()
                pwd_percentage = ward_pwd_count / ward_count * 100
                ward_all_data[ward] = {
                    "ward_count":ward_count,
                    'ward_percentage':round(ward_percentage,2),
                    'female_percentage':round(female_percentage,2),
                    'male_percentage':round(male_percentage,2),
                    'pwd_percentage':round(pwd_percentage,2)}
        
        ward_current_data = {}
        if total_current_applications > 0:
            for ward in current_wards:
                ward_count = Application.objects.filter(profile__ward__name=ward,financial_year__is_active=True).count()
                ward_percentage = ward_count / total_all_applications * 100
                ward_female_count = Application.objects.filter(profile__ward__name=ward,profile__gender='female',financial_year__is_active=True).count()
                female_percentage = ward_female_count / ward_count * 100
                ward_male_count = Application.objects.filter(profile__ward__name=ward,profile__gender='male',financial_year__is_active=True).count()
                male_percentage = ward_male_count / ward_count * 100
                ward_pwd_count = Application.objects.filter(profile__ward__name=ward,profile__disability_status=True,financial_year__is_active=True).count()
                pwd_percentage = ward_pwd_count / ward_count * 100
                ward_current_data[ward] = {
                    "ward_count":ward_count,
                    'ward_percentage':round(ward_percentage,2),
                    'female_percentage':round(female_percentage,2),
                    'male_percentage':round(male_percentage,2),
                    'pwd_percentage':round(pwd_percentage,2)}
        
        return render(request,self.template_name,{"total_all_applications":total_all_applications,
                                                    "total_current_applications":total_current_applications,
                                                    "ward_current_data":ward_current_data,
                                                    "ward_all_data":ward_all_data,
                                                    "all_males":all_males,
                                                    "all_females":all_females,
                                                    "all_males_percentage":all_males_percentage,
                                                    "all_females_percentage":all_females_percentage,
                                                    "current_males":current_males,
                                                    "current_females":current_females,
                                                    "current_males_percentage":current_males_percentage,
                                                    "current_females_percentage":current_females_percentage})
    

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
    form = WardAdminForm
    context_object_name = "application"
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

class ApplicantReview(LoginRequiredMixin,View):
    login_url = "/ward/login/"
    form = WardAdminForm
    model = Application
    
    def get(self,request,*args,**kwargs):
        return redirect('ward homepage')
    
    def post(self,request,*args,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            id = kwargs['pk']
            is_awarded = form.cleaned_data['is_awarded']
            reasons = form.cleaned_data['reasons']
            amount = form.cleaned_data['amount']
            application = Application.objects.get(id=id)
            application.is_awarded = is_awarded
            application.is_active = False
            application.reasons = reasons
            application.amount = amount
            application.save()
            return redirect('ward applicant list')
        else:
            return redirect('ward applicant list')


def logout(request):
    return logout_then_login(request,login_url='/ward/login/')