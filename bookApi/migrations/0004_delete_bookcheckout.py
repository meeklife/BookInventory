# Generated by Django 4.2.6 on 2023-11-04 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookApi', '0003_rename_title_bookcheckout_book'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookCheckout',
        ),
    ]
