from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet

# Initialisation du routeur pour UploadedFileViewSet
router = DefaultRouter()
router.register(r'files', UploadedFileViewSet, basename='uploadedfile')

urlpatterns = [
    path("", include(router.urls)),  # Inclus toutes les routes générées automatiquement par le routeur
]
