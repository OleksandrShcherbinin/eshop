# Generated by Django 4.2.4 on 2023-09-09 09:49
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
    ]
