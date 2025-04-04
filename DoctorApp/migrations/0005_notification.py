# Generated by Django 5.1.5 on 2025-03-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoctorApp', '0004_rename_submitted_at_patientform_date_submitted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('Appointment', 'Appointment'), ('Form Submission', 'Form Submission'), ('Prescription', 'Prescription')], max_length=20)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
