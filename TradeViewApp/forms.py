from django.forms import ModelForm
from django import forms
from TradeViewApp.models import Server, StoreInfo


class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = ['key', 'symbol', 'out_function']
