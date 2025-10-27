from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import IncidentViewSet, LostFoundViewSet, MaintenanceTaskViewSet, subscribe_push, push_test

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incidents')
router.register(r'lostfound', LostFoundViewSet, basename='lostfound')
router.register(r'tasks', MaintenanceTaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('push/subscribe/', subscribe_push),
    path('push/test/', push_test),
]
