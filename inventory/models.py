from django.db import models


class Sku(models.Model):
    sku_id = models.CharField(max_length=50)
    sku_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    product_category = models.CharField(max_length=50, blank=True, null=True)
    product_description = models.CharField(max_length=255, blank=True, null=True)
    style = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    inseam = models.CharField(max_length=50, blank=True, null=True)
    available_to_sell = models.IntegerField(default=0)
    sales_last_week = models.IntegerField(default=0)
    sales_last_4_weeks = models.IntegerField(default=0)
    sales_last_52_weeks = models.IntegerField(default=0)
    current_status = models.CharField(max_length=50, blank=True, null=True)
    eta = models.DateField(auto_now_add=True)
    repl = models.IntegerField(default=0)
    future_wa = models.IntegerField(default=0)
    future_status = models.CharField(max_length=50, blank=True, null=True)
    repl2 = models.IntegerField(default=0)
    eta2 = models.DateField(auto_now_add=True)
    future_status2 = models.CharField(max_length=50, blank=True, null=True)


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, blank=True, null=True)
    order_type = models.CharField(max_length=20, blank=True, null=True)
    submitted_at = models.DateTimeField()
    sku_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)