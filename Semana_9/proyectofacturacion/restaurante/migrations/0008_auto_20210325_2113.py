# Generated by Django 3.1.7 on 2021-03-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0007_auto_20210325_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesamodel',
            name='mesaCapacidad',
            field=models.IntegerField(db_column='mesa_capacidad'),
        ),
    ]
