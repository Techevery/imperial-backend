# Generated by Django 4.1.1 on 2022-10-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_tenant_name_tenant_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='annual_salary',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='former_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='guarantor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='next_of_kin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='place_of_work',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='position_at_work',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='purpose_of_rent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
