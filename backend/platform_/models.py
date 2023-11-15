from django.db import models


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255, blank=False)
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices= GENDER_CHOICES, blank=False)
    school_name = models.CharField(max_length=255, blank=False)
    admission_number = models.CharField(max_length=30, blank=False)
    year_of_study = models.CharField(max_length=50, blank=False)
    CONSTITUENCY_CHOICES = [
        ('Ndaragwa', 'Ndaragwa'),
    ]
    constituency = models.CharField(max_length=25, choices= CONSTITUENCY_CHOICES, blank=False)
    LOCATION_CHOICES = [
        ('Karai', 'Karai'),
        ('Kirima', 'Kirima'),
        ('Kahira', 'Kahira'),
        ('Kanyagia', 'Kanyagia'),
        ('Kahutha', 'Kahutha'),
        ('Kiriogo', 'Kiriogo'),
        ('Muruai', 'Muruai'),
        ('Mwangaza', 'Mwangaza'),
        ('Mwihoko', 'Mwihoko'),
        ('Mairo inya', 'Mairo Inya'),
        ('Mathingira', 'Mathingira'),
        ('Ngawa', 'Ngawa'),
        ('Shamata', 'Shamata'),
    ]
    location = models.CharField(max_length=25, choices= LOCATION_CHOICES, blank=False)
    phone_number = models.CharField(max_length=10, blank=False) # This could be the student's or parent's phone number.
    id_number = models.CharField(max_length=8) # This could be the student's ID number(if they are registered as a voter) or the parent's.
    email_address = models.EmailField(blank=True) # This is optional. It could be used to send updates to the applicant.
    submission_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student_name}"
