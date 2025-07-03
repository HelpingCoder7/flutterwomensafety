
from . import views
from django.urls import path


urlpatterns = [
    path("",views.home),
    path('postotp/', views.send_otp),
    path('register/',views.register_user),
    path('loginuser/',views.loginuser),
    path('getall/',views.get_all_users),
    path('adduser/',views.add_user),

]