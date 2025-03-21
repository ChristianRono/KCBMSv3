from django.db import models
from education.models import Ward,KCBMSUser,FinancialYear

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(KCBMSUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female')
    )
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    admission_number = models.CharField(max_length=100)
    parents_name = models.CharField(max_length=100)
    parents_phone = models.CharField(max_length=15)
    parents_id = models.FileField()
    school_name = models.CharField(max_length=100)
    SCHOOL_TYPE_CHOICES = (
        ('primary','Primary School'),
        ('secondary','Secondary School'),
        ('tertiary','Tertiary School'),
    )
    school_type = models.CharField(max_length=100,choices=SCHOOL_TYPE_CHOICES)
    bank_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    year_of_completion = models.IntegerField()
    disability_status = models.BooleanField(default=False)
    FAMILY_STATUS_CHOICES = (
        ('orphan','Orphan'),
        ('single parents','Single Parents'),
        ('both parents','Both Parents'),
    )
    family_status = models.CharField(max_length=30,choices=FAMILY_STATUS_CHOICES)
    death_certificate_father = models.FileField(blank=True,null=True)
    death_certificate_mother = models.FileField(blank=True,null=True)
    family_income = models.IntegerField()
    applied_bursary_before = models.BooleanField()
    annual_school_fees = models.IntegerField()
    ward = models.ForeignKey(Ward,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Sibling(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=10)
    annual_fees = models.IntegerField()
    fees_paid = models.IntegerField()
    arreas = models.IntegerField()

    def __str__(self):
        return self.name

class Application(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    fee_balance = models.IntegerField()
    fee_statement = models.FileField()
    previous_term_report = models.FileField()
    is_awarded = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    reasons = models.TextField(blank=True)
    amount = models.IntegerField(default=0)
    financial_year = models.ForeignKey(FinancialYear,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.financial_year.name}"