from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import FloatField
from e_health.models import Patient, Doctor, Case, Treatment, Appointment
# ? for custom query examples
from django.db.models import Avg, Max, Min, Count, Q
from django.db.models import Q
class Command(BaseCommand):
    # ? Refrence : https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
    help = 'Run test queries for data aggregation'

    def handle(self, *args, **options):
        
        self.test_queries()


    def test_queries(self):
        print("ORM example:")
        for p in Patient.objects.filter(last_name="Smith"):
            print("ORM ->", p.first_name, p.last_name)
        # * Count Example *
        res = Patient.objects.count()
        print("Total Patients:", res)
        # * aggregate Avg,Max,Min Example *
        """ aggregate():
            Calculates summary values (like sum, average, min, max) over the entire queryset."""
        res=Doctor.objects.aggregate(average_fee=Avg('consultation_fee',default=10,output_field=FloatField()), max_fee=Max('consultation_fee',default=100,output_field=FloatField()), min_fee=Min('consultation_fee',default=5,output_field=FloatField()))
        print("Age Aggregates:", res)
         # * annotate Example *
        """annotate():
          Calculates summary values for each object in the queryset (per row)"""
          
        """The order of values() and annotate() is crucial:

values() → annotate(): Groups by the fields in values() and then annotates each group
annotate() → values(): Annotates all objects first, then values()"""
        res1= Patient.objects.annotate(num_cases=Count('cases')).values('first_name', 'num_cases')
        print("=======================================================================")
        print("SQL Query`:", str(res1.query))  
        print("Age Annotates value after values():", list(res1))
        res2= Patient.objects.values('first_name').annotate(num_cases=Count('cases'))
        print("=======================================================================")
        print("SQL Query2:", str(res2.query))  
        print("Age Annotates value before values():", list(res2))
        
        # * Q Example *
        """Q objects:   """
        high_priority_cases = Case.objects.filter(Q(priority__gte=4) | Q(severity='SEVERE'))
        print("High Priority Cases:", list(high_priority_cases))
        
        

        