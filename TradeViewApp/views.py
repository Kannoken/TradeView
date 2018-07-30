from django.shortcuts import render, HttpResponse
from TradeViewApp.models import Server, StoreInfo
from TradeViewApp.forms import ServerForm
import json
from django.views.decorators.csrf import csrf_exempt
from TradeViewApp.serializers import ServerSerializer, InfoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


@csrf_exempt
def main(request):
    form = ServerForm()
    server = Server.objects.all()
    if not Server.objects.all():
        ser = Server.objects.create()
        ser.save()
    symbol = {}
    if request.method == 'POST' and request.POST.get('id'):
        data = StoreInfo.objects.filter(server=request.POST['id']).first()
        if not data:
            serv = Server.objects.get(id=request.POST['id'])
            serv.refreash_data()
            symbol['name'] = server.symbol

        f = StoreInfo.objects.filter(server=request.POST['id']).last()
        result = create_data(f)
        return HttpResponse(json.dumps({'result': result, 'symbol': symbol}), content_type="application/json")

    else:
        string_data = StoreInfo.objects.first()
        if not string_data:
            serv = Server.objects.last()
            serv.refreash_data()
            symbol['name'] = serv.symbol
            string_data = StoreInfo.objects.last()
        result = create_data(string_data)
    return render(request, 'index.html',
                  {'form': form, 'servers': server, 'result': reversed(sorted(result.items())), 'symbol': symbol})


def create_data(data):
    result = {}
    tmp = {}
    data = data.data.replace("\'", "\"")
    dic = json.loads(data)
    for key, value in dic.items():
        for k, val in value.items():
            result[k] = {}
            tmp[k] = {}
            for kk, v in val.items():
                if 'close' in kk.lower():
                    result[k].update({'close': float(v)})
                if 'open' in kk.lower():
                    tmp[k].update({'open': float(v)})
            abs = round(float(tmp[k]['open']) - float(result[k]['close']), 2)
            percent = round((tmp[k]['open'] - result[k]['close']) / result[k]['close'] * 100, 2)
            result[k].update({'разница': abs, 'разница в процентах': percent})
    return result


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def servers_list(request):
    snippets = Server.objects.all()
    serializer = ServerSerializer(snippets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def server_detail(request, pk):
    server = Server.objects.get(pk=pk)
    serializer = ServerSerializer(server)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def server_symbols_data(request, symbol, fields):
    result = {}
    fields = fields.split(',')
    data = StoreInfo.objects.filter(server__symbol=symbol)
    serializer = InfoSerializer(data, many=True)
    data = dict(serializer.data[0])['data']
    data = json.loads(data.replace("\'", "\""))
    for value in data.values():
        for key, val in value.items():
            for k, v in val.items():
                for x in fields:
                    if x.lower() in k.lower():
                        if result.get(key):
                            result[key].update({k: v})
                        else:
                            result[key] = {k: v}
    return Response(result)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def server_symbols(request, symbol=None):
    if symbol:
        data = StoreInfo.objects.filter(server__symbol=symbol)
        serializer = InfoSerializer(data, many=True)
    else:
        server = Server.objects.all()
        serializer = ServerSerializer(server, context={'fields': ['symbol']}, many=True)
    return Response(serializer.data)
