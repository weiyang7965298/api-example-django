from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework.routers import DefaultRouter

admin.autodiscover()

import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, base_name='appointment')

urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='welcome'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/$', TemplateView.as_view(template_name="index.html")),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]


# from django.conf.urls import include, url
# from django.contrib.auth.decorators import login_required
# from django.views.generic import TemplateView
# from django.contrib import admin
# from rest_framework.routers import DefaultRouter

# admin.autodiscover()

# import views

# router = DefaultRouter()
# router.register(r'appointments', views.AppointmentViewSet, base_name='appointment')

# urlpatterns = [

#     url(r'^api/', include(router.urls, namespace='api')),
#     # url(r'^api/appointments/$', views.appointment_list, name="list_appointment"),
#     # url(r'^api/appointments/(\d+)/$', views.appointment_by_id, name="retrieve_appointment"),
#     # url(r'^api/appointment/search/$', views.search_appointment, name="search_appointment"),
#     url(r'^setup/$', views.SetupView.as_view(), name='setup'),
#     url(r'^welcome/$', views.DoctorWelcome.as_view(), name='welcome'),
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^main/$', TemplateView.as_view(template_name="index.html")),
#     url(r'', include('social.apps.django_app.urls', namespace='social')),
# ]

