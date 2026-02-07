from rest_framework.routers import DefaultRouter
from .views import ReportViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls))
]
