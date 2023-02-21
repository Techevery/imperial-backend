# Generated by Django 4.1.1 on 2023-02-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_manager_emergency_contact_info_manager_gender_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='next_of_kin',
            new_name='next_of_kin_number',
        ),
        migrations.AddField(
            model_name='manager',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
