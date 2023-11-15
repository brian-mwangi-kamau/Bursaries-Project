from django.shortcuts import render
import requests
from .forms import ApplicationForm

def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = {
                'student_name': form.cleaned_data['student_name'],
                'gender': form.cleaned_data['gender'],
                'school_name': form.cleaned_data['school_name'],
                'admission_number': form.cleaned_data['admission_number'],
                'year_of_study': form.cleaned_data['year_of_study'],
                'constituency': form.cleaned_data['constituency'],
                'location': form.cleaned_data['location'],
                'phone_number': form.cleaned_data['phone_number'],
                'id_number': form.cleaned_data['id_number'],
                'email_address': form.cleaned_data['email_address'],
            }

            url = 'http://127.0.0.1:8000/api/v1/apply/'
            response = requests.post(url, data=data)

            if response.status_code == 201:
                return render(request, 'success.html')
            elif response.status_code == 400:
                return render(request, 'failure.html')
            else:
                print(f'Unexpected status code: {response.status_code}')

    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form})
