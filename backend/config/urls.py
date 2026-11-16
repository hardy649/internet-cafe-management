
from django.contrib import admin
from django.urls import path
from cafe import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),

    path('api/', views.home),

    # Компьютер, үнэ, үйлчилгээ
    path('api/computer-types/', views.computer_types),
    path('api/computers/', views.computers),
    path('api/pricings/', views.pricings),
    path('api/services/', views.services),

    # Authentication
    path('api/register/', views.register_user),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/profile/', views.my_profile),
]
