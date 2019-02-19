from datetime import datetime, timedelta

from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint
from serializers import AppointmentSerializer, DoctorSerializer, PatientSerializer
from models import Doctor, Appointment, Patient


def get_token():
    """
    Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
    already signed in.
    """
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    return access_token


def process_api_request(request):
    access_token = get_token()
    doctor_detail = make_doctor_api_request(request, access_token)
    make_patient_api_request(access_token)
    make_appt_api_request(access_token)

    return doctor_detail


def make_doctor_api_request(request, access_token):
    doctor_api = DoctorEndpoint(access_token)
    detail = next(doctor_api.list())
    doctor, _ = Doctor.objects.get_or_create(
        id=detail["id"],
        user=request.user,
        first_name=detail["first_name"],
        last_name=detail["last_name"],
        office_phone=detail["office_phone"]
    )
    return DoctorSerializer(instance=doctor).data


def make_appt_api_request(access_token):
    appt_api = AppointmentEndpoint(access_token)
    for appt in appt_api.list(date=datetime.now()):
        obj, _ = Appointment.objects.update_or_create(
            pk=appt["id"],
            defaults={
                "doctor": Doctor.objects.get(id=appt["doctor"]),
                "patient": Patient.objects.get(id=appt["patient"]),
                "status": appt["status"],
                "start_time": appt["scheduled_time"],
                "duration": appt["duration"]
            }
        )


def make_patient_api_request(access_token):
    patient_api = PatientEndpoint(access_token)
    for patient in patient_api.list():
        Patient.objects.update_or_create(
            pk=patient["id"],
            defaults={
                "doctor": Doctor.objects.get(id=patient["doctor"]),
                "first_name": patient["first_name"],
                "last_name": patient["last_name"],
                "date_of_birth": patient["date_of_birth"],
                "social_security_number": patient["social_security_number"],
                "gender": patient["gender"]
            }
        )
