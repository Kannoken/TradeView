from rest_framework import serializers
from TradeViewApp.models import Server

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ('server', 'symbo;', 'out_function')