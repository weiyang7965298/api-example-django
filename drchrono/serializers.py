from rest_framework.serializers import (
    CharField,
    IntegerField,
    DateTimeField,
    ModelSerializer,
)

from models import Doctor, Appointment, Patient

class PatientSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "ssn",
            "date_of_birth"
        )

class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = (
            "id",
            "patient",
            "status",
            "start_time",
            "completed_time",
            "real_completed_time",
            "checkin_time",
        )