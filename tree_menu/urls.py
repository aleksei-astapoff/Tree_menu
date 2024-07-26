from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name='base.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='base.html'), name='about'),
    path('services/', TemplateView.as_view(template_name='base.html'), name='services'),
    path('contact/', TemplateView.as_view(template_name='base.html'), name='contact'),
    path('services/web-development/', TemplateView.as_view(template_name='base.html'), name='web-development'),
    path('services/seo/', TemplateView.as_view(template_name='base.html'), name='seo'),
    path('services/marketing/', TemplateView.as_view(template_name='base.html'), name='marketing'),
    path('services/seo/level-2/', TemplateView.as_view(template_name='base.html'), name='seo-level-2'),
    path('services/seo/level-3/', TemplateView.as_view(template_name='base.html'), name='seo-level-3'),
    path('overview/', TemplateView.as_view(template_name='base.html'), name='overview'),
    path('team/', TemplateView.as_view(template_name='base.html'), name='team'),
]
