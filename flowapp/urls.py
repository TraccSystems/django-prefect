from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='flowapp/login.html'),name='login'),
    path('flow/<str:flow_name>/edit',views.flow_edit,name='flow-edit'),
    path('flow/<str:flow_name>/delete',views.flow_delete,name='flow-delete'),
    path('flow/schedule/',views.schedule,name='schedule'),
    path('flow/run/',views.runflow,name='runflow')
]
