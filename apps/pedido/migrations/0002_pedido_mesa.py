# Generated by Django 2.2.7 on 2019-11-06 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='mesa',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
    ]