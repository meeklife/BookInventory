# Generated by Django 4.2.6 on 2023-11-03 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookApi', '0002_bookcheckout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookcheckout',
            old_name='title',
            new_name='book',
        ),
    ]
