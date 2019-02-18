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
from serializers import AppointmentSerializer
from models import Doctor, Appointment


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

    def _get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self._get_token()
        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs


class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # need to check the doctor who is currently login
        doctor_id = self.request.GET.get("doctor")
        if not doctor_id:
            return self.queryset.none()
        try:
            doctor = Doctor.objects.get(id="doctor_id")
            return self.queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return self.queryset.none()

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        params = request.GET.dict()
        appts = self.queryset.filter(**params)
        serializer = self.get_serializer(instance=appts, many=True)
        return Response(serializer.data)



# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from django.views.generic import View, TemplateView
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout as django_logout
# from rest_framework import viewsets, filters

# from social_django.models import UserSocialAuth
# from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, AppointmentProfileEndpoint
# from serializers import AppointmentSerializer
# from models import Doctor, Appointment

# def search_appointment(request):
#     params = request.GET.dict()
#     appts = Appointment.objects.filter(**params)
#     return AppointmentSerializer(instance=appts, many=True).data
    

# def appointment_list(request):
#     # need to check the doctor who is currently login
#     doctor_id = request.GET("doctor")
#     if not doctor_id:
#         return JsonResponse({"msg": "FAIL"}) # any json data you want to return
#     try:
#         doctor = Doctor.objects.get(id="doctor_id")
#         appts = Appointment.objects.filter(doctor=doctor)
#         serializer = AppointmentSerializer(instance=appts, many=True)
#         return serializer.data
#     except Doctor.DoesNotExist:
#         return JsonResponse({"msg": "FAIL"}) # any json data you want to return

# def appointment_by_id(request, id=None):
#     # need to check the doctor who is currently login
#     doctor_id = request.GET("doctor")
#     if not doctor_id:
#         return JsonResponse({"msg": "FAIL"}) # any json data you want to return
#     try:
#         doctor = Doctor.objects.get(id="doctor_id")
#         # filter by doctor and today first, then retrieve by id
#         appts = Appointment.objects.filter(doctor=doctor)
#         appt = appts.get(id=id)
#         serializer = AppointmentSerializer(instance=appt)
#         return serializer.data
#     except (Doctor.DoesNotExist, Appointment.DoesNotExist):
#         return JsonResponse({"msg": "FAIL"})  # any json data you want to return

# class SetupView(View):
#     """
#     The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
#     """
#     http_method_names = ['get'] # only allow get request

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return redirect('welcome')
#         return render(request, 'kiosk_setup.html')


# class DoctorWelcome(TemplateView):
#     """
#     The doctor can see what appointments they have today.
#     """
#     template_name = 'doctor_welcome.html'

#     # @login_required(login_url='/setup')
#     def dispatch(self, request, *args, **kwargs):
#         return super(DoctorWelcome, self).dispatch(request, *args, **kwargs)

#     def _get_token(self):
#         """
#         Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
#         already signed in.
#         """
#         oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
#         access_token = oauth_provider.extra_data['access_token']
#         return access_token

#     def make_api_request(self):
#         """
#         Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
#         proved that the OAuth setup is working
#         """
#         # We can create an instance of an endpoint resource class, and use it to fetch details
#         access_token = self._get_token()
#         api = DoctorEndpoint(access_token)
#         # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
#         # account probably only has one doctor in it.
#         return next(api.list())

#     def get_context_data(self, **kwargs):
#         kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
#         # Hit the API using one of the endpoints just to prove that we can
#         # If this works, then your oAuth setup is working correctly.
#         doctor_details = self.make_api_request()
#         kwargs['doctor'] = doctor_details
#         return kwargs


# class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         # need to check the doctor who is currently login
#         doctor_id = self.request.GET("doctor")
#         if not doctor_id:
#             return None

#         try:
#             doctor = Doctor.objects.get(id="doctor_id")
#             return self.queryset.filter(doctor=doctor)
#         except Doctor.DoesNotExist:
#             return None

