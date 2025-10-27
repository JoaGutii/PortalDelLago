from django.db import models
from django.conf import settings

class Incident(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Abierto'
        IN_PROGRESS = 'IN_PROGRESS', 'En progreso'
        RESOLVED = 'RESOLVED', 'Resuelto'

    title = models.CharField(max_length=200)
    description = models.TextField()
    room = models.CharField(max_length=50, blank=True, default='')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incidents_reported')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents_assigned')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.status}] {self.title}"

class LostFoundItem(models.Model):
    class State(models.TextChoices):
        REGISTERED = 'REGISTERED', 'Registrado'
        RETURNED = 'RETURNED', 'Entregado'

    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, default='')
    date_found = models.DateField()
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=State.choices, default=State.REGISTERED)
    delivered_to = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

class MaintenanceTask(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'HIGH', 'Alta'
        MEDIUM = 'MEDIUM', 'Media'
        LOW = 'LOW', 'Baja'

    title = models.CharField(max_length=200)
    detail = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_assigned')
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField(unique=True)
    keys_auth = models.CharField(max_length=255)
    keys_p256dh = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
