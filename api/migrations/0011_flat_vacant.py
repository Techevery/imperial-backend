# Generated by Django 4.1.1 on 2022-12-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_landlorddocument_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='vacant',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]