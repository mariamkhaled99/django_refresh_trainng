from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from e_health.models import Patient, Doctor, Case, Treatment, Appointment
# ? for custom query examples
from django.db import connections

class Command(BaseCommand):
    help = 'Insert sample data and run test queries'

    def handle(self, *args, **options):
        self.insert_sample_data()
        self.test_queries()

    def insert_sample_data(self):
        
        Appointment.objects.all().delete()  
        Case.objects.all().delete()  
        Treatment.objects.all().delete()  
        Doctor.objects.all().delete()  
        Patient.objects.all().delete()  
        User.objects.filter(username__startswith="dr_").delete()  
        
        # Create Patients  
        patient1 = Patient.objects.create(first_name="Mariam", last_name="Eissa", date_of_birth="1999-01-01", gender='F', email="mariam@example.com")  
        patient2 = Patient.objects.create(first_name="John", last_name="Smith", date_of_birth="1990-05-10", gender='M', email="john@example.com")  
        patient3 = Patient.objects.create(first_name="Sarah", last_name="Johnson", date_of_birth="1985-03-15", gender='F', email="sarah@example.com")  
        patient4 = Patient.objects.create(first_name="Mike", last_name="Brown", date_of_birth="1992-07-20", gender='M', email="mike@example.com")  
        patient5 = Patient.objects.create(first_name="Emma", last_name="Davis", date_of_birth="1988-11-30", gender='F', email="emma@example.com")  
        # Add similar names for icontains/trigram_similar tests
        patient6 = Patient.objects.create(first_name="Helen", last_name="Mirren", date_of_birth="1970-04-12", gender='F', email="helen@example.com")
        patient7 = Patient.objects.create(first_name="Helena", last_name="Joy", date_of_birth="1982-08-23", gender='F', email="helena@example.com")
        patient8 = Patient.objects.create(first_name="Hélène", last_name="Smith", date_of_birth="1995-02-17", gender='F', email="helene@example.com")
    
        # Create Users for Doctors - Note: Multiple doctors with same first name "Ahmed"  
        user1 = User.objects.create_user(username="dr_ahmed1", first_name="Ahmed", last_name="Khaled", email="ahmed1@hospital.com", password="test1234")  
        user2 = User.objects.create_user(username="dr_sara", first_name="Sara", last_name="Ali", email="sara@hospital.com", password="test1234")  
        user3 = User.objects.create_user(username="dr_ahmed2", first_name="Ahmed", last_name="Hassan", email="ahmed2@hospital.com", password="test1234")  
        user4 = User.objects.create_user(username="dr_john", first_name="John", last_name="Wilson", email="john@hospital.com", password="test1234")  
        user5 = User.objects.create_user(username="dr_ahmed3", first_name="Ahmed", last_name="Mohamed", email="ahmed3@hospital.com", password="test1234")  
    
        # Create Doctors with varying experience  
        doctor1 = Doctor.objects.create(user=user1, license_number="LIC12345", medical_degree="MD", specialization="Cardiology", years_of_experience=10)  
        doctor2 = Doctor.objects.create(user=user2, license_number="LIC67890", medical_degree="MBBS", specialization="Neurology", years_of_experience=7)  
        doctor3 = Doctor.objects.create(user=user3, license_number="LIC11111", medical_degree="MD", specialization="Cardiology", years_of_experience=15)  
        doctor4 = Doctor.objects.create(user=user4, license_number="LIC22222", medical_degree="DO", specialization="Orthopedics", years_of_experience=5)  
        doctor5 = Doctor.objects.create(user=user5, license_number="LIC33333", medical_degree="MBBS", specialization="Pediatrics", years_of_experience=12)  
    
        # Create Treatments with varying costs  
        treatment1 = Treatment.objects.create(  
            name="ECG", code="TREAT001", description="Electrocardiogram diagnostic test", category="DIAGNOSTIC",  
            base_cost=100.00, insurance_coverage_percentage=80.00, estimated_duration_minutes=15  
        )  
        treatment2 = Treatment.objects.create(  
            name="Physical Therapy", code="TREAT002", description="Therapy for muscle recovery", category="THERAPY",  
            base_cost=200.00, insurance_coverage_percentage=60.00, estimated_duration_minutes=60  
        )  
        treatment3 = Treatment.objects.create(  
            name="MRI Scan", code="TREAT003", description="Magnetic Resonance Imaging", category="DIAGNOSTIC",  
            base_cost=500.00, insurance_coverage_percentage=70.00, estimated_duration_minutes=45  
        )  
        treatment4 = Treatment.objects.create(  
            name="Blood Test", code="TREAT004", description="Complete blood count", category="DIAGNOSTIC",  
            base_cost=50.00, insurance_coverage_percentage=90.00, estimated_duration_minutes=10  
        )  
        treatment5 = Treatment.objects.create(  
            name="Surgery Consultation", code="TREAT005", description="Pre-surgery consultation", category="CONSULTATION",  
            base_cost=300.00, insurance_coverage_percentage=50.00, estimated_duration_minutes=30  
        )  
    
        # Create Cases - doctor1 (Ahmed Khaled) has 3 cases, doctor3 (Ahmed Hassan) has 2 cases  
        case1 = Case.objects.create(  
            patient=patient1, primary_doctor=doctor1, referring_doctor=doctor2,  
            chief_complaint="Chest pain", symptoms_description="Sharp pain in chest",  
            status="OPEN", priority=2, severity="MODERATE"  
        )  
        case2 = Case.objects.create(  
            patient=patient2, primary_doctor=doctor2,  
            chief_complaint="Headache", symptoms_description="Persistent headache",  
            status="IN_PROGRESS", priority=3, severity="MILD"  
        )  
        case3 = Case.objects.create(  
            patient=patient3, primary_doctor=doctor1,  
            chief_complaint="Heart palpitations", symptoms_description="Irregular heartbeat",  
            status="OPEN", priority=1, severity="SEVERE"  
        )  
        case4 = Case.objects.create(  
            patient=patient4, primary_doctor=doctor3,  
            chief_complaint="Back pain", symptoms_description="Lower back pain",  
            status="IN_PROGRESS", priority=2, severity="MODERATE"  
        )  
        case5 = Case.objects.create(  
            patient=patient5, primary_doctor=doctor1,  
            chief_complaint="Shortness of breath", symptoms_description="Difficulty breathing",  
            status="OPEN", priority=1, severity="SEVERE"  
        )  
        case6 = Case.objects.create(  
            patient=patient1, primary_doctor=doctor3,  
            chief_complaint="Chest X-ray follow-up", symptoms_description="Follow-up examination",  
            status="CLOSED", priority=3, severity="MILD"  
        )  
        case7 = Case.objects.create(  
            patient=patient2, primary_doctor=doctor4,  
            chief_complaint="Knee injury", symptoms_description="Sports injury",  
            status="IN_PROGRESS", priority=2, severity="MODERATE"  
        )  
    
        # Create Appointments with varying costs  
        Appointment.objects.create(  
            patient=patient1, doctor=doctor1, case=case1, treatment=treatment1,  
            appointment_date="2025-11-25", appointment_time="09:00",  
            appointment_type="DIAGNOSTIC", purpose="ECG test", status="SCHEDULED", priority=2  
        )  
        Appointment.objects.create(  
            patient=patient2, doctor=doctor2, case=case2, treatment=treatment2,  
            appointment_date="2025-11-26", appointment_time="11:00",  
            appointment_type="THERAPY", purpose="Physical therapy", status="CONFIRMED", priority=3  
        )  
        Appointment.objects.create(  
            patient=patient3, doctor=doctor1, case=case3, treatment=treatment3,  
            appointment_date="2025-11-27", appointment_time="14:00",  
            appointment_type="DIAGNOSTIC", purpose="MRI scan", status="SCHEDULED", priority=1  
        )  
        Appointment.objects.create(  
            patient=patient4, doctor=doctor3, case=case4, treatment=treatment4,  
            appointment_date="2025-11-28", appointment_time="10:00",  
            appointment_type="DIAGNOSTIC", purpose="Blood test", status="CONFIRMED", priority=2  
        )  
        Appointment.objects.create(  
            patient=patient5, doctor=doctor1, case=case5, treatment=treatment5,  
            appointment_date="2025-11-29", appointment_time="15:00",  
            appointment_type="CONSULTATION", purpose="Surgery consultation", status="SCHEDULED", priority=1  
        )  
        
        self.stdout.write(self.style.SUCCESS("Enhanced sample data inserted!"))  
        self.stdout.write(self.style.SUCCESS(f"Created {Patient.objects.count()} patients"))  
        self.stdout.write(self.style.SUCCESS(f"Created {Doctor.objects.count()} doctors"))  
        self.stdout.write(self.style.SUCCESS(f"Created {Case.objects.count()} cases"))  
        self.stdout.write(self.style.SUCCESS(f"Created {Appointment.objects.count()} appointments"))
    def test_queries(self):
        print("ORM example:")
        for p in Patient.objects.filter(last_name="Smith"):
            print("ORM ->", p.first_name, p.last_name)

        print("\nRAW example:")
        # * Using raw SQL query to fetch patients with last name 'Smith' with escape parameters to prevent SQL injection
        people = Patient.objects.raw("SELECT * FROM patient WHERE last_name=%s", ["Smith"])
        for p in people:
            print("RAW ->", p.first_name, p.last_name)
        # ! using raw SQL query to join multiple tables and fetch specific fields without escape parameters (not recommended for production due to SQL injection risk)
        print("\nRAW example (not safe):")
        query=" SELECT * FROM patient WHERE last_name LIKE'eissa'"
        results = Patient.objects.raw(query)
        for r in results:
            print("RAW JOIN ->", r.first_name, r.last_name, r.uuid)
        # * Using raw SQL with translations to map selected fields to model fields
        print("\nRAW with translations example:")
        name_map = {"first": "first_name", "last": "last_name", "uuid": "uuid"}
        people = Patient.objects.raw("SELECT first_name AS first, last_name AS last, uuid AS uuid FROM patient WHERE last_name=%s", ["Smith"], translations=name_map)
        for p in people:
            print("RAW with translations ->", p.first_name, p.last_name)
            
        # ========================indexing and inspecting database schema========================
        print("\nIndexing retrive example:")
        query ="select * from doctor"
        results = Doctor.objects.raw(query)[0]
        print("Indexing retrive ->", results)
        
        
        # ================================================================
        # NEW: CURSOR EXAMPLES
        # ================================================================

        print("\n--- Cursor Example 1: Normal tuple results with Python types ---")
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT uuid, first_name, last_name FROM patient")
            print("Executed description:", cursor.description)
            
            # Print column names
            print("Columns:", [desc[0] for desc in cursor.description])

            rows = cursor.fetchall()
            for row in rows:
                types = [type(value) for value in row]  # get Python types for each column
                print("Tuple ->", row, "| Types ->", types)

        print("\n--- Cursor Example 2: Dictionary results with Python types ---")

        def dictfetchall(cursor):
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT uuid, first_name, last_name, email FROM patient")
            
            rows = dictfetchall(cursor)
            for row in rows:
                types = {k: type(v) for k, v in row.items()}
                print("Dict ->", row, "| Types ->", types)

        print("\n--- Cursor Example 3: Named tuple results with Python types ---")
        from collections import namedtuple

        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT uuid, first_name, last_name FROM patient")
            
            columns = [col[0] for col in cursor.description]
            Row = namedtuple("Row", columns)
            rows = [Row(*r) for r in cursor.fetchall()]

            for row in rows:
                types = {col: type(getattr(row, col)) for col in row._fields}
                print(f"NamedTuple -> {row} | Types -> {types}")
