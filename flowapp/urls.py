from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('flow/',views.flows,name='flow'),
    path('login/',auth_views.LoginView.as_view(template_name='flowapp/login.html'),name='login'),
    path('flow/<str:connection_name>/edit',views.connection_edit,name='connection-edit'),
    path('flow/<str:connection_name>/delete',views.connection_delete,name='connection-delete'),
]
