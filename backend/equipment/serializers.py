from rest_framework import serializers
from .models import Equipment, UploadBatch


class UploadBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadBatch
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    upload_batch_id = serializers.IntegerField(source='upload_batch.id', read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'
