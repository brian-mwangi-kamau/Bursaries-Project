## The NG-CDF Bursaries Program  -  A server-side approach

#### In this step-by-step overview, I will take you through the basic setup of the system.

__Prerequisites__:
  - Basic Programming 
  - The Python Programming Language
  - The Django framework 


This project is built in __Django__ with __Python__.

We have a  `models.py` file, containing the following code:<br>
This is a model that holds/carries the applications being submitted by users.

```python
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
```

The server-side logic, being built with the __Django Rest Framework__, contains a ```serializers.py``` file that contains the code below:
```python
from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
```

The ```views.py``` fie contains the code below:
```python
# Imports
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db import connections
import smtplib
import gspread
import os

from .serializers import ApplicationSerializer
```


#### The view below collects the application data from a POST request, and processes it by calling the ```get_voter_info``` function, which queries the voter database to determine whether the application is valid or invalid.
```python
class ApplicationViewset(APIView):

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            voter_constituency, voter_location = get_voter_info(serializer.validated_data['id_number'])

            if (
                voter_constituency == serializer.validated_data['constituency']
                and voter_location == serializer.validated_data['location']
            ):
                save_to_spreadsheets({
                    "student_name": serializer.validated_data['student_name'],
                    "school_name": serializer.validated_data['school_name'],
                    "admission_number": serializer.validated_data['admission_number'],
                    "gender": serializer.validated_data['gender'],
                    "year_of_study": serializer.validated_data['year_of_study'],
                    "constituency": serializer.validated_data['constituency'],
                    "location": serializer.validated_data['location'],
                })
                return Response(serializer.errors, status=status.HTTP_201_CREATED)
            else:
                # print("Conditions in the if block are NOT met")
                send_application_to_admin(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # print("The form is invalid")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

The ```get_voter_info``` function which queries the __IEBC__*(voter database)*:

```python
def get_voter_info(id_number):
    with connections['voter_db'].cursor() as cursor:
        cursor.execute(
            "SELECT constituency, location FROM voter_info WHERE id_number = %s", [id_number]
        )
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None, None
```

The other function is the view that sends valid applications to a __Google Spreadsheet__.:

```python
def save_to_spreadsheets(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE_PATH, scope)
        client = gspread.authorize(credentials)

        spreadsheet = client.open(SPREADSHEET_NAME)

        worksheet = spreadsheet.get_worksheet(0)

        worksheet.append_row([
            data["student_name"],
            data["school_name"],
            data["admission_number"],
            data["gender"],
            data["year_of_study"],
            data["constituency"],
            data["location"],
        ])

    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
```

#### This saves the application data for every valid application to a spreadsheet.

The view below ```send_application_to_admin``` sends invalid applications to the administrator's email address:

```python
def send_application_to_admin(application_data):
    subject = "New Application Review"
    message = (
        f"Application details:\n\n"
        f"Name: {application_data['student_name']}\n"
        f"School: {application_data['school_name']}\n"
        f"Admission Number: {application_data['admission_number']}\n"
        f"Gender: {application_data['gender']}\n"
        f"Year of Study: {application_data['year_of_study']}\n"
        f"Constituency: {application_data['constituency']}\n"
        f"Location: {application_data['location']}\n"
        f"Phone Number: {application_data['phone_number']}\n"
        f"ID Number: {application_data['id_number']}\n"
        f"Email Address: {application_data['email_address']}\n"
    )

    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_username = os.environ.get("EMAIL_HOST_USER")
    smtp_password = os.environ.get("EMAIL_HOST_PASSWORD")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if not all([smtp_username, smtp_password, recipient_email]):
        print("Missing email configuration. Please check your environment variables.")
        return

    from_email = smtp_username
    to_email = recipient_email

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        # print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        # pass
```


The ```urls.py``` file in our app directory maps the views to routes with the following code:

```python
from django.urls import path
# from rest_framework.routers import DefaultRouter

from .views import ApplicationViewset

# router = DefaultRouter()
# router.register(r'v1/apply', ApplicationViewset, basename='application')


urlpatterns = [
    path('api/v1/apply/', ApplicationViewset.as_view(), name='apply')
]
```

When an application is submitted, the browser directs to ```https://the_frontend_url/api/v1/apply``` which maps to the view for handling applications.

#### Refer to the client-side logic in the README file located in the `frontend/` folder.