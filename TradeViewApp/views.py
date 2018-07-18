from django.shortcuts import render
from TradeViewApp.models import Server, StoreInfo
from TradeViewApp.forms import ServerForm
import json
import math

def main(request):
    form = ServerForm()
    server = Server.objects.all()
    if request.method == 'GET':
        pass
    string_data = StoreInfo.objects.first()
    create_data(string_data)
    return render(request, 'index.html', {'form':form, 'server': server})

def create_data(data):
    result = []
    tmp = []
    data = data.data.replace("\'", "\"")
    print(data)
    dic = json.loads(data)
    for key, value in dic.items():
        for k, val in value.items():
            result.append(k)
            tmp.append(k)
            for kk, v in val.items():
                if 'close' in kk.lower():
                    result[k].update({'close':float(v)})
                if 'open' in kk.lower():
                    tmp[k].update({'open': float(v)})
            abs = math.fabs(float(tmp[k]['open']) - float(result[k]['close']))
            percent = (tmp[k]['open']-result[k]['close'])/result[k]['close']*100
            result[k].update({'abs': abs, 'per': percent})
    print(result)