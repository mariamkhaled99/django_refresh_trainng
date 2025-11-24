from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from e_health.models import Patient, Doctor, Case, Treatment, Appointment
# ? for custom query examples
from django.db import connections

class Command(BaseCommand):
      # ? Refrence :
    help = 'Run test queries for data searching'

    def handle(self, *args, **options):
        
        self.test_queries()


    def test_queries(self):
        print("ORM example:")
        for p in Patient.objects.filter(last_name="Smith"):
            print("ORM ->", p.first_name, p.last_name)
