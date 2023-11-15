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
# from .models import Application


def get_voter_info(id_number):
    with connections['voter_db'].cursor() as cursor:
        cursor.execute(
            "SELECT constituency, location FROM voter_info WHERE id_number = %s", [id_number]
        )
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None, None


SPREADSHEET_NAME = 'Bursaries Project' # The name of the spreadsheet
CREDENTIALS_FILE_PATH = 'credentials.json' # credentials.json

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