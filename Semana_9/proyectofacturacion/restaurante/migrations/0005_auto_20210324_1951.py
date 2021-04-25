# Generated by Django 3.1.7 on 2021-03-25 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0004_auto_20210324_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='platomodel',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, db_column='create_at', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platomodel',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, db_column='updated_at'),
        ),
    ]
