# Generated by Django 2.2.1 on 2019-10-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_issuer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='Qty_available',
        ),
        migrations.RemoveField(
            model_name='book',
            name='auther_name',
        ),
        migrations.AlterField(
            model_name='currently_issued',
            name='time_due',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
