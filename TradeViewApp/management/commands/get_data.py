from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from TradeViewApp.models import Server


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.now().time().strftime("%H:%M:%S")
        for server in Server.objects.filter(interval_in_hour=now):
            print('WORK')
            server.refreash_data()