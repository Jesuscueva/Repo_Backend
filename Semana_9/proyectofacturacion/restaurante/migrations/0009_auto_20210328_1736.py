# Generated by Django 3.1.7 on 2021-03-28 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0008_auto_20210325_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabeceracomandamodel',
            name='comprobante',
            field=models.ForeignKey(db_column='comprobante_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurante.comprobantemodel'),
        ),
    ]
