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
from education.forms import LoginForm

# Create your views here.
class LoginView(View):
    form_class = LoginForm
    template_name = "base_education_login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and not user.is_ward_admin and user.is_edu_admin and not user.is_accountant:
                login(request,user)
                messages.success(request,"Log In Successful")
                return redirect('education homepage')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('education login')
            
class HomePageView(LoginRequiredMixin,View):
    login_url = "/education/login/"
    template_name = "base_education_homepage.html"

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
