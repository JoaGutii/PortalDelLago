from rest_framework import serializers
from .models import Incident, LostFoundItem, MaintenanceTask, NotificationSubscription
import bleach

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ('reported_by','created_at','updated_at')

    def validate_title(self, v):
        return bleach.clean(v)

    def validate_description(self, v):
        return bleach.clean(v)

class LostFoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostFoundItem
        fields = '__all__'
        read_only_fields = ('registered_by','created_at')

    def validate_description(self, v):
        return bleach.clean(v)

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = '__all__'
        read_only_fields = ('created_by','created_at','updated_at')

    def validate_title(self, v):
        return bleach.clean(v)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSubscription
        fields = ('id','endpoint','keys_auth','keys_p256dh')
