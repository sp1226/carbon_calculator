from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from calculator.views import CarbonCalculationViewSet

router = DefaultRouter()
router.register(r'calculations', CarbonCalculationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
