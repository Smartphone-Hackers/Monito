# Generated by Django 2.2.7 on 2020-04-28 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_addexpenses_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpenses',
            name='date',
            field=models.DateField(),
        ),
    ]
