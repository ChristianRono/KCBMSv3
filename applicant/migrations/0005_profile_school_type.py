# Generated by Django 4.2.5 on 2023-09-13 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0004_alter_application_amount_alter_application_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='school_type',
            field=models.CharField(choices=[('primary', 'Primary School'), ('secondary', 'Secondary School'), ('tertiary', 'Tertiary School')], default='primary', max_length=100),
            preserve_default=False,
        ),
    ]
