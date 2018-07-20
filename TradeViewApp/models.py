from django.db import models
import requests
import json
from django.db import IntegrityError
from datetime import datetime


class Server(models.Model):
    def __str__(self):
        return self.server+' ('+self.symbol+')'

    server = models.CharField(default='https://www.alphavantage.co/', max_length=255, verbose_name='Название сервера')
    key = models.CharField(default='O8TY56AICAWDOPWM', max_length=255)
    symbol = models.CharField(max_length=255, default='MSFT', verbose_name='символ акций компании')
    interval_in_hour = models.IntegerField(verbose_name="Интервал запроса", default=1)
    out_function = models.CharField(default='TIME_SERIES_DAILY', max_length=255)

    def refreash_data(self):
        req  = self.server+'query?function='+self.out_function+'&symbol='+self.symbol+'&apikey='+self.key
        header = {"Content-type": "Application/json"}
        r = requests.get(req, headers=header)
        data = json.loads(r.text)
        meta = data['Meta Data']
        del data['Meta Data']
        last_refreash = ''
        for key in meta:
            if 'refreshed' in key.lower():

                last_refreash = meta[key]

        StoreInfo.objects.create(date=last_refreash, server=self, data=data)


class StoreInfo(models.Model):

    def __str__(self):
        return str(self.date)

    date = models.DateField(verbose_name='Дата обновления на сервере', editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='Настройки запроса к серверу')
    data = models.TextField(default='', verbose_name='Информация из сервера')

    class Meta:
        ordering = ['-date']
        unique_together = ('date', 'server')