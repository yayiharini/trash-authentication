from rest_framework import serializers
from .models import newusers
import hashlib


class newuserserializer(serializers.ModelSerializer):
    class Meta:
        model = newusers
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
