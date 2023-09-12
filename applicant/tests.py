from django.test import TestCase,Client
from django.core.files.uploadedfile import SimpleUploadedFile

from applicant.models import Profile,Sibling,Application
from applicant.forms import LoginForm,RegistrationForm
from education.models import KCBMSUser,Ward,FinancialYear
# Create your tests here.

class ProfileTest(TestCase):
    def create_profile(self):
        return Profile.objects.create(
            user = KCBMSUser.objects.create(
                username = 'test',
                password = 'chriswayne'
            ),
            first_name = 'Test',
            last_name = 'Case',
            admission_number = '5905',
            parents_name = 'Unit Test',
            parents_phone = '+254723958286',
            parents_id = SimpleUploadedFile(
                'parents_id.pdf',
                b'This is the parent\'s id'
            ),
            school_name = 'Tenwek High',
            bank_name = 'KCB',
            bank_account = '100000000',
            bank_branch = 'Bomet',
            course = 'KCSE',
            year_of_study = 4,
            year_of_completion = 2016,
            disability_status = False,
            family_status = 'Single Parents',
            applied_bursary_before = False,
            annual_school_fees = 60000,
            ward = Ward.objects.create(name='Ainamoi'),
            family_income = 20000,
        )

    def test_profile_creation(self):
        profile = self.create_profile()
        self.assertTrue(isinstance(profile,Profile))
        self.assertEqual(profile.__str__(),f'{profile.first_name} {profile.last_name}')

    def test_valid_login_form(self):
        data = {'username':'test','password':'chriswayne'}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {'username':'test','password':''}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_registration_form(self):
        data = {
            'username':'test',
            'email':'kiprotichchristian@gmail.com',
            'password1':'chriswayne',
            'password2':'chriswayne',
            }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        data = {
            'username':'',
            'email':'kiprotichchristian@gmail.com',
            'password1':'',
            'password2':'chriswayne'
            }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_view(self):
        KCBMSUser.objects.create_user(
            username='babu',
            password='chriswayne'
        )
        client = Client()
        response = client.login(username='babu',password='chriswayne')
        self.assertTrue(response)



class SiblingTest(TestCase):
    def create_sibling(self):
        return Sibling.objects.create(
            profile = ProfileTest().create_profile(),
            name = 'Test Case 2',
            school = 'Tenwek High School',
            year_of_study = 3,
            annual_fees = 50000,
            fees_paid = 10000,
            arreas = 30000,
        )

    def test_sibling_creation(self):
        sibling = self.create_sibling()
        self.assertTrue(isinstance(sibling,Sibling))
        self.assertEqual(sibling.__str__(),sibling.name)

class ApplicationTest(TestCase):
    def create_application(self):
        return Application.objects.create(
            profile = ProfileTest().create_profile(),
            fee_balance = 20000,
            fee_statement = SimpleUploadedFile(
                'fee statement.pdf',
                b'This is the fee statement'
            ),
            is_awarded = False,
            is_active = True,
            reasons = '',
            amount = 0,
            previous_term_report = SimpleUploadedFile(
                'Report Card.pdf',
                b'This is the report card'
            ),
            financial_year = FinancialYear.objects.create(
                name = '2021/2022',
                is_active = True,
                is_editable = True,
            )
        )

    def test_application_creation(self):
        application = self.create_application()
        self.assertTrue(isinstance(application,Application))
        self.assertEqual(application.__str__(),f"{application.profile.user.first_name} {application.financial_year.name}")