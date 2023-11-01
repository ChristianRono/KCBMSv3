import pandas as pd

from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q,Count
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


from applicant.models import Application,Profile
from education.models import KCBMSUser,FinancialYear,Ward,WardAllocation
from education.forms import LoginForm,AllocationForm,FinancialForm,UserForm

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

@login_required(login_url='/education/login/')
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

    return render(request,"base_education_applications.html",{'applications':applications, 
                                                  'schools':schools, 
                                                  'wards':wards,
                                                  'banks':banks,
                                                  'count':count})

@login_required(login_url='/education/login/')
def allocations(request):
    allocations = WardAllocation.objects.all()
    return render(request,"base_education_allocations.html",{"allocations":allocations})

@login_required(login_url='/education/login/')
def allocations_new(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            ward = form.cleaned_data['ward']
            financial_year = form.cleaned_data['financial_year']
            amount = form.cleaned_data['amount']
            allocation = WardAllocation.objects.create(ward=ward,financial_year=financial_year,amount=amount)
            allocation.save()
            return redirect('education allocations')
    else:
        form = AllocationForm()
        return render(request,"base_education_allocations_form.html",{'form':form})

@login_required(login_url='/education/login/')
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
    return render(request,"base_education_applications_filter.html",{
        "applications":applications,
        "filter":filter_q})

@login_required(login_url='/education/login/')
def users(request):
    edu_admin_users = KCBMSUser.objects.filter(is_edu_admin=True)
    accountant_users = KCBMSUser.objects.filter(is_accountant=True)
    ward_admin_users = KCBMSUser.objects.filter(is_ward_admin=True)
    return render(request,"base_education_users.html",{
        "edu_admin_users":edu_admin_users,
        "accountant_users":accountant_users,
        "ward_admin_users":ward_admin_users})

@login_required(login_url='/education/login')
def edit_users(request,id):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_ward_admin = form.cleaned_data['is_ward_admin']
            is_edu_admin = form.cleaned_data['is_edu_admin']
            is_accountant = form.cleaned_data['is_accountant']

            user = KCBMSUser.objects.create(
                username = username,
                password = make_password(password),
                is_ward_admin = is_ward_admin,
                is_edu_admin = is_edu_admin,
                is_accountant = is_accountant
            )
            user.save()
            return redirect('education users')
        else:
            return redirect(f'/education/users/edit/{id}/')
    else:
        instance = KCBMSUser.objects.get(id=id)
        form = UserForm(instance=instance)
        return render(request,'base_education_users_edit.html',{"form":form,'id':id})


@login_required(login_url='/education/login/')
def activate_user(request,id):
    user = KCBMSUser.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('education users')

@login_required(login_url='/education/login/')
def deactivate_user(request,id):
    user = KCBMSUser.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('education users')

@login_required(login_url='/education/login/')
def add_users(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_ward_admin = form.cleaned_data['is_ward_admin']
            is_edu_admin = form.cleaned_data['is_edu_admin']
            is_accountant = form.cleaned_data['is_accountant']

            user = KCBMSUser.objects.create(
                username = username,
                password = make_password(password),
                is_ward_admin = is_ward_admin,
                is_edu_admin = is_edu_admin,
                is_accountant = is_accountant
            )
            user.save()
            return redirect('edcation users')
        else:
            return redirect('education users add')
    else:
        form = UserForm()
        return render(request,'base_education_users_add.html',{"form":form})

@login_required(login_url='/education/login/')
def financial(request):
    financials = FinancialYear.objects.all()
    return render(request,"base_education_financial.html",{"financials":financials})

@login_required(login_url='/education/login/')
def financial_new(request):
    if request.method == 'POST':
        form = FinancialForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            is_active = form.cleaned_data['is_active']
            if is_active:
                financial_year = FinancialYear.objects.get(is_active=True)
                financial_year.is_active = False
                financial_year.save()
                financial_year = FinancialYear.objects.create(name=name,is_active=is_active)
                financial_year.save()
            else:
                financial_year = FinancialYear.objects.create(name=name,is_active=is_active)
                financial_year.save()
            return redirect('education financial')
    else:
        form = FinancialForm()
        return render(request,'base_education_financial_form.html',{'form':form})

@login_required(login_url='/education/login/')
def financial_deactivate(request,id):
    financial_year = FinancialYear.objects.get(id=id)
    financial_year.is_active = False
    financial_year.save()
    return redirect('education financial')

@login_required(login_url='/education/login/')
def financial_activate(request,id):
    try:
        financial_year = FinancialYear.objects.get(is_active=True)
        financial_year.is_active = False
        financial_year.save()
    except:
        pass
    financial_year = FinancialYear.objects.get(id=id)
    financial_year.is_active = True
    financial_year.save()
    return redirect('education financial')

@login_required(login_url='/education/login/')
def check_applications(request):
    dups = (
        Application.objects.values('birth_cert_no')
        .annotate(count=Count('id'))
        .values('birth_cert_no')
        .order_by()
        .filter(financial_year__is_active=True,count__gt=1)
    )
    applications = Application.objects.filter(birth_cert_no__in=dups).order_by('birth_cert_no')
    if applications.exists():
        return render(request,'master_applications_check.html',{'applications':applications})
    else:
        messages.info(request,'No duplicate Birth Certificates found!')
        return redirect('master applications')
    

@login_required(login_url='/education/login/')   
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