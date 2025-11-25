from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from e_health.fields import CommaSeparatedCharField

# Create your models here.
class Patient (models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Information
    first_name = models.CharField(max_length=50, help_text="Patient's first name")
    last_name = models.CharField(max_length=50, help_text="Patient's last name")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    
    # Demographics
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField()
    
    # Contact Information
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    
    # Medical Information
    blood_type = models.CharField(max_length=3, blank=True)
    medical_history = models.TextField(blank=True, help_text="Previous medical conditions")
    allergies = models.TextField(blank=True, help_text="Known allergies")
    current_medications = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    
    # Status and Timestamps
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patient'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
class Doctor (models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Professional Information
    license_number = models.CharField(max_length=20, unique=True)
    medical_degree = models.CharField(max_length=100, help_text="e.g., MD, DO, MBBS")
    specialization = models.CharField(max_length=100, blank=True)
    sub_specialization = models.CharField(max_length=100, blank=True)
    board_certifications = models.TextField(blank=True)
    
    # Experience and Education
    years_of_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    medical_school = models.CharField(max_length=200, blank=True)
    residency_hospital = models.CharField(max_length=200, blank=True)
    
    # Contact and Location
    office_phone = models.CharField(max_length=15, blank=True)
    office_address = models.TextField(blank=True)
    hospital_affiliations = models.TextField(blank=True)
    
    # Financial and Scheduling
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    follow_up_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    availability_hours = models.CharField(max_length=200, blank=True, help_text="e.g., Mon-Fri 9-5")
    
    # Status
    is_available = models.BooleanField(default=True)
    is_accepting_new_patients = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor'
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
class Case (models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Case Identification
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Relationships
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='cases')
    primary_doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='primary_cases'
    )
    referring_doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referred_cases'
    )
    
    # Case Details
    chief_complaint = models.CharField(max_length=200, help_text="Main reason for visit")
    symptoms_description = models.TextField(help_text="Detailed description of symptoms")
    medical_history_notes = models.TextField(blank=True)
    physical_examination_notes = models.TextField(blank=True)
    
    # Diagnosis and Treatment
    preliminary_diagnosis = models.CharField(max_length=200, blank=True)
    final_diagnosis = models.CharField(max_length=200, blank=True)
    treatment_plan = models.TextField(blank=True)
    
    # Status and Priority
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('UNDER_REVIEW', 'Under Review'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
        ('REFERRED', 'Referred'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    
    PRIORITY_CHOICES = [
        (1, 'Emergency'),
        (2, 'Urgent'),
        (3, 'Normal'),
        (4, 'Low'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    
    SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
        ('CRITICAL', 'Critical'),
    ]
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True)
    
    # Financial Information
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    insurance_coverage = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    patient_liability = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'case'
        ordering = ['-created_at']
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['patient', 'created_at']),
        ]
    
    def __str__(self):
        return f"Case {self.case_number} - {self.patient.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            self.case_number = f"CASE{timezone.now().strftime('%Y%m%d')}{Case.objects.count() + 1:04d}"
        super().save(*args, **kwargs)

class Treatment (models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Information
    name = models.CharField(max_length=100, help_text="Treatment name")
    code = models.CharField(max_length=20, unique=True, help_text="Treatment code (e.g., CPT code)")
    description = models.TextField(help_text="Detailed description of the treatment")
    
    # Categorization
    CATEGORY_CHOICES = [
        ('DIAGNOSTIC', 'Diagnostic'),
        ('THERAPEUTIC', 'Therapeutic'),
        ('PREVENTIVE', 'Preventive'),
        ('SURGICAL', 'Surgical'),
        ('MEDICATION', 'Medication'),
        ('THERAPY', 'Therapy'),
        ('CONSULTATION', 'Consultation'),
    ]
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, blank=True)
    
    # Medical Details
    indications = models.TextField(blank=True, help_text="When this treatment is indicated")
    contraindications = models.TextField(blank=True, help_text="When this treatment should not be used")
    side_effects = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    
    # Cost and Duration
    base_cost = models.DecimalField(max_digits=8, decimal_places=2)
    insurance_coverage_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    estimated_duration_minutes = models.PositiveIntegerField()
    preparation_time_minutes = models.PositiveIntegerField(default=0)
    recovery_time_hours = models.PositiveIntegerField(default=0)
    
    # Requirements and Conditions
    requires_anesthesia = models.BooleanField(default=False)
    requires_hospitalization = models.BooleanField(default=False)
    requires_fasting = models.BooleanField(default=False)
    requires_specialist = models.BooleanField(default=False)
    min_age_requirement = models.PositiveIntegerField(null=True, blank=True)
    max_age_requirement = models.PositiveIntegerField(null=True, blank=True)
    
    # Equipment and Resources
    required_equipment = models.TextField(blank=True)
    required_medications = models.TextField(blank=True)
    required_staff_count = models.PositiveIntegerField(default=1)
    
    # Status and Availability
    is_active = models.BooleanField(default=True)
    is_experimental = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'treatment'
        ordering = ['category', 'name']
        verbose_name = 'Treatment'
        verbose_name_plural = 'Treatments'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class Appointment (models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    case = models.ForeignKey(
        Case, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='appointments'
    )
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    
    # Scheduling Information
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    estimated_duration = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Appointment Details
    APPOINTMENT_TYPE_CHOICES = [
        ('CONSULTATION', 'Consultation'),
        ('FOLLOW_UP', 'Follow-up'),
        ('PROCEDURE', 'Procedure'),
        ('SURGERY', 'Surgery'),
        ('THERAPY', 'Therapy'),
        ('DIAGNOSTIC', 'Diagnostic Test'),
        ('EMERGENCY', 'Emergency'),
    ]
    appointment_type = models.CharField(max_length=15, choices=APPOINTMENT_TYPE_CHOICES)
    
    purpose = models.CharField(max_length=200, help_text="Purpose of the appointment")
    special_instructions = models.TextField(blank=True)
    preparation_notes = models.TextField(blank=True)
    
    # Status and Priority
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='SCHEDULED')
    
    PRIORITY_CHOICES = [
        (1, 'Emergency'),
        (2, 'Urgent'),
        (3, 'Normal'),
        (4, 'Routine'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    
    # Location and Resources
    room_number = models.CharField(max_length=20, blank=True)
    location_notes = models.CharField(max_length=100, blank=True)
    required_equipment = models.TextField(blank=True)
    
    # Financial Information
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    insurance_approved = models.BooleanField(default=False)
    co_pay_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    # Communication
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    patient_contacted = models.BooleanField(default=False)
    
    # Outcome and Follow-up
    outcome_notes = models.TextField(blank=True)
    next_appointment_recommended = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    cancellation_reason = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'appointment'
        ordering = ['appointment_date', 'appointment_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        indexes = [
            models.Index(fields=['appointment_date', 'doctor']),
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['status', 'appointment_date']),
        ]
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor} on {self.appointment_date} at {self.appointment_time}"
    
    @property
    def is_upcoming(self):
        from datetime import datetime
        now = datetime.now()
        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)
        return appointment_datetime > now
    
    @property
    def duration_actual(self):
        if self.actual_start_time and self.actual_end_time:
            delta = self.actual_end_time - self.actual_start_time
            return delta.total_seconds() / 60  # Return minutes
        return None
    
    
    
    
    
class TestCustomFielModel(models.Model):
    number= models.IntegerField()
    comma_separated_numbers = CommaSeparatedCharField(max_length=255, separator=',')
    class Meta:
        db_table = 'test_custom_model'
