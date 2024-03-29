# Generated by Django 4.1.1 on 2023-01-04 07:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_flat_all_tenants_flat_current_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='all_tenants',
            field=models.ManyToManyField(blank=True, related_name='tenant_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
