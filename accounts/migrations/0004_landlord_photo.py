# Generated by Django 4.1.1 on 2023-01-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_manager_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlord',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/landlord-pictures'),
        ),
    ]
