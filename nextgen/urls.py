"""nextgen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from newgen import views
from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.urls import re_path
from django.views.generic import TemplateView
from nextgen.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.views.static import serve
from nextgen import settings


urlpatterns = [
    path('main', views.mainworker,name = 'main'),
    re_path(r'^admin/*', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    re_path(r'^organisations_requests', views.organisations_requests, name='organisations_requests'),
    re_path(r'^new_request', views.new_request, name='new_request'),
     re_path(r'^delete_temp_note', views.delete_temp_note, name='delete_temp_note'),
    re_path(r'^delete_tool', views.delete_tool, name='delete_tool'),
    re_path(r'^tool_transfers', views.tool_transfers, name='tool_transfers'),
    re_path(r'^edit_tool', views.edit_tool, name='edit_tool'),
    re_path(r'^notice_work', views.notice_work, name='notice_work'),
    re_path(r'^add_tool', views.add_tool, name='add_tool'),
    re_path(r'^tool_forwarding', views.tool_forwarding, name='tool_forwarding'),
    re_path(r'^add_temp_close_request', views.add_temp_close_request, name='add_temp_close_request'),
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^job_evaluation/(?P<encrypted_text>\w+)',views.job_evaluation),
    re_path(r'^evaluation', views.evaluation, name='evaluation'),
    re_path(r'^404', views.unknown_page, name='unknown_page'),
    #re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    #re_path(r'^inbox/notifications/delete/(?P<slug>\d+)/', views.delete),
    #re_path(r'^mark_as_read/(?P<description>\d+)',views.mark_as_read),
    re_path(r'^tools/',views.tools, name='tools'),
    re_path(r'^inserting_auth_code/',views.inserting_auth_code, name='inserting_auth_code'),
    re_path(r'^confirm_email/',views.confirm_email, name='confirm_email'),
    re_path(r'^it/',views.it, name='it'),
    #re_path(r'^webpush/', include('webpush.urls')),
    #re_path(r'^sw.js$', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    re_path(r'^.*$', RedirectView.as_view(url='main')), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)