from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Incident, LostFoundItem, MaintenanceTask, NotificationSubscription
from .serializers import IncidentSerializer, LostFoundSerializer, MaintenanceTaskSerializer, SubscriptionSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from pywebpush import webpush, WebPushException

User = get_user_model()

class IsAuthenticatedOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return super().has_permission(request, view)

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        obj = serializer.save(reported_by=self.request.user)
        self.broadcast('incident_created', obj)

    def perform_update(self, serializer):
        obj = serializer.save()
        self.broadcast('incident_updated', obj)

    def perform_destroy(self, instance):
        pk = instance.pk
        instance.delete()
        self.broadcast('incident_deleted', {'id': pk})

    def broadcast(self, event, payload):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications', {'type': 'notify', 'event': event, 'payload': IncidentSerializer(payload).data if isinstance(payload, Incident) else payload}
        )

class LostFoundViewSet(viewsets.ModelViewSet):
    queryset = LostFoundItem.objects.all().order_by('-created_at')
    serializer_class = LostFoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        obj = serializer.save(registered_by=self.request.user)
        self.broadcast('lostfound_created', obj)

    def perform_update(self, serializer):
        obj = serializer.save()
        self.broadcast('lostfound_updated', obj)

    def perform_destroy(self, instance):
        pk = instance.pk
        instance.delete()
        self.broadcast('lostfound_deleted', {'id': pk})

    def broadcast(self, event, payload):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications', {'type': 'notify', 'event': event, 'payload': LostFoundSerializer(payload).data if isinstance(payload, LostFoundItem) else payload}
        )

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTask.objects.all().order_by('-created_at')
    serializer_class = MaintenanceTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        obj = serializer.save(created_by=self.request.user)
        self.broadcast('task_created', obj)

    def perform_update(self, serializer):
        obj = serializer.save()
        self.broadcast('task_updated', obj)

    def perform_destroy(self, instance):
        pk = instance.pk
        instance.delete()
        self.broadcast('task_deleted', {'id': pk})

    def broadcast(self, event, payload):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications', {'type': 'notify', 'event': event, 'payload': MaintenanceTaskSerializer(payload).data if isinstance(payload, MaintenanceTask) else payload}
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def subscribe_push(request):
    data = request.data
    sub, _ = NotificationSubscription.objects.get_or_create(
        user=request.user,
        endpoint=data['endpoint'],
        defaults={'keys_auth': data['keys']['auth'], 'keys_p256dh': data['keys']['p256dh']}
    )
    return Response({'status':'ok'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def push_test(request):
    subs = NotificationSubscription.objects.filter(user=request.user)
    for s in subs:
        try:
            webpush(
                subscription_info={
                    "endpoint": s.endpoint,
                    "keys": {"auth": s.keys_auth, "p256dh": s.keys_p256dh}
                },
                data="Notificación de prueba",
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": settings.VAPID_EMAIL},
                vapid_public_key=settings.VAPID_PUBLIC_KEY
            )
        except WebPushException as e:
            pass
    return Response({'sent': subs.count()})
