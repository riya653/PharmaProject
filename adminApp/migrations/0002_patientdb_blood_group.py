# Generated by Django 5.1.5 on 2025-02-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdb',
            name='Blood_Group',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
