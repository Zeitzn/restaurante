# Generated by Django 2.2.7 on 2019-12-04 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_pedido_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='numero',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='tipo',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]