# Generated by Django 4.2.5 on 2023-09-08 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0001_initial'),
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='education.ward'),
        ),
        migrations.AddField(
            model_name='application',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.financialyear'),
        ),
        migrations.AddField(
            model_name='application',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.profile'),
        ),
    ]
