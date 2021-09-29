import requests
import json
import csv
import os
import math
import re
from pathlib import Path
from datetime import *

import pandas as pd
from allauth.account.decorators import login_required

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from requests.api import request

from .models import Sku, Order

# import numpy as np
# import re

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class CatalogView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog.html'

    # def __init__(self):
    #     get_sku_data(request)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # API_KEY = '91dd237119c46f9fcba63327d9a1ed48'
        # PASSWORD = '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'
        # SHOP_NAME = 'theperfectjean.myshopify.com'
        # VERSION = "2021-04"

        # cursor = connection.cursor()
        # cursor.execute("SELECT MAX(DATE(submitted_at)) AS last_data FROM inventory_order")
        # row = cursor.fetchone()

        # yesterday = datetime.today() - timedelta(days=1)
        # last_day = row[0]

        # last = 0
        # orders = []
        # while True:
        #     url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}/admin/api/{VERSION}/orders.json?limit=250&status=any&fields=id,fulfillments,created_at&since_id={last}&updated_at_min={last_day.strftime('%Y-%m-%d')}&updated_at_max={yesterday.strftime('%Y-%m-%d')}"
        #     response = requests.request("GET", url)

        #     result = response.json()['orders']

        #     for row in result:
        #         if 'fulfillments' not in row:
        #             break

        #         for fulfillment in row['fulfillments']:
        #             if 'line_items' not in fulfillment:
        #                 break

        #             for item in fulfillment['line_items']:
        #                 orders.append(Order(order_id=row['id'], \
        #                     status=fulfillment['status'], \
        #                     submitted_at=row['created_at'], \
        #                     sku_name=item['sku'], quantity=item['quantity']))

        #     if len(result) < 250:
        #         break
            
        #     last = result[-1]['id']
        
        # Order.objects.bulk_create(orders)
        
        # cursor.execute("UPDATE inventory_sku AS s SET s.sales_last_week = 0, sales_last_4_weeks = 0, sales_last_52_weeks = 0")

        # cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 1 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_week = i.sum_quantity WHERE s.sku_name = i.sku_name")

        # cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 4 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_4_weeks = i.sum_quantity WHERE s.sku_name = i.sku_name")

        # cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 52 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_52_weeks = i.sum_quantity WHERE s.sku_name = i.sku_name")

        search_value = request.GET.get('search_value', '').strip()
        sort_column = request.GET.get('sort_column', '')
        sort_dir = request.GET.get('sort_dir', '')

        data = Sku.objects.filter(Q(sku_id__contains=search_value) | Q(sku_name__contains=search_value) | Q(upc__contains=search_value)).order_by('sku_id')

        if sort_column:
            if sort_dir == 'asc':
                data = data.order_by(sort_column)
            else:
                data = data.order_by('-' + sort_column)

        # for row in data:
        #     row.average_week = row.sales_last_4_weeks / 4
        #     if row.average_week:
        #         row.weeks_available = math.ceil(row.available_to_sell / row.average_week)
        #     else:
        #         row.weeks_available = '∞'

        page_number = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 100)
        paginator = Paginator(data, per_page)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        context['data'] = page_obj
        context['search_value'] = search_value
        context['sort_column'] = sort_column
        context['sort_dir'] = sort_dir

        return self.render_to_response(context)


class ImportA2000View(LoginRequiredMixin, TemplateView):
    template_name = 'import_a2000.html'


