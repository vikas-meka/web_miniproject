# Generated by Django 4.2.6 on 2023-10-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='roll_no',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
