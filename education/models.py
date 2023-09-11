from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class KCBMSUser(AbstractUser):
    is_ward_admin = models.BooleanField(default=False)
    is_edu_admin = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class FinancialYear(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    is_editable = models.BooleanField()

    def __str__(self):
        return self.name

class Ward(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WardAllocation(models.Model):
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.ward.name}'s allocation for financial year {self.financial_year.name}"