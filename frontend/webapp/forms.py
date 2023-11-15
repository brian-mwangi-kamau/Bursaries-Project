from django import forms
from django.core.validators import RegexValidator


class ApplicationForm(forms.Form):
    student_name = forms.CharField(max_length=255, label="Name of Student")
    gender = forms.CharField(max_length=10, label="Gender")
    school_name = forms.CharField(max_length=255, label="Name of School")
    admission_number = forms.CharField(max_length=30, label="Admission Number")
    year_of_study = forms.CharField(max_length=50, label="Form or Year of Study")
    constituency = forms.CharField(max_length=15, label="Constituency")
    location = forms.CharField(max_length=15, label="Location")
    phone_number = forms.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Enter a valid phone number')],
        label="Phone Number"
    )
    id_number = forms.CharField(max_length=8, label="ID Number")
    email_address = forms.EmailField(label="Email Address")