# Generated by Django 4.2.5 on 2023-09-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kcbmsuser',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='kcbmsuser',
            name='is_edu_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='kcbmsuser',
            name='is_ward_admin',
            field=models.BooleanField(default=False),
        ),
    ]
