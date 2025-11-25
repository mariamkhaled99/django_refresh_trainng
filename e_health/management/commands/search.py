from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from e_health.models import Patient, Doctor, Case, Treatment, Appointment
from django.db.models import F, ExpressionWrapper, DecimalField,Count,window

# ? for custom query examples
from django.db import connections
from django.db.models import F, Func

class Command(BaseCommand):
      # ? Refrence :
    help = 'Run test queries for data searching'

    def handle(self, *args, **options):
        
        self.test_queries()


    def test_queries(self):
        print("Exact matching search (only this value):")
        for p in Patient.objects.filter(last_name="Smith"):
            print("ORM ->", p.first_name, p.last_name)

        print("Case-sensitive search (contains this value):")
        # This will only match names containing 'John' exactly (e.g., 'John', 'Johnny'), but NOT 'john' or 'JOHN'
        for p in Patient.objects.filter(first_name__contains="John"):
            print("ORM ->", p.first_name)

        print("Case-insensitive search (icontains):")
        # This will match any case variation, e.g., 'john', 'JOHN', 'JoHn', 'Johnny'
        for p in Patient.objects.filter(first_name__icontains="john"):
            print("ORM ->", p.first_name)

        print("Case-insensitive search in specialization:")
        for d in Doctor.objects.filter(specialization__icontains="cardio"):
            print("ORM ->", d.user.first_name, d.user.last_name, d.specialization)
            
            
        # print("similarity search using TrigramSimilarity:")
        # #* Note:trigram_similar lookup is only supported with PostgreSQL
        # """To use trigram similarity search, you need to enable the pg_trgm extension in your PostgreSQL database.
        # You can do this by executing the following SQL command in your database:
        # postgres=# CREATE EXTENSION IF NOT EXISTS pg_trgm;
        # CREATE EXTENSION
        # postgres=# SELECT * FROM pg_extension WHERE extname = 'pg_trgm';"""
        
        # for p in Patient.objects.filter(first_name__trigram_similar="john"):
        #     print("ORM ->", p.first_name)
        

        print("Date range search:")
        # find all appointments scheduled between January 1, 2023 and December 31, 2023
        from datetime import date
        start_date = date(2024, 11, 1)
        end_date = date(2025, 11, 25)
        for a in Appointment.objects.filter(appointment_date__range=(start_date, end_date)):
            print("ORM ->", a.patient.first_name,a.appointment_date)
            
            
        print("Using F() to compare fields:")
        res = Appointment.objects.annotate(
    is_over_priced=ExpressionWrapper(F('actual_cost') - F('estimated_cost'), output_field=DecimalField())
).filter(is_over_priced__gt=1000)        
        print(res)
        
        from django.db.models import OuterRef, Subquery,Exists,Q, When

            
            
        print("Using Func() for database functions:")
        appointment_subquery = Appointment.objects.filter(
            doctor=OuterRef("pk")
        )

        #

        doctors_with_appointments = Doctor.objects.annotate(
            has_appointments=Exists(appointment_subquery)
        )

        for doctor in doctors_with_appointments:
            print(doctor.user.first_name, doctor.has_appointments)
            
            
        # subquery single column limitation example
        print("Using Subquery() for subqueries:")
        appoinments = Appointment.objects.filter(
            appointment_date=f'2025-11-25',
        )
        
        patient_going_appointments = Appointment.objects.filter(patient_id__in=Subquery(appoinments.values('patient_id')))
        print(f"patient_going_appointments: {patient_going_appointments}")
        
        from django.db.models import Case, When, Value, IntegerField, Q

        filter_when = Patient.objects.annotate(
    is_special=Case(
        When(Q(first_name__startswith="John") | Q(last_name__startswith="M"), then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
    )
).exclude(
    gender="F"   
).filter(
    is_special=1
)

        
        print(f"filter_when: {filter_when}")
        from django.db.models.lookups import GreaterThan, GreaterThanOrEqual
        
        


        
        filter_when=Appointment.objects.annotate(is_overpriced=Case(
    When(GreaterThanOrEqual(F('actual_cost'), F('estimated_cost')), then=Value(1)),
 
    )  )
        
        print(f"filter_when: {filter_when}")
        
        
        filter_based_on_choice = Appointment.objects.aggregate(
            
            CONSULTATION=Count( 'pk',filter=Q(appointment_type='CONSULTATION')),
            All=Count( 'pk',filter=~Q(appointment_type__isnull=True))
           
            
        )
        print(f"filter_based_on_choice: {filter_based_on_choice}")
        
        print("window functions using Over():")
        
        
        



                
        
        
