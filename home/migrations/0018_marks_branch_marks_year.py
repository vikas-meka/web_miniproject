# Generated by Django 4.2.6 on 2023-10-31 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_teacher_branch_teacher_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='branch',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='marks',
            name='year',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
