# Generated by Django 3.2.4 on 2021-07-06 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_sku_future_status2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='future_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
