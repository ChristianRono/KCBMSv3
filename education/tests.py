from django.test import TestCase
from django.urls import reverse

from education.models import KCBMSUser,Ward,WardAllocation,FinancialYear

# Create your tests here.

class UserTest(TestCase):
    def create_user(self,is_ward_admin=False,is_edu_admin=False,is_accountant=False):
        return KCBMSUser.objects.create_user(
            username = 'test',
            password = 'chriswayne',
        )

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user,KCBMSUser))
        self.assertEqual(user.__str__(),user.username)

    def test_applicant_login(self):
        user = self.create_user()
        url = reverse('applicant login')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

class WardTest(TestCase):
    def create_ward(self):
        return Ward.objects.create(
            name = 'Ainamoi'
        )

    def test_ward_creation(self):
        ward = self.create_ward()
        self.assertTrue(isinstance(ward,Ward))
        self.assertEqual(ward.__str__(),ward.name)

class FinancialYearTest(TestCase):
    def create_financial_year(self):
        return FinancialYear.objects.create(
            name = '2020/2021',
            is_active = True,
            is_editable = True,
        )

    def test_financial_year_creation(self):
        financial_year = self.create_financial_year()
        self.assertTrue(isinstance(financial_year,FinancialYear))
        self.assertEqual(financial_year.__str__(),financial_year.name)

class WardAllocationTest(TestCase):
    def create_ward_allocation(self):
        return WardAllocation.objects.create(
            ward = WardTest().create_ward(),
            financial_year = FinancialYearTest().create_financial_year(),
            amount = 2000000,
        )

    def test_ward_allocation_creation(self):
        ward_allocation = self.create_ward_allocation()
        self.assertTrue(isinstance(ward_allocation,WardAllocation))
        self.assertEqual(ward_allocation.__str__(),f"{ward_allocation.ward.name}'s allocation for financial year {ward_allocation.financial_year.name}")