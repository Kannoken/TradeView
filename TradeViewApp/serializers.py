from rest_framework import serializers
from TradeViewApp.models import Server, StoreInfo


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInfo
        fields = ('id', 'date', 'data')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'server', 'symbol', 'out_function')

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(ServerSerializer, self).get_field_names(*args, **kwargs)
