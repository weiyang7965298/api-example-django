from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    office_phone = models.CharField(max_length=35)

    def __str__(self):
        return str(self.id)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(null=True)
    gender = models.CharField(max_length=20)
    social_security_number = models.CharField(max_length=20)


class AppointmentQuerySet(models.QuerySet):
    def doctor_for_today(self, doctor):
        today = datetime.now()
        return self.filter(
            doctor=doctor,
            start_time__year=today.year,
            start_time__month=today.month,
            start_time__day=today.day
        ).order_by('start_time')

    def search_by_patient(self, **kwargs):
        updated_dict = {}
        for key in kwargs:
            new_key = "patient__{}".format(key)
            updated_dict[new_key] = kwargs[key]
        return self.filter(**updated_dict)


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    updated_time = models.DateTimeField(auto_now_add=True)
    #checkedin/noshow/complete/cancel/inprogress/rechedule
    start_time = models.DateTimeField(null=True)
    duration = models.IntegerField()
    real_completed_time = models.DateTimeField(null=True)
    checkin_time = models.DateTimeField(null=True)

    objects = models.Manager.from_queryset(AppointmentQuerySet)()


class WaitTime(models.Model):
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    wait_time = models.FloatField(null=True)
    def __str__(self):
        return str(self.wait_time)