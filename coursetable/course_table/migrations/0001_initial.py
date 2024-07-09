# Generated by Django 4.2.13 on 2024-07-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('course_name', models.CharField(max_length=100)),
                ('instructor', models.CharField(max_length=100)),
                ('credits', models.IntegerField()),
            ],
        ),
    ]