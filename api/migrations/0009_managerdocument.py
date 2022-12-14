# Generated by Django 4.1.1 on 2022-12-05 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_landlorddocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('document', models.FileField(upload_to='documents/manager-documents')),
                ('date', models.DateField(auto_now_add=True)),
                ('house_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]