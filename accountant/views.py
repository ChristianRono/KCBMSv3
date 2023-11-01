from django.shortcuts import render

# Create your views here.
import os
import pandas as pd

from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib import messages

from education.models import FinancialYear
from accountant.forms import EmailForm,LoginForm
from applicant.models import Application,Profile

from ward.utility import file_creator,file_creator2

# Create your views here.
class LoginView(View):
    form_class = LoginForm
    template_name = "accounts_login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and not user.is_ward_admin and not user.is_edu_admin and user.is_accountant:
                login(request,user)
                messages.success(request,"Log In Successful")
                return redirect('accounts homepage')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('accounts login')

@login_required(login_url='/accounts/login/')
def homepage(request):
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
    
    return render(request,"accounts_homepage.html",{"total_all_applications":total_all_applications,
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

@login_required(login_url='/accounts/login/')
def applications(request):
    financialyear = FinancialYear.objects.get(is_active=True)
    schools = Profile.objects.values_list('school_name', flat=True).distinct()
    banks = Profile.objects.values_list('bank_name', flat=True).distinct()
    wards = Profile.objects.values_list('ward__name', flat=True).distinct()
    applications = Application.objects.filter(financial_year=financialyear).order_by('profile__first_name')
    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    count = Application.objects.filter(financial_year=financialyear).count()

    return render(request,"accounts_applications.html",{'applications':applications, 
                                                  'schools':schools, 
                                                  'wards':wards,
                                                  'banks':banks,
                                                  'count':count})

@login_required(login_url='/accounts/login/')
def list_filter(request):
    query = Q(financial_year__is_active=True)
    filter_q = 'Financial Year: Current'
    if 'school-checkbox' in request.POST:
        filter_q += ' & School:' + request.POST['school-dropdown']
        query = query & Q(profile__school_name=request.POST['school-dropdown'])
    if 'gender-checkbox' in request.POST:
        gender = "Male" if request.POST['gender-dropdown'] == 'm' else "Female"
        filter_q += ' & Gender:' + gender
        query = query & Q(profile__gender=request.POST['gender-dropdown'])
    if 'bank-checkbox' in request.POST:
        filter_q += ' & Bank:' + request.POST['bank-dropdown']
        query = query & Q(profile__bank_name=request.POST['bank-dropdown'])
    if 'ward-checkbox' in request.POST:
        filter_q += ' & Ward:' + request.POST['ward-dropdown']
        query = query & Q(profile__ward__name=request.POST['ward-dropdown'])
    
    applications = Application.objects.filter(query)

    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    return render(request,"accounts_filter.html",{
        "applications":applications,
        "filter":filter_q})

@login_required(login_url='/accounts/login/')
def list_schools(request):
    schools = Application.objects.filter(financial_year__is_active=True).values_list('profile__school_name',flat=True).distinct()
    SCHOOLS = {}
    Total = 0
    for school in schools:
        applications = Application.objects.filter(profile__school_name=school,financial_year__is_active=True)
        sub_total = 0
        branch = {}
        account = {}
        for application in applications:
            sub_total += int(application.amount)
            b = branch.get(application.profile.bank_branch,0)
            branch[application.profile.bank_branch] = int(b) + 1
            a = account.get(application.profile.bank_account,0)
            account[application.profile.bank_account] = int(a) + 1
        
        if len(branch) > 3:
            branch = list(sorted(branch)[0:3])
            account = list(sorted(account)[0:3])
        else:
            branch = list(branch)
            account = list(account)
        SCHOOLS[application.profile.school_name] = {
            'bank':application.profile.bank_name,
            'branch':branch,
            'account':account,
            'amount':sub_total
            }
        Total += sub_total
    return render(request,"accounts_schools.html",{'schools':SCHOOLS,'total':Total})

@login_required(login_url='/accounts/login/')
def list_students(request,institution):
    applications = Application.objects.filter(financial_year__is_active=True,profile__school_name=institution)

    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    return render(request,"accounts_students.html",{
        "applications":applications,'institution':institution})
    

@login_required(login_url='/accounts/login/')
def email(request,institution):
    if request.method == 'POST':
        form = EmailForm(request.POST,request.FILES)
        if form.is_valid():
            to = [form.cleaned_data['to']]
            re = form.cleaned_data['re']
            message = form.cleaned_data['message']
            doc = f"{FinancialYear.objects.get(is_active=True).name.replace('/',':')}-{institution}-Students List.xlsx"
            attachment = f'media/{doc}'
            email = EmailMessage(re,message,to=to)

            content = open(attachment, 'rb')
            email.attach(doc,content.read(),'application/pdf')
            email.send()
            os.remove(f'media/{doc}')
            return redirect("accounts homepage")
    else:
        applications = Application.objects.filter(profile__school_name=institution)
        year = FinancialYear.objects.get(is_active=True)
        file_creator(applications,institution,year.name)
        form =EmailForm({'re':'Bursary Students List','message':'This is an automatic message. Please do not reply.'})
        return render(request,"accounts_email.html",{'form':form,'institution':institution})
 
@login_required(login_url='/accounts/login/')   
def print_file(request,filter):
    filters = filter.split('&')
    query = Q(financial_year__is_active=True)
    print(filters)
    for filter in filters[1:]:
        parts = filter.split(':')
        part0 = parts[0].lower().strip()
        if part0 == 'ward':
            query = query & Q(ward__name=parts[1])
        else:
            if part0 == 'school':
                part0 = "profile__school_name"
            if part0 == 'profile__gender':
                if parts[1] == 'male':
                    parts[1] = 'male'
                else:
                    parts[1] = 'female'
            query = query & Q((part0,parts[1]))
        print(query)
    applications = Application.objects.filter(query)
    print(applications)
    applications.select_related('ward','financial_year')
    applications_list = list(applications.values('profile__first_name',
                                                 'profile__last_name',
                                                 'profile__admission_number',
                                                 'profile__gender',
                                                 'amount'))
    year = FinancialYear.objects.get(is_active=True)
    df = pd.DataFrame(applications_list)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{year}-{filter}.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required(login_url='/accounts/login/')
def download(request,institution):
    applications = Application.objects.filter(profile__school_name=institution,financial_year__is_active=True)
    applications_list = list(applications.values('profile__first_name',
                                                 'profile__last_name',
                                                 'profile__admission_number',
                                                 'profile__gender',
                                                 'amount'))
    year = FinancialYear.objects.get(is_active=True)
    df = pd.DataFrame(applications_list)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{year}-{filter}.xlsx"'
    df.to_excel(response, index=False)
    return response
