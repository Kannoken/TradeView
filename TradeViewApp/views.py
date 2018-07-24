from django.shortcuts import render, HttpResponse
from TradeViewApp.models import Server, StoreInfo
from TradeViewApp.forms import ServerForm
import json
from django.views.decorators.csrf import csrf_exempt
from TradeViewApp.serializers import ServerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions



@csrf_exempt
def main(request):
    form = ServerForm()
    server = Server.objects.all()
    if not Server.objects.all():
        ser = Server.objects.create()
        ser.save()
    result = {}
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
    return render(request, 'index.html', {'form':form, 'servers': server, 'result':reversed(sorted(result.items())), 'symbol': symbol})

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
                    result[k].update({'close':float(v)})
                if 'open' in kk.lower():
                    tmp[k].update({'open': float(v)})
            abs = round(float(tmp[k]['open']) - float(result[k]['close']), 2)
            percent = round((tmp[k]['open']-result[k]['close'])/result[k]['close']*100, 2)
            result[k].update({'abs': abs, 'per': percent})
    return result

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def servers_list(request):
    if request.method == 'GET':
        snippets = Server.objects.all()
        serializer = ServerSerializer(snippets, many=True)
        print(serializer.data)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def server_detail(request, pk):
    snippet = Server.objects.get(pk=pk)
    print(snippet)
    if request.method == 'GET':
        serializer = ServerSerializer(snippet)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def server_symbols(request):
    servers = Server.objects.all()
    serializer = ServerSerializer(servers, many=True)
    print(serializer.data)
    return Response(serializer.data)


