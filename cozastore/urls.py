"""Cozastore URL configuration"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('', RedirectView.as_view(url='store/', permanent=True)),
    path('csvs', include('csvs.urls', namespace='csvs')),
]

# Authentication urls
urlpatterns += [
    path('accounts/login', views.ContextLoginView.as_view(), name ='login'),
    path('accounts/logout', views.ContextLogoutView.as_view(), name ='logout'),
    path('accounts/password-reset', views.ContextPasswordResetView.as_view(), 
        name ='password_reset'),
    path('accounts/password-reset-done', views.ContextPasswordResetDone.as_view(),
        name ='password_reset_done'),
    path('accounts/password-reset-confirm', views.ContextPasswordResetConfirm.as_view(),
        name ='password_reset_confirm'),
    path('accounts/password-reset-complete', views.ContextPasswordResetComplete.as_view(), 
        name ='password_reset_complete'),
    path('accounts/register', views.register, name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Automatically create URL to reference a media file
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
