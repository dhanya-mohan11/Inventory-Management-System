# Generated by Django 5.0.3 on 2024-03-19 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='user',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='user',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='user',
        ),
    ]
