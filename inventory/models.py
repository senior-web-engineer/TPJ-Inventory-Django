from django.db import models


class Sku(models.Model):
    sku_id = models.CharField(max_length=50)
    sku_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=50)
    product_description = models.CharField(max_length=255)
    style = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    size = models.IntegerField()
    available_to_sell = models.IntegerField()
    sales_last_week = models.IntegerField()
    sales_last_4_weeks = models.IntegerField()
    sales_last_52_weeks = models.IntegerField()


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20)
    submitted_at = models.DateTimeField()
    sku_name = models.CharField(max_length=50)
    quantity = models.IntegerField()