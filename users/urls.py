from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('adminlogin/', views.adminlogin_view, name='admin_login'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('registrations/<int:event_id>/', views.event_registrations, name='event_registrations'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('manage-registrations/', views.manage_registrations, name='manage_registrations'),
    path('delete-registration/<int:registration_id>/', views.delete_registration, name='delete_registration'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)