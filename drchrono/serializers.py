from datetime import datetime

from rest_framework.serializers import (
    CharField,
    IntegerField,
    DateTimeField,
    ModelSerializer,
)

from models import Doctor, Appointment, Patient, WaitTime


class DoctorSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = (
            "first_name",
            "last_name",
            "office_phone"
        )


class PatientSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "social_security_number",
            "date_of_birth"
        )

class WaitTimeSerializer(ModelSerializer):
    class Meta:
        model = WaitTime
        fields = '__all__'

class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = (
            "id",
            "patient",
            "status",
            "start_time",
            "duration",
            "real_completed_time",
            "checkin_time",
        )

    def validate(self, attrs):
        status = attrs.get("status")
        if status and status == 'Checked In':
            attrs["checkin_time"] = datetime.now()

        if status and status == "Complete":
            attrs["real_completed_time"] = datetime.now()

        return attrs