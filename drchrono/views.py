from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout

from rest_framework.decorators import action
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, AppointmentProfileEndpoint
from api_helper import process_api_request, get_token
from serializers import AppointmentSerializer, DoctorSerializer, WaitTimeSerializer
from models import Doctor, Appointment, WaitTime
from datetime import datetime

class SetupView(View):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    http_method_names = ['get'] # only allow get request

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('welcome')
        return render(request, 'kiosk_setup.html')


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/setup')
        return super(DoctorWelcome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        kwargs['doctor'] = kwargs.pop("doctor_detail")
        return kwargs

    def get(self, request, *args, **kwargs):
        doctor_detail = process_api_request(request)
        context = self.get_context_data(doctor_detail=doctor_detail)
        return self.render_to_response(context)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get_queryset(self):
        # need to check the doctor who is currently login
        try:
            today = datetime.now()
            doctor = Doctor.objects.first()
            # doctor = Doctor.objects.get(user=self.request.user)
            return self.queryset.filter(
                doctor=doctor,
                start_time__year=today.year,
                start_time__month=today.month,
                start_time__day=today.day
            ).order_by('start_time')
        except Doctor.DoesNotExist:
            return self.queryset.none()

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        params = request.GET.dict()
        updated_dict = {}
        for key in params:
            new_key = "patient__{}".format(key)
            updated_dict[new_key] = params[key]

        appts = self.queryset.filter(**updated_dict)
        serializer = self.get_serializer(instance=appts, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        resp = super(AppointmentViewSet, self).update(request, *args, **kwargs)
        instance = self.get_object()
        api = AppointmentEndpoint(get_token())
        api.update(instance.id, request.data, partial=True)

        if instance.checkin_time and instance.real_completed_time:
            # create wait time object, do your self to calculate the waititme at line 85
            wait_time = (instance.real_completed_time - instance.checkin_time).total_sceonds()
            WaitTime.objects.create(appointment=instance, wait_time=wait_time)

        return resp


class WaitTimeViewSet(viewsets.ModelViewSet):
    queryset = WaitTime.objects.all()
    serializer_class = WaitTimeSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    def get_queryset(self):
        # need to check the doctor who is currently login
        try:
            # doctor = Doctor.objects.get(user=self.request.user)
            doctor = Doctor.objects.first()
            today = datetime.now()
            return self.queryset.filter(appointment__doctor=doctor,
            date__year=today.year,
            date__month=today.month,
            date__day=today.day)
        except Doctor.DoesNotExist:
            return self.queryset.none()
