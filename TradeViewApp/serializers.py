from rest_framework import serializers
from TradeViewApp.models import Server

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'server', 'symbol', 'out_function')