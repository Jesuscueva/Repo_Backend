# Generated by Django 3.1.7 on 2021-03-29 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0012_delete_personalmesamodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabeceracomandamodel',
            name='mesa',
            field=models.ForeignKey(db_column='mesa_id', on_delete=django.db.models.deletion.PROTECT, related_name='mesaCabeceras', to='restaurante.mesamodel'),
        ),
        migrations.AlterField(
            model_name='cabeceracomandamodel',
            name='mozo',
            field=models.ForeignKey(db_column='mozo_id', on_delete=django.db.models.deletion.PROTECT, related_name='mozoCabecera', to=settings.AUTH_USER_MODEL),
        ),
    ]
