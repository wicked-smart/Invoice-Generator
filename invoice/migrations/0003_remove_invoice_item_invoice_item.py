# Generated by Django 4.2.7 on 2023-11-29 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_invoice_boughtitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='item',
        ),
        migrations.AddField(
            model_name='invoice',
            name='item',
            field=models.ManyToManyField(to='invoice.item'),
        ),
    ]