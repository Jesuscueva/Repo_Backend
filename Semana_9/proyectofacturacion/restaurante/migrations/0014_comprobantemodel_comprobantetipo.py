# Generated by Django 3.1.7 on 2021-03-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0013_auto_20210329_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobantemodel',
            name='comprobanteTipo',
            field=models.IntegerField(choices=[(1, 'BOLETA'), (2, 'FACTURA')], db_column='comprobante_tipo', default=None),
            preserve_default=False,
        ),
    ]
