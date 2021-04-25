# Generated by Django 3.1.7 on 2021-03-28 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0010_auto_20210328_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabeceracomandamodel',
            name='comprobante',
            field=models.ForeignKey(db_column='comprobante_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurante.comprobantemodel'),
        ),
        migrations.AlterField(
            model_name='detallecomandamodel',
            name='cabecera',
            field=models.ForeignKey(db_column='cabecera_id', on_delete=django.db.models.deletion.PROTECT, related_name='cabeceraDetalles', to='restaurante.cabeceracomandamodel'),
        ),
        migrations.AlterField(
            model_name='detallecomandamodel',
            name='plato',
            field=models.ForeignKey(db_column='plato_id', on_delete=django.db.models.deletion.PROTECT, related_name='PlatoDetalles', to='restaurante.platomodel'),
        ),
    ]