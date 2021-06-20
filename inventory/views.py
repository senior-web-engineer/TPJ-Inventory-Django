import requests
import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import pandas as pd
# import numpy as np
# import re


class GetToken(TemplateView):
    template_name = 'base.html'


def get_token(request):
    pass


def get_data(request):
    create_callback()

    url = "https://sandbox.masonhub.co/theperfectjean/api/v1/snapshot_request"

    payload = {
        "snapshot_type": "full",
        "snapshot_as_of_date": "2021-08-05T08:15:30-07:00"
    }
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZWNyZXRfcGhyYXNlIjoibW92ZW1lbnQgdGhhdCB5b3VyIG1hbiBwYXJ0cyByZXF1aXJlIiwic3lzdGVtX2lkIjpudWxsLCJleHAiOjQ3NzYzMzk4MjIsImlhdCI6MTYyMjczOTgyMiwiaXNzIjoiTWFzb25IdWIifQ.OiqFs9cYzd_dtCYNO0cvjAxPpaBz7CtKfJgyLtWr4_s',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())

    return JsonResponse(response.json())


def snapshot_ready(request):
    json_data = json.loads(request.body.decode("utf-8"))
    print(json_data)
    download_url = json.loads(json_data['data'])['download_url']
    print(download_url)

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZWNyZXRfcGhyYXNlIjoibW92ZW1lbnQgdGhhdCB5b3VyIG1hbiBwYXJ0cyByZXF1aXJlIiwic3lzdGVtX2lkIjpudWxsLCJleHAiOjQ3NzYzMzk4MjIsImlhdCI6MTYyMjczOTgyMiwiaXNzIjoiTWFzb25IdWIifQ.OiqFs9cYzd_dtCYNO0cvjAxPpaBz7CtKfJgyLtWr4_s',
        'Content-Type': 'application/json',
    }

    response = requests.request("GET", download_url, headers=headers, json={})
    print(response.json())

    return HttpResponse('')


def create_callback():
    url = "https://sandbox.masonhub.co/theperfectjean/api/v1/callbacks"

    payload = [
        {
            "url": "https://tpj-inventory.herokuapp.com/snapshot_ready/",
            "message_type": "snapshotReady",
            "api_version": "2.0"
        }
    ]
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZWNyZXRfcGhyYXNlIjoibW92ZW1lbnQgdGhhdCB5b3VyIG1hbiBwYXJ0cyByZXF1aXJlIiwic3lzdGVtX2lkIjpudWxsLCJleHAiOjQ3NzYzMzk4MjIsImlhdCI6MTYyMjczOTgyMiwiaXNzIjoiTWFzb25IdWIifQ.OiqFs9cYzd_dtCYNO0cvjAxPpaBz7CtKfJgyLtWr4_s',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text)