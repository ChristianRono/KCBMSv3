import pandas as pd
# import openpyxl as xl

from education.models import FinancialYear
from applicant.models import Application
from collections import defaultdict
from django.apps import apps


def file_creator(applications,school,year):
    data = {}
    a = 0
    data['NAME'] = []
    data['ADMISSION/REGISTRATION'] = []
    data['GENDER'] = []
    data['AMOUNT'] = []
    for application in applications:
        data['NAME'].append(f"{application.profile.first_name} {application.profile.last_name}")
        data['ADMISSION/REGISTRATION'].append(application.profile.admission_number)
        data['GENDER'].append('Male' if application.profile.gender == 'male' else 'Female')
        data['AMOUNT'].append(application.amount)

        a += 1
    df = pd.DataFrame(data)
    year = year.replace('/',':')
    df.to_excel(f'media/{year}-{school}-Students List.xlsx')

def file_creator2(applications,filter,year):
    data = {}
    a = 0
    data['NAME'] = []
    data['ADMISSION/REGISTRATION'] = []
    data['WARD'] = []
    data['GENDER'] = []
    data['INSTITUTION'] = []
    data['BANK'] = []
    data['ACCOUNT'] = []
    data['BRANCH'] = []
    data['AMOUNT'] = []
    for application in applications:
        data['NAME'].append(f"{application.profile.first_name} {application.profile.last_name}")
        data['ADMISSION/REGISTRATION'].append(application.profile.admission_number)
        data['GENDER'].append('Male' if application.profile.gender == 'male' else 'Female')
        data['AMOUNT'].append(application.amount)
        data['WARD'].append(application.profile.ward.name)
        data['INSTITUTION'].append(application.profile.school_name)
        data['BANK'].append(application.profile.bank_name)
        data['ACCOUNT'].append(application.profile.bank_account)
        data['BRANCH'].append(application.profile.bank_branch)

        a += 1
    df = pd.DataFrame(data)
    year = year.replace('/',':')
    df.to_excel(f'media/{year}-{filter}-Students List.xlsx')
    return f'media/{year}-{filter}-Students List.xlsx'


""" def file_creator(applications):
    wb = xl.Workbook()
    ws = wb.active
    c1 = ws.cell(row=1,column=1)
    c1.value = 'Full Name'
    c2 = ws.cell(row=1,column=2)
    c2.value = 'Admission/Registration Number'
    c3 = ws.cell(row=1,column=3)
    c3.value = 'Gender'
    c4 = ws.cell(row=1,column=4)
    c4.value = 'Amount'

    i = 2
    for data in applications:
        c1 = ws.cell(row=i,column=1)
        c1.value = data.full_name
        c2 = ws.cell(row=i,column=2)
        c2.value = data.admission_no
        c3 = ws.cell(row=i,column=3)
        c3.value = data.get_gender_display()
        c4 = ws.cell(row=i,column=4)
        c4.value = data.amount
        i += 1
    
    wb.save('Students List.xlsx') """