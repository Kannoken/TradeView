from django.shortcuts import render
from TradeViewApp.models import Server, StoreInfo
import json


def main(request):
    server = Server.objects.get(id='1')
    print(server.get_data())
    return render(request, 'index.html')