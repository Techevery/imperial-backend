# Generated by Django 4.1.1 on 2023-02-23 08:05

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_rename_next_of_kin_manager_next_of_kin_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='next_of_kin_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='next_of_kin_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='next_of_kin_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]