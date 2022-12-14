# Generated by Django 4.1.1 on 2022-10-29 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_adddocument_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MakePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('amount', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('online payment', 'online_payment'), ('transfer', 'transfer')], max_length=100)),
                ('ref_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='documents/tenant-payments')),
                ('status', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]