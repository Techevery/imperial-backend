# Generated by Django 4.1.1 on 2022-12-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_makepayment_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpayment',
            name='type',
            field=models.CharField(blank=True, choices=[('one-off', 'one-off'), ('recurring', 'recurring')], max_length=100, null=True),
        ),
    ]
