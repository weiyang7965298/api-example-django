from django.db import models

class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    access_token = models.CharField(max_length=200, null=True, blank=True, default=None)
    refresh_token = models.CharField(max_length=200, null=True, blank=True, default=None)
    token_expires_timestamp = models.DateTimeField(auto_now_add=False, null=True, blank=True, default=None)
    def __str__(self):
        return str(self.id)

class Patient(models.Model):
    irst_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    ssn = models.CharField(max_length=20)

class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    updated_time = models.DateTimeField(auto_now_add=True)
    #checkedin/noshow/complete/cancel/inprogress/rechedule
    #appoint time
    start_time = models.DateTimeField(null=True)
    # schedule appointment end time
    completed_time = models.DateTimeField(null=True)
    real_start_time = models.DateTimeField(null=True)
    real_completed_time = models.DateTimeField(null=True)
    checkin_time = models.DateTimeField(null=True)


class WaitTime(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateField(primary_key=True)
    wait_time = models.IntegerField(null=True)
    def __str__(self):
        return str(self.wait_time)