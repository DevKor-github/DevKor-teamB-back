# Generated by Django 5.0.6 on 2024-07-31 05:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificationcode",
            name="email",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
