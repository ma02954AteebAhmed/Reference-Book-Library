# Generated by Django 2.2.1 on 2019-10-14 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_issuer', '0003_currently_issued_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='books_issued',
            name='barcode',
            field=models.CharField(default=False, max_length=12),
            preserve_default=False,
        ),
    ]
