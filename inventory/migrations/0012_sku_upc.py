# Generated by Django 3.2.4 on 2021-07-19 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_sku_future_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='upc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
