# Generated by Django 5.0.3 on 2024-03-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PIZZA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='in_id',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
    ]