@login_required
def export_excel(request):
    data = []
    skus = Sku.objects.all()

    for row in skus:
        data.append({
            'SKU': row.sku_name,
            'UPC': row.upc,
            'Prodcut Name': row.product_name,
            'Category': row.product_category,
            'Description': '',
            'Style': '',
            'Color': row.color,
            'Inseam': row.inseam,
            'Size': row.size,
            'Avaiable': row.available_to_sell,
            'Week avail.': row.weeks_available,
            'Current Status': row.current_status,
            'Replenishment': row.repl,
            'ETA': row.eta,
            'Future WA.': row.future_wa,
            'Future Status': row.future_status,
            'Throttle': '',
            'Repl. New': row.repl2,
            'ETA 2': '',
            'Fut. Status 2': row.future_status2,
            'Sales Last Wk.': row.sales_last_week,
            'Sales Last 4Wk.': row.sales_last_4_weeks,
            'Sales Last 52Wk.': row.sales_last_52_weeks,
            'Sales Best Week': '',
            'Sales Average Week': row.average_week
        })

    df = pd.DataFrame(data)
    df.to_excel('export.xlsx', index=False, header=True)

    with open('export.xlsx', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=export.xlsx'
        return response


@login_required
def get_token(request):
    pass


# @login_required
def get_data(request):
    create_callback()

    url = f"{settings.MASONHUB_URL}/snapshot_request"

    payload = {
        "snapshot_type": "full",
        "snapshot_as_of_date": "2021-08-05T08:15:30-07:00"
    }
    headers = {
        'Authorization': f'Bearer {settings.MASONHUB_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())

    return JsonResponse(response.json())


# @login_required
def snapshot_ready(request):
    json_data = json.loads(request.body.decode("utf-8"))
    download_url = json.loads(json_data['data'])['download_url']

    headers = {
        'Authorization': f'Bearer {settings.MASONHUB_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.request("GET", download_url, headers=headers, json={})

    return HttpResponse('')


def sku_inventory_change(request):
    json_data = json.loads(request.body.decode("utf-8"))
    data = json.loads(json_data['data'])
    for row in data:
        if isinstance(row, str):
            row = json.loads(row)

        selected = Sku.objects.filter(sku_id=row['sku_id']).first()
        if not selected:
            continue

        selected.available_to_sell = row['total_available_to_sell']
        selected.save()
    
    return JsonResponse({})

# @login_required
def create_callback(request):
    
    url = f"{settings.MASONHUB_URL}/callbacks"

    payload = [
        {
            # "url": f"https://{request.get_host()}/sku_inventory_change/",
            "url": f"https://agora.masonhub.co/callbacks/theperfectjean/skuInventoryChange",
            "message_type": "skuInventoryChange",
            "api_version": "2.0"
        }
    ]
    headers = {
        'Authorization': f'Bearer {settings.MASONHUB_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return JsonResponse({})


def get_sku_data(request):
    headers = {
        'Authorization': f'Bearer {settings.MASONHUB_TOKEN}',
        'Content-Type': 'application/json',
    }

    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE inventory_sku")

    offset = 0
    skus = []
    while True:
        url = f"{settings.MASONHUB_URL}/skus?include_counts=true&limit=100&offset={offset}"
        response = requests.request("GET", url, headers=headers, json={})

        result = response.json()['data']

        for row in result:
            color = ''
            if 'properties' in row and 'color' in row['properties'] and row['properties']['color']:
                color = row['properties']['color']
            elif 'customer_color' in row and row['customer_color']:
                color = row['customer_color']
            elif 'vendor_color' in row and row['vendor_color']:
                color = row['vendor_color']
            
            # if 'size' in row and row['size']:
            #     size = row['size']
            # elif 'properties' in row and 'size' in row['properties'] and row['properties']['size']:
            #     size = row['properties']['size']
            # elif 'properties' in row and 'First Choose Your Waist:' in row['properties'] and \
            #     row['properties']['First Choose Your Waist:']:
            #     size = row['properties']['First Choose Your Waist:']

            # if 'length' in row and row['length']:
            #     inseam = row['length']
            # elif 'properties' in row and 'length' in row['properties'] and \
            #     row['properties']['length']:
            #     inseam = row['properties']['length']
            # elif 'inseam' in row and row['inseam']:
            #     inseam = row['inseam']
            # elif 'properties' in row and \
            #     'That Waist is Available in these Lengths:' in row['properties'] and \
            #     row['properties']['That Waist is Available in these Lengths:']:
            #     inseam = row['properties']['That Waist is Available in these Lengths:']
            
            inseam = ''
            size = ''

            regex = re.compile(r'(\d{2})-(\d{2})')
            match = regex.search(row['unique_sku_name'])
            if match != None:
                inseam, size = match.groups()

            skus.append(Sku(sku_id=row['id'], sku_name=row['unique_sku_name'], \
                product_name=row['product_name'], product_category=row['product_category'], \
                product_description=row['product_description'], style=row['pick_style'], \
                color=color, inseam=inseam, size=size, upc=row['customer_bar_code'], \
                available_to_sell=row['inventory_totals']['total_available_to_sell']))

        if len(skus) >= 1000:
            Sku.objects.bulk_create(skus)
            skus = []
            
        if len(result) < 100:
            break

        offset = offset + 100
        
    Sku.objects.bulk_create(skus)

    return JsonResponse({})


# @login_required
def shopify_orders_data(request):
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE inventory_order")

    API_KEY = '91dd237119c46f9fcba63327d9a1ed48'
    PASSWORD = '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'
    SHOP_NAME = 'theperfectjean.myshopify.com'
    VERSION = "2021-04"

    last = 0
    orders = []
    while True:
        url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}/admin/api/{VERSION}/orders.json?limit=250&status=any&fields=id,fulfillments,created_at&since_id={last}&updated_at_min=2021-05-23"
        response = requests.request("GET", url)

        result = response.json()['orders']

        for row in result:
            if 'fulfillments' not in row:
                break

            for fulfillment in row['fulfillments']:
                if 'line_items' not in fulfillment:
                    break

                for item in fulfillment['line_items']:
                    orders.append(Order(order_id=row['id'], \
                        status=fulfillment['status'], \
                        submitted_at=row['created_at'], \
                        sku_name=item['sku'], quantity=item['quantity']))

        if len(orders) >= 1000:
            Order.objects.bulk_create(orders)
            orders = []

        if len(result) < 250:
            break
        
        last = result[-1]['id']
    
    if len(orders):
        Order.objects.bulk_create(orders)
        
    cursor = connection.cursor()

    cursor.execute("UPDATE inventory_sku AS s SET s.sales_last_week = 0, sales_last_4_weeks = 0, sales_last_52_weeks = 0")

    cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 1 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_week = i.sum_quantity WHERE s.sku_name = i.sku_name")

    cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 4 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_4_weeks = i.sum_quantity, s.average_week = CEIL(i.sum_quantity / 4), s.weeks_available = IF(i.sum_quantity = 0, 500, ROUND(s.available_to_sell / CEIL(i.sum_quantity / 4))) WHERE s.sku_name = i.sku_name")

    cursor.execute("UPDATE inventory_sku AS s, (SELECT SUM(quantity) AS sum_quantity, sku_name FROM inventory_order WHERE DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) >= DATE(submitted_at) AND DATE(submitted_at) >= DATE(DATE_SUB(NOW(), INTERVAL 52 WEEK)) GROUP BY sku_name) AS i SET s.sales_last_52_weeks = i.sum_quantity WHERE s.sku_name = i.sku_name")

    return JsonResponse({})


@login_required
def upload_a2000(request):
    BASE_DIR = Path(__file__).resolve().parent.parent

    file_obj = request.FILES.get('file')
    url = f"{os.path.join(BASE_DIR, 'uploads')}/{file_obj.name}"

    f = open(url, 'wb')
    for line in file_obj.chunks():
        f.write(line)
    f.close()

    try:
        df = pd.read_csv(url)
    except:
        df = pd.read_excel(url)
    
    request.session['a2000_url'] = url

    return JsonResponse({
        'name': file_obj.name,
        'size': file_obj.size,
        'src': f'/uploads/{file_obj.name}',
        'columns': df.columns.tolist()
    })


@login_required
def import_a2000(request):
    url = request.session.get('a2000_url', '')

    upc_column = request.POST.get('upc', '')
    eta_column = request.POST.get('eta', '')
    repl_column = request.POST.get('replenishment', '')
    size_inseam_column = request.POST.get('size-inseam', '')

    if not url or not upc_column or not eta_column or not repl_column or not size_inseam_column:
        return JsonResponse({
            'result': False
        })

    try:
        df = pd.read_csv(url)
    except:
        df = pd.read_excel(url)

    data = json.loads(df.to_json(orient='records'))

    for row in data:
        selected = Sku.objects.filter(upc=str(row[upc_column])).first()
        if not selected:
            continue

        size_inseam = row[size_inseam_column].split('/')
        if len(size_inseam) == 2:
            selected.size = size_inseam[0]
            selected.inseam = size_inseam[1]

        selected.eta = date.fromtimestamp(row[eta_column] / 1e3)
        selected.repl = row[repl_column]
        today = date.today()
        average_week = selected.sales_last_4_weeks / 4

        # Get current status and available weeks
        if average_week:
            weeks_available = math.round(selected.available_to_sell / average_week)
            if today + timedelta(days=weeks_available*7) < selected.eta:
                selected.current_status = 'RUNNING OUT'
            else:
                selected.current_status = 'ENOUGH INV'
        else:
            weeks_available = '∞'
            selected.current_status = 'ENOUGH INV'
        
        # Get Future WA
        date_delta = selected.eta - today
        remaining_inventory = selected.available_to_sell - average_week / 7 * date_delta.days
        if average_week:
            selected.future_wa = (remaining_inventory + selected.repl) / average_week
        else:
            selected.future_wa = 500

        # Get Future Status
        if selected.future_wa <= 25:
            selected.future_status = 'UNDERBOUGHT'
        else:
            selected.future_status = 'ENOUGH INV'

        # Get Repl. New
        selected.repl2 = (40 - selected.future_wa) * average_week

        # Get Fut. Status 2
        if selected.repl2 < 0:
            selected.future_status2 = 'OVERBOUGHT'
        else:
            selected.future_status2 = 'JUST RIGHT'

        selected.save()

        # selected.update(eta=eta, repl=repl, current_status=current_status)

    return JsonResponse({
        'result': True
    })


@login_required
def import_csv(request):
    BASE_DIR = Path(__file__).resolve().parent.parent

    url = f"{os.path.join(BASE_DIR, 'staticfiles')}/skus(masonhub).csv"
    df = pd.read_csv(url)

    data = json.loads(df.to_json(orient='records'))

    # BASE_DIR = Path(__file__).resolve().parent.parent
    # url = f"{os.path.join(BASE_DIR, 'staticfiles')}/skus(masonhub).csv"
    # df = pd.read_csv(url)
    # data = json.loads(df.to_json(orient='records'))

    # for row in data:
    #     if row['sales_last_4_weeks'] == '<nil>':
    #         row['average_week'] = 0
    #     else:
    #         row['average_week'] = int(row['sales_last_4_weeks']) / 4
        
    #     if row['average_week']:
    #         row['weeks_available'] = round(int(row['current_available']) / row['average_week'])
    #     else:
    #         row['weeks_available'] = '∞'


    # while True:
    #     url = f"{settings.MASONHUB_URL}/orders?list_type=summary&limit=100&offset={offset}"
    #     response = requests.request("GET", url, headers=headers, json={})

    #     result = response.json()['data']

    #     print(result)

    #     for row in result:
    #         if 'shipments' not in row:
    #             break

    #         for shipment in row['shipments']:
    #             if 'shipment_line_items' in shipment:
    #                 break

    #             for item in shipment['shipment_line_items']:
    #                 orders.append(Order(order_id=row['id'], status=shipment['status'], \
    #                     submitted_at=shipment['shipment_date_time'], \
    #                     sku_name=item['sku_customer_id'], quantity=item['quantity']))

    #     if len(result) < 100 or offset >= 1000:
    #         break

    #     offset = offset + 100

    return JsonResponse(data, safe=False)