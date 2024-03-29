# Generated by Django 3.2.4 on 2021-07-05 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_sku_inseam'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='eta',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='eta2',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='future_status',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='future_wa',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sku',
            name='repl',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sku',
            name='repl2',
            field=models.IntegerField(default=0),
        ),
    ]
