from django.shortcuts import render
from TradeViewApp.models import Server, StoreInfo
from TradeViewApp.forms import ServerForm
import json


def main(request):
    servers = Server.objects.all()
    return render(request, 'index.html', {'servers': servers})