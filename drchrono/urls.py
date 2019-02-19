from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework.routers import DefaultRouter

admin.autodiscover()

import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, base_name='appointment')
router.register(r'waittime', views.WaitTimeViewSet, base_name='waittime')
urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='welcome'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/$', TemplateView.as_view(template_name="index.html")),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]

