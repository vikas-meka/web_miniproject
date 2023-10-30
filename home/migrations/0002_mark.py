# Generated by Django 4.2.6 on 2023-10-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=150)),
                ('course', models.CharField(max_length=150)),
                ('ct1', models.IntegerField(blank=True)),
                ('ct2', models.IntegerField(blank=True)),
                ('end', models.IntegerField(blank=True)),
                ('internals', models.IntegerField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('grade', models.IntegerField(blank=True)),
                ('score', models.CharField(blank=True, max_length=1)),
            ],
        ),
    ]
