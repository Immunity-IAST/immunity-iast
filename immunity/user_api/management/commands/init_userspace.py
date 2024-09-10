"""
Кастомная manage.py командп для инициализации системы при первом запуске.
"""

from user_api.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Запуск действий команды. """

        try:
            User.objects.get(username="admin")
            print("Администратор уже создан.")
        except:
            User.objects.create_superuser(username="admin", password="admin")